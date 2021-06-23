
from flask_user import login_required
from flask import Flask, render_template, Blueprint


from .Models import Widget, Settings

from  WateringApp.Fachwerte.Humidity import Humidity

from WateringApp.materialien.SoilSensor import SoilSensor




import json


import WateringApp.WateringSystem as wsys

from WateringApp.config import SQLALCHEMY_DATABASE_URI

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from WateringApp.werkzeuge.shared import menu_items



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
        water_level = sess.query(Widget).first().current_water_level
        activation_level = sess.query(Settings).first().activation_level

        sess.commit()
    wsys.wsys.set_state(False)

    wsys.wsys.set_activation_level(activation_level)
    wsys.wsys.set_water_level(water_level)


    # TODO: initialize wsys object

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








@test.route('/test')
@login_required
def testSite():

    # menu_items.append()
    return render_template("test.html", menu_items = menu_items, view_name='Test')


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
