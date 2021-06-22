
from flask import Flask, render_template, Blueprint
from flask_user import login_required
from WateringApp.werkzeuge.shared import menu_items
statistics = Blueprint('statistics', __name__)


@statistics.route("/statistics")
@login_required
def statistics_page():
    return render_template("statistics.html", menu_items=menu_items, view_name='Statistics')
