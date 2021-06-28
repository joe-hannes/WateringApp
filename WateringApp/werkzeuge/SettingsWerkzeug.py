import os
import requests
from requests.exceptions import ConnectionError
import time
import math
from statistics import StatisticsError


from flask import Flask, render_template, Blueprint
from flask_user import login_required

from influxdb import InfluxDBClient

import WateringApp.WateringSystem as wsys
from WateringApp.config import API_KEY
from WateringApp.werkzeuge.shared import session
from WateringApp.Models import Settings, Widget
from WateringApp.forms.settings_form import SettingsForm
from WateringApp.werkzeuge.shared import menu_items
from WateringApp.linear_regression import calc_params, regress





settings = Blueprint('settings', __name__)
restartView = Blueprint('restartView', __name__)
reset_water_level = Blueprint('reset_water_level', __name__)


def calculate_refill():

    with session as sess:
        consumption = sess.query(Settings).first().consumption
        current_water_level = sess.query(Widget).first().current_water_level

    max_pump_activations = math.floor(current_water_level / consumption)


    try:

        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('humidity')

        with session as sess:
            location = sess.query(Settings).first().location

        interval = 14

        activations_result = client.query('SELECT "count" FROM (select count("value"), time from "activation" GROUP BY time({}d)) WHERE "count" > 0'.format(interval))
        temperature_result = client.query('SELECT mean("value") FROM temperature GROUP BY time({}d)'.format(interval))

        # use these to test
        # demo_temp = [24,11,25,13,14,23,16,17,18,23]
        # demo_act = [11,2,12,4,5,10,7,8,9,10]
        activations = [act['count'] for act in list(activations_result.get_points())]
        temperature =   [temp['mean'] for temp in list(temperature_result.get_points())]

        base_url = 'http://api.openweathermap.org/data/2.5/'
        type = ['weather', 'history', 'forecast']
        country_code = ',DEU'
        concat_url = base_url + type[2] + "/daily" + '?q=' + location.strip() + country_code + "&cnt=15" '&appid=' + API_KEY
        conversion_val = 273.15

        r = requests.get(concat_url)
        data = r.json()
        reg_params = calc_params(temperature, activations)
        temp = sum([ temp['temp']['day'] for temp in data['list'] ]) / len(data['list'])


        actual_pump_activations = regress(temp - conversion_val, reg_params)
        refill_time = max_pump_activations / actual_pump_activations * interval


    except (ConnectionError, ZeroDivisionError, StatisticsError)  as e:
        print("""Cant use linear regression for refill time calculation because
            there are either too few datapoints on no internet connection.
            Proceeding by using normal estimation instead""")

        with session as sess:
            last_activation = sess.query(Widget).first().last_activation

        interval = time.time() - last_activation

        refill_time = max_pump_activations * (interval / 360 / 24)



    # print('refill_time: {} days'.format(refill_time))

    return round(refill_time, 2)



# TODO: statisticsError needs at least 1 datapoint
@settings.route("/settings", methods= ['GET', 'POST'])
@login_required
def settings_page():
    """view: displays the settingspage with the according values"""
    form = SettingsForm()

    refill_time = -1

    if form.validate_on_submit():
        # when a form is submitted update database entries and set internal system
        # state
        # print('form submitted')
        with session as sess:
            sess.query(Settings).first().location = form.location.data
            sess.query(Settings).first().reservoir_size = form.reservoir_size.data
            sess.query(Settings).first().consumption = form.consumption.data
            sess.query(Settings).first().reservoir_warn_level = form.reservoir_warn_level.data
            sess.query(Widget).first().activation_level = form.activation_level.data
            sess.query(Settings).first().api_key = form.api_key.data

            reservoir_size = sess.query(Settings).first().reservoir_size

            if reservoir_size != form.reservoir_size.data:
                sess.query(Widget).first().current_water_level = reservoir_size

            sess.commit()
            wsys.wsys.set_activation_level(form.activation_level.data)

        refill_time = calculate_refill()

    with session as sess:
        settings = sess.query(Settings).first()
        # print('settings: {}'.format(settings))


    return render_template(
        "settings.html",
        menu_items = menu_items,
        view_name='Settings',
        form = form,
        settings = settings,
        refill_time = refill_time)


@restartView.route("/restart")
@login_required
def restart():
    """restart the machine"""
    os.system('sudo reboot now')
    return 'restarting'


@reset_water_level.route("/reset_water_level", methods=['GET', 'POST'])
@login_required
def reset_water_level_func():
    """endpoint:
    update the water_level in the database and sets the internal System instance variable"""

    # TODO: validate input
    with session as sess:
        reservoir_size = sess.query(Settings).first().reservoir_size
        sess.query(Widget).first().current_water_level = reservoir_size
        sess.query(Widget).first().widget_state = False
        sess.commit()

        wsys.wsys.set_state(False)

    return 'success'
