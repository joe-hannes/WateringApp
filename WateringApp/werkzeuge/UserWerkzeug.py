from flask import Flask, render_template, Blueprint, request
from flask_user import login_required

from WateringApp.werkzeuge.shared import session
from WateringApp.Models import Settings, Widget
import WateringApp.WateringSystem as wsys


update_user = Blueprint('update_user', __name__)
user_view = Blueprint('user_view', __name__)



@user_view.route("/user")
@login_required
def user():
    return render_template('user.html')

@update_user.route("/updateUser", methods=['POST'])
@login_required
def update_user_func():
    pass
    return 'updated user'
