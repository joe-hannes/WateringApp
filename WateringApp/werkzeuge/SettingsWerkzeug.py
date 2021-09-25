import os
import requests
from requests.exceptions import ConnectionError
import time
import math
from statistics import StatisticsError


from flask import Flask, render_template, Blueprint
from flask_user import login_required
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

import WateringApp.WateringSystem as wsys
from WateringApp.config import API_KEY, SQLALCHEMY_DATABASE_URI, INFLUXDB_PORT
from WateringApp.Models import Settings, Widget
from WateringApp.forms.settings_form import SettingsForm
from WateringApp.linear_regression import calc_params, regress
# from WateringApp.config import DB_NAME, DB_PASSWORD, DB_USERNAME, DB_BASE_URI
from WateringApp.materialien.Database import SQLDatabase, InfluxDBDatabase
from WateringApp.Fachwerte.URI import URI

#
# uri = URI(DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD)
# uri = uri.get_uri_string()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)


settings = Blueprint('settings', __name__)
restartView = Blueprint('restartView', __name__)
reset_water_level = Blueprint('reset_water_level', __name__)



# TODO: statisticsError needs at least 1 datapoint; update pump activation level
@settings.route("/settings", methods= ['GET', 'POST'])
@login_required
def settings_page():
    """view: displays the settingspage with the according values"""
    form = SettingsForm()

    # refill_time = -1

    if form.validate_on_submit():
        # when a form is submitted update database entries and set internal system
        # state
        # print('form submitted')
        with session as sess:
            if form.location.data != "":
                sess.query(Settings).first().location = form.location.data
            if form.reservoir_size.data != "":
                sess.query(Settings).first().reservoir_size = form.reservoir_size.data
            if form.consumption.data != "":
                sess.query(Settings).first().consumption = form.consumption.data
            if form.reservoir_warn_level.data != "":
                sess.query(Settings).first().reservoir_warn_level = form.reservoir_warn_level.data
            if form.activation_level.data != "":
                sess.query(Settings).first().activation_level = form.activation_level.data
                wsys.wsys.set_activation_level(form.activation_level.data)
            if form.api_key.data != "":
                sess.query(Settings).first().api_key = form.api_key.data

            reservoir_size = sess.query(Settings).first().reservoir_size

            if reservoir_size != form.reservoir_size.data:
                sess.query(Widget).first().current_water_level = reservoir_size

            sess.commit()


            # OLD CODE FOR OUTSOURCING SQL TABLES TO EXTERNAL SOURCE

            # print("db_name: {}".format(form.db_name.data))
            # if form.db_name.data != "" and \
            #     form.db_name.data != "" and \
            #     form.db_username.data != "" and \
            #     form.db_password.data != "":
            #     print("created new database")
            #     uri = URI(
            #         base_uri = form.db_uri.data,
            #         db_name = form.db_name.data,
            #         db_username = form.db_username.data,
            #         db_password = form.db_password.data,
            #         db_type = "mysql+pymysql"
            #     )
            #
            #     with session as sess:
            #         sess.query(Settings).first().use_external_db = True
            #         sess.commit()



            # SQLALCHEMY_DATABASE_URI = uri.get_uri_string()

            # print(SQLALCHEMY_DATABASE_URI)
            # db = SQLDatabase(uri)
            # db.add_database()

            # CREATE INFLUX DB DATABASES

            print("db_name: {}".format(form.db_name.data))
            if form.db_uri.data != "" and \
                form.db_uri.data != "":
                print("created new database")
                uri = URI(
                    base_uri = form.db_uri.data,
                    db_type = "influx"
                )

            db = InfluxDBDatabase(uri)
            db.add_database('humidity')
            db.add_database('activation')


    with session as sess:
        settings = sess.query(Settings).first()
        # print('settings: {}'.format(settings))


    return render_template(
        "settings.html",
        form = form,
        settings = settings
    )


@restartView.route("/restart")
@login_required
def restart():
    """restart the machine"""
    os.system('sudo reboot now')
    return 'restarting'


@reset_water_level.route("/reset_water_level", methods=['GET', 'POST'])
@login_required
def reset_water_level_func():
    """endpoint:
    update the water_level in the database and sets the internal System instance variable"""

    # TODO: validate input
    with session as sess:
        reservoir_size = sess.query(Settings).first().reservoir_size
        sess.query(Widget).first().current_water_level = reservoir_size
        sess.query(Widget).first().widget_state = False
        sess.commit()

        wsys.wsys.set_state(False)

    return 'success'
