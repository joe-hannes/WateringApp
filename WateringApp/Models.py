from flask_user import UserMixin

from sqlalchemy import Column, Integer, String, Boolean

from .extensions import db, Base



class Widget(Base):
    __tablename__ = 'Widget'

    id = Column(Integer, primary_key=True)
    widget_state = Column(Boolean)

    current_water_level = Column(Integer)
    last_activation = Column(Integer)



class Settings(Base):
    __tablename__ = 'Settings'

    id = Column(Integer, primary_key=True)
    location = Column(String(50), nullable=True, server_default='N/V')
    reservoir_size = Column(Integer, nullable=True, server_default='-1')
    consumption = Column(Integer, nullable=True, server_default='N/V')
    reservoir_warn_level = Column(Integer, nullable=True, server_default='-1')
    activation_level = Column(Integer)


    def __init__(self, description):
        self.description = description


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')
