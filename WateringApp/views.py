
import json

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask_user import login_required
from flask import Flask, render_template, Blueprint

import WateringApp.WateringSystem as wsys
from WateringApp.Fachwerte.Humidity import Humidity
from WateringApp.materialien.SoilSensor import SoilSensor
from WateringApp.config import SQLALCHEMY_DATABASE_URI
from WateringApp.Models import Widget, Settings
from WateringApp.extensions import db
from WateringApp.werkzeuge.shared import menu_items



engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)

json = Blueprint('json', __name__)

test = Blueprint('test', __name__)



createTables = Blueprint('createTables', __name__)

initialCode = Blueprint('initialCode', __name__)

badReq = Blueprint('badReq', __name__)

assertionError = Blueprint('assertionError', __name__)


@initialCode.before_app_first_request
def activate_job():
    """initialize database tables (create and add an entry)
    if they are not yet initialized (first start)
    initilize state of the system when restarting """
    wsys.wsys.start()

    db.create_all()



    with session as sess:
        # make new table entry if table has none
        if sess.query(Settings).first() == None:
            sess.query(Settings).update(id = 1)
        if sess.query(Widget).first() == None:
            sess.query(Widget).first().widget_state = False
        sess.commit()

        # query widget state and initialize System accordingly
        water_level = sess.query(Widget).first().current_water_level
        activation_level = sess.query(Settings).first().activation_level

    wsys.wsys.set_state(False)
    wsys.wsys.set_activation_level(activation_level)
    wsys.wsys.set_water_level(water_level)



@test.route('/test')
@login_required
def testSite():
    return render_template("test.html", menu_items = menu_items, view_name='Test')
