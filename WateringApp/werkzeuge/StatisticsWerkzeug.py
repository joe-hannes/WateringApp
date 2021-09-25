
from flask import Flask, render_template, Blueprint
from flask_user import login_required

statistics = Blueprint('statistics', __name__)


@statistics.route("/statistics")
@login_required
def statistics_page():
    return render_template("statistics.html", view_name='Statistics')
