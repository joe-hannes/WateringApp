import json

from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask_user import login_required
from flask import Flask, render_template, Blueprint

import WateringApp.WateringSystem as wsys
from WateringApp.Fachwerte.Humidity import Humidity
from WateringApp.materialien.SoilSensor import SoilSensor
from WateringApp.config import DB_NAME, SQLALCHEMY_DATABASE_URI
from WateringApp.Models import Widget, Settings
from WateringApp.extensions import db, client, Base
from WateringApp.Fachwerte.URI import URI
from WateringApp.materialien.Database import SQLDatabase, InfluxDBDatabase


uri = URI(db_name = DB_NAME)
uri_string = uri.get_uri_string()
engine = create_engine(uri_string)
session = Session(engine)


json = Blueprint('json', __name__)

test = Blueprint('test', __name__)



createTables = Blueprint('createTables', __name__)

initialCode = Blueprint('initialCode', __name__)

badReq = Blueprint('badReq', __name__)

assertionError = Blueprint('assertionError', __name__)


def create_influx_db(uri):
    influx_db = InfluxDBDatabase(uri)
    influx_db.add_database(db_name = "humidity")
    influx_db.add_database(db_name = "activation")



@initialCode.before_app_first_request
def activate_job():
    """initialize database tables (create and add an entry)
    if they are not yet initialized (first start)
    initilize state of the system when restarting """

    sql_db = SQLDatabase(uri)
    sql_db.add_database()

    db.create_all()
    Base.metadata.create_all(engine, checkfirst=True)


    # CREATE INITIAL TABLE ENTRIES FOR SETTINGS AND WIDGET TABLES
    settings = Settings(
        id=1,
        location="Hamburg",
        reservoir_size=500,
        consumption=50,
        reservoir_warn_level=1,
        activation_level=33,
        api_key="api_key"
    )

    widget = Widget(
        id=1,
        widget_state=False,
        current_water_level=0,
        last_activation=0
    )

    with session as sess:
        # ADD NEW TABLE ENTRY IF NONE EXIST YET
        if sess.query(Settings).first() == None:
            sess.add(settings)
        if sess.query(Widget).first() == None:
            sess.add(widget)
        sess.query(Widget).first().widget_state = False
        sess.commit()

        # INITIALIZE WIDGET PROPER
        water_level = sess.query(Widget).first().current_water_level
        activation_level = sess.query(Settings).first().activation_level
        print('initial w_level: {}'.format(water_level))
        print('initial a_level: {}'.format(activation_level))


    # CREATE INFLUX DB DATABASES

    with session as sess:
        external_db_uri = sess.query(Settings).first().external_db_uri
        if external_db_uri != "NULL":
            influx_uri = URI(db_type='influx', db_name=DB_NAME, base_uri=external_db_uri)
            create_influx_db(external_db_uri)
        else:
            influx_uri = URI(db_type='influx', db_name=DB_NAME)
            create_influx_db(influx_uri)


    # INITIALIZE WSYS

    wsys.wsys.set_state(False)
    wsys.wsys.set_activation_level(activation_level)
    wsys.wsys.set_water_level(water_level)
    wsys.wsys.start()
