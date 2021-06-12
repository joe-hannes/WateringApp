
from flask_user import login_required
from flask import Flask, render_template, Blueprint, g, request

import threading

from .WateringSystem import WateringSystem, STOP

from .extensions import db

from .Models import Widget

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

wsys = WateringSystem()


def startSystem(wsys):
    # do everything else
    wsys.start()



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
    db_entry = Widget.query.first().widget_state
    print(str(db_entry))


    return str(db_entry)

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
        wsys.setState(False)

    else:

        # Set as a daemon so it will be killed once the main thread is dead.
        # daemon.setDaemon(True)
        # daemon.start()
        Widget.query.first().widget_stwate = True
        db.session.commit()
        wsys.setState(True)



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
        # print('activation_level: ' + str(activation_level))
        Widget.query.first().activation_level = request.form['data']
        db.session.commit()
        wsys.setActivationLevel(int(activation_level))



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
