from flask import Flask, Blueprint


from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy

import time

# import threading

from .extensions import db

from .views import  json, test,  createTables, initialCode, badReq, assertionError

from WateringApp.werkzeuge.WidgetWerkzeug import pump, main, widgetState, autoMode, updateActivationLevelView, getActivationLevelView, json

from WateringApp.werkzeuge.SettingsWerkzeug import settings, restartView, reset_water_level

from WateringApp.werkzeuge.StatisticsWerkzeug import statistics

from WateringApp.werkzeuge.UserWerkzeug import  user_view, update_user

from .Models import User, Widget



from flask_fontawesome import FontAwesome



def createApp(config_file= 'config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    user_manager = UserManager(app, db, User)


    fa = FontAwesome(app)

    app.register_blueprint(main)
    app.register_blueprint(json)
    app.register_blueprint(pump)
    app.register_blueprint(test)
    app.register_blueprint(statistics)
    app.register_blueprint(settings)
    app.register_blueprint(user_view)
    app.register_blueprint(update_user)
    app.register_blueprint(autoMode)
    app.register_blueprint(createTables)
    app.register_blueprint(widgetState)
    app.register_blueprint(initialCode)
    app.register_blueprint(badReq)
    app.register_blueprint(restartView)
    app.register_blueprint(updateActivationLevelView)
    app.register_blueprint(getActivationLevelView)
    app.register_blueprint(reset_water_level)

    # app.register_blueprint(assertionError)

    db.init_app(app)




    # app.run(threaded=True, host="0.0.0.0", port="8080")

    return app
