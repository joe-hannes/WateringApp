import time

from flask import Flask, Blueprint
from flask_fontawesome import FontAwesome
from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from WateringApp.werkzeuge.HomeWerkzeug import  home, index
from WateringApp.werkzeuge.WidgetWerkzeug import widget, widget_no_auth, activate_pump, get_widget_state, toggle_auto_mode, update_activation_level, get_activation_level, get_json, socketio
from WateringApp.werkzeuge.SettingsWerkzeug import settings, restartView, reset_water_level
from WateringApp.werkzeuge.StatisticsWerkzeug import statistics
from WateringApp.werkzeuge.UserWerkzeug import  user_view, update_user
from WateringApp.werkzeuge.AboutWerkzeug import about

from .Models import User, Widget
from .extensions import db
from .views import  json, createTables, initialCode, badReq, assertionError




def createApp(config_file= 'config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    user_manager = UserManager(app, db, User)

    fa = FontAwesome(app)

    app.register_blueprint(initialCode)

    app.register_blueprint(home)
    app.register_blueprint(index)

    app.register_blueprint(widget)
    app.register_blueprint(widget_no_auth)
    app.register_blueprint(get_json)
    app.register_blueprint(activate_pump)
    app.register_blueprint(get_widget_state)
    app.register_blueprint(toggle_auto_mode)


    app.register_blueprint(statistics)

    app.register_blueprint(user_view)
    app.register_blueprint(update_user)

    app.register_blueprint(settings)
    app.register_blueprint(restartView)
    app.register_blueprint(update_activation_level)
    app.register_blueprint(get_activation_level)
    app.register_blueprint(reset_water_level)

    app.register_blueprint(about)


    app.register_blueprint(createTables)
    app.register_blueprint(badReq)

    # app.register_blueprint(assertionError)

    db.init_app(app)
    socketio.init_app(app)




    # app.run(threaded=True, host="0.0.0.0", port="8080")

    return app
