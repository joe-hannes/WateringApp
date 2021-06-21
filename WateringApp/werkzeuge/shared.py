
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from WateringApp.extensions import db, metadata

from WateringApp.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)
