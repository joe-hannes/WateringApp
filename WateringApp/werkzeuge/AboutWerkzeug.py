
from flask import Flask, render_template, Blueprint


about = Blueprint('about', __name__)


@about.route('/about')
def about_func():
    return render_template('about.html', view_name ='About')
