from flask_user import login_required
from flask import Flask, render_template, Blueprint, g, request

from WateringApp.werkzeuge.shared import SQLALCHEMY_DATABASE_URI

from WateringApp.Models import Settings, Widget
from WateringApp.materialien.SoilSensor import SoilSensor
from WateringApp.materialien.Motor import Motor

from  WateringApp.Fachwerte.Humidity import Humidity
import json as json2

import WateringApp.WateringSystem as wsys


from sqlalchemy import create_engine
from sqlalchemy.orm import Session
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)



# import WateringApp.tests.modulea_test as tests


import time


pump = Blueprint('pump', __name__)
widgetState = Blueprint('widgetState', __name__)
autoMode = Blueprint('autoMode', __name__)
main = Blueprint('main', __name__)
updateActivationLevelView = Blueprint('updateActivationLevelView', __name__)
getActivationLevelView = Blueprint('getActivationLevelView', __name__)
json = Blueprint('json', __name__)

@main.route("/")
@login_required
def index():
    # TODO: for now initialize last_activation and current_water_level when the page is opened
    # should be only initialized once when the program starts in the future

    # values = SoilSensor(1).getHumidity()
    # values = values.inPercent()
    return render_template("index.html")

@pump.route("/activatePump")
@login_required
def activatePump():
    # TODO: update water level
    motor = Motor()
    motor.continuous("right")
    motor.stop()
    with session as sess:
        wsys.wsys.update_water_level(sess)



    return "Successfully started Motor"


@widgetState.route("/getWidgetState")
@login_required
def getWidgetState():
    with session as sess:
        widget_state = sess.query(Widget).first().widget_state

    wsys.wsys.set_state(widget_state)

    return str(widget_state)


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

    with session as sess:
        if sess.query(Widget).first().widget_state:

            sess.query(Widget).first().widget_state = False
            sess.commit()
            STOP = True
            # daemon.stop = False
            wsys.wsys.set_state(False)

        else:
            sess.query(Widget).first().widget_state = True
            sess.commit()
            wsys.wsys.set_state(True)

        result = str(sess.query(Widget).first().widget_state)

    return result


@updateActivationLevelView.route("/updateActivationLevel", methods=['POST'])
@login_required
def updateActivationLevel():
    if request.method == "POST":
        activation_level = request.form['data']
        # print('activation_level: ' + str(activation_level))
        with session as sess:
            sess.query(Settings).first().activation_level = request.form['data']
            sess.commit()
        wsys.wsys.set_activation_level(int(activation_level))
    return 'updated Activation Level'

@getActivationLevelView.route("/getActivationLevel", methods=['POST'])
@login_required
def getActivationLevel():
    if request.method == "POST":
        with session as sess:
            value = sess.query(Settings).first().activation_level



    return str(value)

@json.route("/json")
def serveJSON():
    valArray = []
    average = 0
    activeAmount = 0
    results = {}
    channel = {}


    water_level = wsys.wsys.get_water_level()



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

    # TODO:  do this calculation in fachwerte and make reservoir size (500) dynamic
    results['results']['water_level'] =  water_level *  (60/500)
    channel["average"] = avg_humidity.toJSONString()

    # print(results)
    # valArray.append("\"average\" :" + "\"" + str(average) + "\"")

    # print(valArray)
    return json2.dumps(results)
        # return values
