
from flask_user import login_required
from flask import Flask, render_template, Blueprint, g

import threading

from .WateringSystem import WateringSystem, STOP

from .extensions import db

from .Models import Widget

import sqlite3

from .SoilSensor import SoilSensor
from .Motor import Motor

import json as json2

import time

DATABASE = 'sqlite3.db'


main = Blueprint('main', __name__)

json = Blueprint('json', __name__)

test = Blueprint('test', __name__)

pump = Blueprint('pump', __name__)

autoMode = Blueprint('autoMode', __name__)

widgetState = Blueprint('widgetState', __name__)

createTables = Blueprint('createTables', __name__)


def startSystem(wsys):
    # do everything else
    wsys.start()

@main.route("/")
@login_required
def index():
    # values = SoilSensor().getHumidity(0)
    values = SoilSensor().getHumidity(1)
    print("values:" + str(values.getValue()))
    values = values.inPercent()
    state = Widget.query.first().widget_state
    return render_template("index.html", data= state)

@json.route("/json")
def serveJSON():
    valArray = []

    # for i in range(3):
        # i=1
    value = SoilSensor().getHumidity(1)
    value = value.toJSONString()
    valArray.append(value)

    time.sleep(0.1)

    # value = SoilSensor().getHumidity(2)
    # value = value.toJSONString()
    # valArray.append(value)
    #
    # time.sleep(0.5)
    #
    # value = SoilSensor().getHumidity(3)
    # value = value.toJSONString()
    # valArray.append(value)
    # print(listString)
    return json2.dumps(valArray)
        # return values

@pump.route("/activatePump")
@login_required
def activatePump():
    motor = Motor()
    motor.continuous("right")
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

    wsys = WateringSystem()
    daemon = threading.Thread(name='startSystem',
                              target=startSystem, args=(wsys,))


    if Widget.query.first().widget_state == True:


        Widget.query.first().widget_state = False
        db.session.commit()
        STOP = True
        daemon.stop = False

    else:


        # Set as a daemon so it will be killed once the main thread is dead.
        daemon.setDaemon(True)
        daemon.start()
        Widget.query.first().widget_state = True
        db.session.commit()



    return str(Widget.query.first().widget_state)

@test.route('/test')
@login_required
def testSite():
    return render_template("test.html")


@createTables.route('/create')
@login_required
def testSite():
    db.create_all()
    widget = Widget(widget_state= False)
    db.session.add(widget)
    db.session.commit()
    return "created all tables!"
