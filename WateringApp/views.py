
from flask_user import login_required
from flask import Flask, render_template, Blueprint

from SoilSensor import SoilSensor


main = Blueprint('main', __name__)

json = Blueprint('json', __name__)

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
    values = SoilSensor().getHumidity(1)
    values = values.toJSONString()
    return values
