
import math
import requests
import time
from requests.exceptions import ConnectionError

from statistics import StatisticsError

from flask_user import login_required
from flask import Flask, render_template, Blueprint
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from influxdb import InfluxDBClient

from WateringApp.config import API_KEY, DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD, SQLALCHEMY_DATABASE_URI
from WateringApp.linear_regression import calc_params, regress
from WateringApp.Models import Settings, Widget
from WateringApp.Fachwerte.URI import URI

home = Blueprint('home', __name__)
index = Blueprint('index', __name__)

# uri = URI(DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD)
# uri = uri.get_uri_string()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)

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

        print('temperature: {}'.format(temperature))

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


    except (ConnectionError, ZeroDivisionError, StatisticsError, TypeError, AssertionError)  as e:
        print("""
        \x1b[33m Cant use linear regression for refill time calculation because
        there are either too few datapoints on no internet connection.
        Proceeding by using extrapolation method to estimation refilltime instead \033[0m
        """)

        with session as sess:
            last_activation = sess.query(Widget).first().last_activation

        interval = time.time() - last_activation

        refill_time = max_pump_activations * (interval / 360 / 24)



    # print('refill_time: {} days'.format(refill_time))

    return round(refill_time, 2)



@index.route('/')
@login_required
def redirect_home():
    return render_template("home.html", view_name='Home')



@home.route('/home')
@login_required
def home_func():
    refill_time = calculate_refill()

    return render_template(
        "home.html",
        view_name='Home',
        refill_time = refill_time)
