
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from WateringApp.Fachwerte.URI import URI
from WateringApp.config import DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD, SQLALCHEMY_DATABASE_URI


from WateringApp.extensions import db, metadata

# uri = URI(DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD)
# uri = uri.get_uri_string()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
session = Session(engine)
