from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import MetaData

from sqlalchemy.ext.declarative import declarative_base

from WateringApp.config import INFLUXDB_URI, INFLUXDB_PORT

from influxdb import InfluxDBClient

metadata = MetaData()
Base = declarative_base(metadata=metadata)



db = SQLAlchemy(metadata=metadata)

client = InfluxDBClient(host=INFLUXDB_URI, port=INFLUXDB_PORT)
