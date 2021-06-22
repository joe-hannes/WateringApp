from flask import Flask, render_template, Blueprint
from flask_user import login_required
import os
import requests
import time

from influxdb import InfluxDBClient

from WateringApp.werkzeuge.shared import session
from WateringApp.Models import Settings, Widget

from WateringApp.forms.settings_form import SettingsForm


from WateringApp.werkzeuge.shared import menu_items

from WateringApp.linear_regression import beta_one, regress

import WateringApp.WateringSystem as wsys

from WateringApp.config import API_KEY

settings = Blueprint('settings', __name__)
restartView = Blueprint('restartView', __name__)
reset_water_level = Blueprint('reset_water_level', __name__)


calculate_refill = Blueprint('calculate_refill', __name__)


@settings.route("/settings", methods= ['GET', 'POST'])
@login_required
def settings_page():

    form = SettingsForm()

    if form.validate_on_submit():
        print('form submitted')
        with session as sess:
            sess.query(Settings).first().location = form.location.data
            sess.query(Settings).first().reservoir_size = form.reservoir_size.data
            sess.query(Settings).first().consumption = form.consumption.data
            sess.query(Settings).first().reservoir_warn_level = form.reservoir_warn_level.data
            sess.query(Widget).first().activation_level = form.activation_level.data
            sess.commit()
            wsys.wsys.set_activation_level(form.activation_level.data)



    with session as sess:
        settings = sess.query(Settings).first()
        print('settings: {}'.format(settings))


    # return render_template("settings.html", )
    return render_template("settings.html", menu_items = menu_items, view_name='Settings', form = form, settings = settings)


@restartView.route("/restart")
@login_required
def restart():
    os.system('sudo reboot now')
    return 'restarting'


@reset_water_level.route("/reset_water_level", methods=['GET', 'POST'])
@login_required
def reset_water_level_func():
    with session as sess:
        reservoir_size = sess.query(Settings).first().reservoir_size
        sess.query(Widget).first().current_water_level = reservoir_size
        sess.commit()
    return render_template("settings.html", menu_items = menu_items, view_name='Settings', form = form, settings = settings)


@calculate_refill.route("/calculate_refill", methods=['POST'])
@login_required
def calculate_refill_func():

    with session as sess:
        location = sess.query(Settings).first().location

    base_url = 'http://api.openweathermap.org/data/2.5/'

    type = ['weather', 'history', 'forecast']

    country_code = ',DEU'


    concat_url = base_url + type[2] + '?q=' + location.strip() + country_code + '&appid=' + API_KEY
    conversion_val = 273.15

    # print('concat_url: {}'.format(concat_url))

    # TODO: catch network exception, error 404
    r = requests.get(concat_url)

    # print('response: {}'.format(r.text))
    # temperature = r.main.temp - convertion_val

    data = r.json()

    # print(f'data_list length: {len(data)}')



    client = InfluxDBClient(host='localhost', port=8086)
    client.switch_database('humidity')

    activations_result = client.query('SELECT "count" FROM (select count("value"), time from "activation" GROUP BY time(1w)) WHERE "count" > 0')
    temperature_result = client.query('SELECT mean("value") FROM temperature GROUP BY time(1w)')

    activations = [act['count'] for act in list(activations_result.get_points())]
    temperature =   [temp['mean'] for temp in list(temperature_result.get_points())]
    print(activations)

    # reg_params = beta_one(temperature, activations)


    demo_temp = [10,11,12,13,14,15,16,17,18,19]
    demo_act = [20,21,22,23,24,25,26,27,28,29]
    reg_params = beta_one(demo_temp, demo_act)

    time.time() * 1000

    print(time.strftime('%MS', t))
    t = 8.64 * 10**7

    day = []

     for i in range(len(data.list)):
         day[i] = [ item.main.dt.temp for item in data.list if data.list.dt < data.list.dt + 8.64 * 10**7 ]
         day.append([])



    est_activations = regress(30, reg_params)




    # temp = r.json()['main']['temp'] - conversion_val


    # TODO: use better structure
    # client = InfluxDBClient(host='localhost', port=8086)
    # client.switch_database('humidity')
    # json_body = [
    #     {
    #         "measurement": "temperature",
    #         "fields": {
    #             "value": temp
    #         }
    #     },
    #
    # ]
    #
    # was_successfull = client.write_points(json_body)


    return str(est_activations)
