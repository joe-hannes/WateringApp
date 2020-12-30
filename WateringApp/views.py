
from flask_user import login_required
from flask import Flask, render_template, Blueprint

from .SoilSensor import SoilSensor
from .Motor import Motor

import json as json2


main = Blueprint('main', __name__)

json = Blueprint('json', __name__)

test = Blueprint('test', __name__)
pump = Blueprint('pump', __name__)

@main.route("/")
@login_required
def index():
    # values = SoilSensor().getHumidity(0)
    values = SoilSensor().getHumidity(1)
    print("values:" + str(values.getValue()))
    values = values.inPercent()
    return render_template("index.html", data=values)

@json.route("/json")
def serveJSON():
    valArray = []

    for i in range(3):
        # i=1
        values = SoilSensor().getHumidity(i)
        values = values.toJSONString()
        valArray.append(values)
    # print(listString)
    return json2.dumps(valArray)
        # return values

@pump.route("/activatePump")
@login_required
def activatePump():
    motor = Motor()
    motor.continuous("right")
    return "Successfully started Motor"

@test.route('/test')
@login_required
def testSite():
    return render_template("test.html")
