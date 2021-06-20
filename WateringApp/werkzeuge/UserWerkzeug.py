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
def update_user_ep():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            print('location: {}'.format(data))


            # TODO: handle case where we want to add an entry if no entry is already there
            with session as sess:
                sess.query(Settings).filter_by(id=1).update(data)
                # TODO: only update reservoir size
                sess.query(Widget).first().current_water_level = data['reservoir_size']
                wsys.wsys.update_consumption(data['consumption'])
                sess.commit()
            # Settings.query.first().reservoir_size = data['reservoirSize']
            # db.session.commit()
            # Settings.query.first().reservoir_warn_level = data['reservoirWarn']
            # db.session.commit()
    return 'updated Settings successfully'
