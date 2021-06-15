from flask import Flask, Blueprint

from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy

import time


import sqlite3
import threading

from .extensions import db

from .views import main, json, statistics, update_user, settings, get_temperature, pump, test, autoMode, createTables, widgetState, initialCode, badReq, assertionError, restartView, updateActivationLevelView, getActivationLevelView

from .Models import User, Widget

from .WateringSystem import WateringSystem

from flask_fontawesome import FontAwesome

# import requests


# def start_runner():
#     def start_loop():
#         not_started = True
#         while not_started:
#             print('In start loop')
#             try:
#                 r = requests.get('http://127.0.0.1:5000/')
#                 print(r)
#                 if r.status_code == 200:
#                     print('Server started, quiting start_loop')
#                     not_started = False
#                     wsys = WateringSystem()
#                     wsys.start()
#
#                 print(r.status_code)
#             except:
#                 print('Server not yet started')
#             time.sleep(2)
#
#     print('Started runner')
    # thread = threading.Thread(target=start_loop)
    # thread.start()
    # start_loop()

# def start_wsys():
#     conn = sqlite3.connect('sqlite3.db')
#     cursor = conn.cursor()
#     cursor.execute=
#     pass



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
    app.register_blueprint(get_temperature)
    app.register_blueprint(update_user)
    app.register_blueprint(autoMode)
    app.register_blueprint(createTables)
    app.register_blueprint(widgetState)
    app.register_blueprint(initialCode)
    app.register_blueprint(badReq)
    app.register_blueprint(restartView)
    app.register_blueprint(updateActivationLevelView)
    app.register_blueprint(getActivationLevelView)
    # app.register_blueprint(assertionError)

    db.init_app(app)

    # start_runner()


    # app.run(threaded=True, host="0.0.0.0", port="8080")

    return app




# if __name__ == "__main__":
#     # Start the server in a new thread
#
#     daemon = threading.Thread(name='startServer',
#                               target=startServer)
#
#     # Set as a daemon so it will be killed once the main thread is dead.
#     daemon.setDaemon(True)
#     daemon.start()
#     print('lulz')
    # do everything else
