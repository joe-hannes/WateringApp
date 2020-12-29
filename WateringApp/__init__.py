from flask import Flask, Blueprint

from flask_user import UserManager
from flask_sqlalchemy import SQLAlchemy

from .extensions import db

from .views import main, json

from .User import User




def createApp(config_file= 'config.py'):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    user_manager = UserManager(app, db, User)

    app.register_blueprint(main)
    app.register_blueprint(json)

    db.init_app(app)

    # app.run(threaded=True, host="0.0.0.0", port="8080")

    return app




if __name__ == "__main__":
    # Start the server in a new thread

    daemon = threading.Thread(name='startServer',
                              target=startServer)

    # Set as a daemon so it will be killed once the main thread is dead.
    daemon.setDaemon(True)
    daemon.start()

    # do everything else
    wsys = WateringSystem()
    wsys.start()
