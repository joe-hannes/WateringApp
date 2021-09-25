import time
import json as json2

from flask_user import login_required
from flask import Flask, render_template, Blueprint, g, request
from flask_socketio import SocketIO, send
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from WateringApp.Models import Settings, Widget
from WateringApp.materialien.SoilSensor import SoilSensor
from WateringApp.materialien.Motor import Motor
from WateringApp.Fachwerte.Humidity import Humidity
import WateringApp.WateringSystem as wsys
from WateringApp.config import DB_BASE_URI, SQLALCHEMY_DATABASE_URI



socketio = SocketIO()
# uri = URI(DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD)
# uri = uri.get_uri_string()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)



widget = Blueprint('widget', __name__)
widget_no_auth = Blueprint('widget_no_auth', __name__)
activate_pump = Blueprint('activate_pump', __name__)
get_widget_state = Blueprint('get_widget_state', __name__)
toggle_auto_mode = Blueprint('toggle_auto_mode', __name__)

update_activation_level = Blueprint('update_activation_level', __name__)
get_activation_level = Blueprint('get_activation_level', __name__)
get_json = Blueprint('get_json', __name__)


@socketio.on('message')
def message_func(msg):

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = Session(engine)


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
        with session as sess:
            reservoir_size = sess.query(Settings).first().reservoir_size

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

    # TODO:  do this calculation in fachwerte
    results['results']['water_level'] =  water_level *  (60/reservoir_size)
    channel["average"] = avg_humidity.toJSONString()

    send(json2.dumps(results), broadcast=True)

    # print(msg)

@widget.route("/widget/<sensor_nr>")
@login_required
def widget_func(sensor_nr):
    # TODO: for now initialize last_activation and current_water_level when the page is opened
    # should be only initialized once when the program starts in the future

    # values = SoilSensor(1).getHumidity()
    # values = values.inPercent()
    return render_template("widget.html", sensor_nr=sensor_nr)


@widget_no_auth.route("/widget_no_auth/<sensor_nr>")
def widget_no_auth_func(sensor_nr):
    return render_template("widget_no_auth.html", sensor_nr=sensor_nr)

@activate_pump.route("/activatePump")
@login_required
def activate_pump_func():
    # TODO: update water level
    motor = Motor()
    motor.continuous("right")
    motor.stop()
    with session as sess:
        wsys.wsys.update_water_level(sess)

    return "Successfully started Motor"


@get_widget_state.route("/getWidgetState")
def get_widget_state_func():
    with session as sess:
        widget_state = sess.query(Widget).first().widget_state

    wsys.wsys.set_state(widget_state)

    return str(widget_state)


@toggle_auto_mode.route("/toggleAutoMode")
@login_required
def toggle_auto_mode_func():

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = Session(engine)

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


@update_activation_level.route("/updateActivationLevel", methods=['POST'])
@login_required
def update_activation_level_func():
    if request.method == "POST":
        activation_level = request.form['data']
        # print('activation_level: ' + str(activation_level))
        with session as sess:
            sess.query(Settings).first().activation_level = request.form['data']
            sess.commit()
        wsys.wsys.set_activation_level(int(activation_level))
    return 'updated Activation Level'

@get_activation_level.route("/getActivationLevel", methods=['POST'])
@login_required
def getActivationLevel():
    if request.method == "POST":
        with session as sess:
            value = sess.query(Settings).first().activation_level



    return str(value)

@get_json.route("/json")
def get_json_func():

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    session = Session(engine)


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
        with session as sess:
            reservoir_size = sess.query(Settings).first().reservoir_size

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

    # TODO:  do this calculation in fachwerte
    results['results']['water_level'] =  water_level *  (60/reservoir_size)
    channel["average"] = avg_humidity.toJSONString()

    # print(results)
    # valArray.append("\"average\" :" + "\"" + str(average) + "\"")

    # print(valArray)
    return json2.dumps(results)
        # return values
