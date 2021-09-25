from flask_user import UserMixin

from sqlalchemy import Column, Integer, String, Boolean

from .extensions import db, Base



class Widget(Base):
    __tablename__ = 'widget'

    id = Column(Integer, primary_key=True)
    widget_state = Column(Boolean)
    current_water_level = Column(Integer)
    last_activation = Column(Integer)
    before_last_activation = Column(Integer, server_default="NULL")



class Settings(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    location = Column(String(50), nullable=True)
    reservoir_size = Column(Integer, nullable=True)
    consumption = Column(Integer, nullable=True)
    reservoir_warn_level = Column(Integer, nullable=True)
    activation_level = Column(Integer)
    api_key = Column(String(50), nullable=True)
    external_db_uri = Column(String, nullable=True, server_default="NULL")
    # database = Column(String(50), nullable= True)



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
