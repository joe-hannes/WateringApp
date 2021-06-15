from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from WateringApp.WateringSystem import WateringSystem

from WateringApp.extensions import db, metadata

from WateringApp.config import SQLALCHEMY_DATABASE_URI

wsys = WateringSystem()

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)
