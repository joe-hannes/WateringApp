from flask_user import UserMixin

from .extensions import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

class Widget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    widget_state = db.Column(db.Boolean)
    activation_level = db.Column(db.Integer)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(50), nullable=True, server_default='N/V')
    reservoir_size = db.Column(db.Integer, nullable=True, server_default='-1')
    reservoir_warn_level = db.Column(db.Integer, nullable=True, server_default='-1')
