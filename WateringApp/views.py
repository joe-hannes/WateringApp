
from flask_user import login_required
from flask import Flask, render_template, Blueprint, g, request

import threading

from .WateringSystem import WateringSystem, STOP

from .extensions import db

from .Models import Widget, User, Settings

import sqlite3

from  WateringApp.Fachwerte.Humidity import Humidity

from .SoilSensor import SoilSensor
from .Motor import Motor

import json as json2

import time

import requests
import json

import werkzeug
import os

DATABASE = 'sqlite3.db'


main = Blueprint('main', __name__)

json = Blueprint('json', __name__)

test = Blueprint('test', __name__)

statistics = Blueprint('statistics', __name__)

settings = Blueprint('settings', __name__)

get_temperature = Blueprint('get_temperature', __name__)

update_user = Blueprint('update_user', __name__)

pump = Blueprint('pump', __name__)

autoMode = Blueprint('autoMode', __name__)

widgetState = Blueprint('widgetState', __name__)

createTables = Blueprint('createTables', __name__)

initialCode = Blueprint('initialCode', __name__)

badReq = Blueprint('badReq', __name__)

restartView = Blueprint('restartView', __name__)
updateActivationLevelView = Blueprint('updateActivationLevelView', __name__)

getActivationLevelView = Blueprint('getActivationLevelView', __name__)

assertionError = Blueprint('assertionError', __name__)



# TODO: wsys gets called every time an endpoint is accessed and needs to be made
# persistent
wsys = WateringSystem()





# @initialCode.before_app_first_request
# def activate_job():
#     if Widget.query.first().widget_state:
#         wsys = WateringSystem()
#         daemon = threading.Thread(name='startSystem',
#                                   target=startSystem, args=(wsys,))
#         daemon.start()
#         print("started wsys")
    # def run_job():
    #     not_started = True
    #     while not_started:
    #         try:
    #             if g._database.Widget.query.first().widget_state == True:
    #                 wsys = WateringSystem()
    #                 wsys.start()
    #                 print("started wsys")
    #                 not_started = False
    #         except:
    #             print("couldnt query db")
    #
    #
    #
    #
    #         time.sleep(3)
    #
    # thread = threading.Thread(target=run_job)
    # thread.start()

@main.route("/")
@login_required
def index():
    # values = SoilSensor().getHumidity(0)
    values = SoilSensor(1).getHumidity()
    # print("values:" + str(values.getValue()))
    values = values.inPercent()
    state = Widget.query.first().widget_state
    return render_template("index.html", data = state)

@json.route("/json")
def serveJSON():
    valArray = []
    average = 0
    activeAmount = 0
    results = {}
    channel = {}
    for i in range(SoilSensor.AMOUNT + 1):
        sensor = SoilSensor(i)
        humidity = sensor.getHumidity()
        json = humidity.toJSONString()
        if humidity.getValue() > 100:
            average += humidity.getValue()
            activeAmount += 1
            json["active"] = 1
        else:
            json["active"] = 0
            json["value"] = "-"
            json["percent"] = "-"
            json["percentString"] = "-"
        json["channel"] = i
        valArray.append(json)

    # print('activeAmount: ' + str(activeAmount))
    average = round(average / activeAmount)
    avg_humidity = Humidity.intToHumidity(average)
    channel["channel"] = valArray
    results["results"] = channel
    channel["average"] = avg_humidity.toJSONString()

    # print(results)
    # valArray.append("\"average\" :" + "\"" + str(average) + "\"")

    # print(valArray)
    return json2.dumps(results)
        # return values

@statistics.route("/statistics")
@login_required
def statistics_page():
    return render_template("statistics.html")



@settings.route("/settings")
@login_required
def settings_page():
    # settings = User.query.filter_by('username')
    return render_template("settings.html", data = settings)

@pump.route("/activatePump")
@login_required
def activatePump():
    motor = Motor()
    motor.continuous("right")
    motor.stop()
    return "Successfully started Motor"


@widgetState.route("/getWidgetState")
@login_required
def getWidgetState():
    # db = getattr(g, '_database', None)
    # if db is None:
    #     db = g._database = sqlite3.connect(DATABASE)
    #
    # cur = db.cursor().execute("SELECT * FROM Widget")
    #
    # rows = cur.fetchall()
    #
    # for row in rows:
    #     print(row)

    # TODO: somethings not working
    db_entry = Widget.query.first().widget_state
    wsys.set_state(db_entry)

    return 'retrieved widget state: {}'.format(db_entry)


@update_user.route("/updateUser", methods=['POST'])
@login_required
def update_user_ep():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            print('location: {}'.format(data))
            db.session.query(Settings).filter_by(id=1).update(data)
            db.session.commit()
            # Settings.query.first().reservoir_size = data['reservoirSize']
            # db.session.commit()
            # Settings.query.first().reservoir_warn_level = data['reservoirWarn']
            # db.session.commit()
    return 'updated Settings successfully'


@get_temperature.route("/getTemperature", methods=['POST'])
@login_required
def get_temperature_ep():
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    location = Settings.query.first().location
    api_key = 'aec85d0e0f52e5c5e509ff4142a3a822'
    concat_url = base_url + '?q=' + location + '&appid=' + api_key
    conversion_val = 273.15

    print('concat_url: {}'.format(concat_url))

    r = requests.get(concat_url)

    print('response: {}'.format(r.text))
    # temperature = r.main.temp - convertion_val

    return str(r.json()['main']['temp'] - conversion_val)

@autoMode.route("/toggleAutoMode")
@login_required
def toggleAutoMode():
    # db = getattr(g, '_database', None)
    # if db is None:
    #     db = g._database = sqlite3.connect(DATABASE)
    #
    # cur = db.cursor().execute("SELECT * FROM Widget")
    #
    # rows = cur.fetchall()
    #
    # for row in rows:
    #     print(row)



    # wsys.setS


    if Widget.query.first().widget_state:

        Widget.query.first().widget_state = False
        db.session.commit()
        STOP = True
        # daemon.stop = False
        wsys.set_state(False)

    else:

        # Set as a daemon so it will be killed once the main thread is dead.
        # daemon.setDaemon(True)
        # daemon.start()
        Widget.query.first().widget_state = True
        db.session.commit()
        wsys.set_state(True)



    return str(Widget.query.first().widget_state)

@restartView.route("/restart")
@login_required
def restart():
    os.system('sudo reboot now')
    return 'restarting'

@updateActivationLevelView.route("/updateActivationLevel", methods=['POST'])
@login_required
def updateActivationLevel():
    if request.method == "POST":
        activation_level = request.form['data']
        print('activation_level: ' + str(activation_level))
        Widget.query.first().activation_level = request.form['data']
        db.session.commit()
        wsys.set_activationLevel(int(activation_level))



    return 'updated Activation Level'

@getActivationLevelView.route("/getActivationLevel", methods=['POST'])
@login_required
def getActivationLevel():
    if request.method == "POST":
        value = Widget.query.first().activation_level



    return str(value)

@test.route('/test')
@login_required
def testSite():
    return render_template("test.html" )


@createTables.route('/create')
# @login_required
def testSite():
    db.create_all()
    widget = Widget(widget_state= False, activation_level= 65)
    db.session.add(widget)
    db.session.commit()
    return "created all tables!"

# @badReq.errorhandler(werkzeug.exceptions.NotFound)
# def handle_bad_request(e):
#     return 'not found!', 404

# @assertionError.errorhandler(werkzeug.exceptions)
# def handle_bad_request(e):
#     return 'Assertion error'
