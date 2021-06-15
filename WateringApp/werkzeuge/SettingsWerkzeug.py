from flask import Flask, render_template, Blueprint
from flask_user import login_required
import os

settings = Blueprint('settings', __name__)
restartView = Blueprint('restartView', __name__)


@settings.route("/settings")
@login_required
def settings_page():
    # settings = User.query.filter_by('username')
    return render_template("settings.html", data = settings)


@restartView.route("/restart")
@login_required
def restart():
    os.system('sudo reboot now')
    return 'restarting'
