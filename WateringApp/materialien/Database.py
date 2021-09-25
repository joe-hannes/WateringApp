
from WateringApp.Fachwerte.URI import URI
from sqlalchemy_utils import create_database, database_exists
from influxdb import InfluxDBClient
from abc import ABC, abstractmethod
from WateringApp.config import SQLALCHEMY_DATABASE_URI


class Database(ABC):
    """ Represents a BaseDatabase"""
    def __init__(self, uri):
        self.__uri = uri

    @abstractmethod
    def add_database(self):
        pass

class InfluxDBDatabase(Database):
    """represents a InfluxDB database"""
    def __init__(self, uri):
        self.__uri = uri
        self.__client = InfluxDBClient(
            host = self.__uri.get_uri_string(),
            port = self.__uri.get_db_port()
        )

    def add_database(self, db_name):
        self.__client.create_database(db_name)

class SQLDatabase(Database):
    """represents a MariaDB database"""
    def __init__(self, uri):
        self.__uri = uri

    def add_database(self):
        SQLALCHEMY_DATABASE_URI = self.__uri.get_uri_string()

        if not database_exists(SQLALCHEMY_DATABASE_URI):
            create_database(SQLALCHEMY_DATABASE_URI)
