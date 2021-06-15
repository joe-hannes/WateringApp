from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(metadata=metadata)

db = SQLAlchemy(metadata=metadata)
