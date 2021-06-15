from flask_user import login_required
from flask import Flask, render_template, Blueprint, g, request



from WateringApp.werkzeuge.shared import wsys, session
from WateringApp.Models import Settings, Widget
from WateringApp.materialien.SoilSensor import SoilSensor
from WateringApp.materialien.Motor import Motor


import time


pump = Blueprint('pump', __name__)
widgetState = Blueprint('widgetState', __name__)
autoMode = Blueprint('autoMode', __name__)
main = Blueprint('main', __name__)
updateActivationLevelView = Blueprint('updateActivationLevelView', __name__)
getActivationLevelView = Blueprint('getActivationLevelView', __name__)




@main.route("/")
@login_required
def index():

    # TODO: for now initialize last_activation and current_water_level when the page is opened
    # should be only initialized once when the program starts in the future
    with session as sess:
        sess.query(Widget).first().last_activation = time.time()
        water_level = sess.query(Settings).first().reservoir_size
        sess.query(Widget).first().current_water_level = water_level
        sess.commit()
        consumption = sess.query(Settings).first().consumption
        state = sess.query(Widget).first().widget_state

    # values = SoilSensor().getHumidity(0)
    values = SoilSensor(1).getHumidity()
    # print("values:" + str(values.getValue()))
    values = values.inPercent()
    return render_template("index.html", data = state)

@pump.route("/activatePump")
@login_required
def activatePump():
    print('calculated time until refill: {} hours'.format(wsys.calculate_refill(time.time())/360))
    motor = Motor()
    motor.continuous("right")
    motor.stop()


    return "Successfully started Motor"


@widgetState.route("/getWidgetState")
@login_required
def getWidgetState():
    # db = getattr(g, '_database', None)
    # if db is None:
    #     db = g._database = sqlite3.connect(DATABASE)
    #
    # cur = db.cursor().execute("SELECT * FROM Widget")
    #
    # rows = cur.fetchall()
    #
    # for row in rows:
    #     print(row)

    # TODO: somethings not working
    with session as sess:
        db_entry = sess.query(Widget).first().widget_state

    wsys.set_state(db_entry)

    return 'retrieved widget state: {}'.format(db_entry)


@autoMode.route("/toggleAutoMode")
@login_required
def toggleAutoMode():
    # db = getattr(g, '_database', None)
    # if db is None:
    #     db = g._database = sqlite3.connect(DATABASE)
    #
    # cur = db.cursor().execute("SELECT * FROM Widget")
    #
    # rows = cur.fetchall()
    #
    # for row in rows:
    #     print(row)



    # wsys.setS

    with session as sess:
        if sess.query(Widget).first().widget_state:

            sess.query(Widget).first().widget_state = False
            sess.commit()
            STOP = True
            # daemon.stop = False
            wsys.set_state(False)

        else:

            # Set as a daemon so it will be killed once the main thread is dead.
            # daemon.setDaemon(True)
            # daemon.start()
            sess.query(Widget).first().widget_state = True
            sess.commit()
            wsys.set_state(True)

        result = str(sess.query(Widget).first().widget_state)

    return result


@updateActivationLevelView.route("/updateActivationLevel", methods=['POST'])
@login_required
def updateActivationLevel():
    if request.method == "POST":
        activation_level = request.form['data']
        print('activation_level: ' + str(activation_level))
        with session as sess:
            sess.query(Widget).first().activation_level = request.form['data']
            sess.commit()
        wsys.set_activationLevel(int(activation_level))
    return 'updated Activation Level'

@getActivationLevelView.route("/getActivationLevel", methods=['POST'])
@login_required
def getActivationLevel():
    if request.method == "POST":
        with session as sess:
            value = sess.query(Widget).first().activation_level



    return str(value)
