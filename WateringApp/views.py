
from flask_user import login_required
from flask import Flask, render_template, Blueprint


from .Models import Widget, Settings

from  WateringApp.Fachwerte.Humidity import Humidity

from WateringApp.materialien.SoilSensor import SoilSensor

import json as json2


import json


import WateringApp.WateringSystem as wsys

from WateringApp.config import SQLALCHEMY_DATABASE_URI

from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)

# import werkzeug





json = Blueprint('json', __name__)

test = Blueprint('test', __name__)



createTables = Blueprint('createTables', __name__)

initialCode = Blueprint('initialCode', __name__)

badReq = Blueprint('badReq', __name__)

assertionError = Blueprint('assertionError', __name__)

# TODO: wsys gets called every time an endpoint is accessed and needs to be made
# persistent








@initialCode.before_app_first_request
def activate_job():
    """initialize the loop"""
    wsys.wsys.start()
    with session as sess:
        sess.query(Widget).first().widget_state = False

    # if Widget.query.first().widget_state:
    #     wsys = WateringSystem()
    #     daemon = threading.Thread(name='startSystem',
    #                               target=startSystem, args=(wsys,))
    #     daemon.start()
    #     print("started wsys")
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



@json.route("/json")
def serveJSON():
    valArray = []
    average = 0
    activeAmount = 0
    results = {}
    channel = {}

    with session as sess:
        water_level = sess.query(Widget).first().current_water_level



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














@test.route('/test')
@login_required
def testSite():
    return render_template("test.html" )


@createTables.route('/create')
# @login_required
def testSite():
    db.create_all()
    with session as sess:
        widget = Widget(widget_state= False, activation_level= 65)
        sess.add(widget)
        sess.commit()
    return "created all tables!"

# @badReq.errorhandler(werkzeug.exceptions.NotFound)
# def handle_bad_request(e):
#     return 'not found!', 404

# @assertionError.errorhandler(werkzeug.exceptions)
# def handle_bad_request(e):
#     return 'Assertion error'
