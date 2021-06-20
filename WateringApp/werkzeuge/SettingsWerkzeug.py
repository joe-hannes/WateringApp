from flask import Flask, render_template, Blueprint
from flask_user import login_required
import os
import requests

from influxdb import InfluxDBClient

from WateringApp.werkzeuge.shared import session
from WateringApp.Models import Settings




from WateringApp.linear_regression import beta_one, regress

settings = Blueprint('settings', __name__)
restartView = Blueprint('restartView', __name__)

get_temperature = Blueprint('get_temperature', __name__)


@settings.route("/settings")
@login_required
def settings_page():
    # settings = User.query.filter_by('username')
    return render_template("settings.html", data = settings)


@restartView.route("/restart")
@login_required
def restart():
    os.system('sudo reboot now')
    return 'restarting'


@get_temperature.route("/getTemperature", methods=['POST'])
@login_required
def get_temperature_ep():

    with session as sess:
        location = sess.query(Settings).first().location

    base_url = 'http://api.openweathermap.org/data/2.5/'

    type = ['weather', 'history', 'forecast']

    country_code = ',DEU'

    api_key = 'aec85d0e0f52e5c5e509ff4142a3a822'
    concat_url = base_url + type[2] + '?q=' + location + country_code + '&appid=' + api_key
    conversion_val = 273.15

    print('concat_url: {}'.format(concat_url))

    r = requests.get(concat_url)

    print('response: {}'.format(r.text))
    # temperature = r.main.temp - convertion_val

    data = r.json()['list']

    print(f'data_list length: {len(data)}')



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
