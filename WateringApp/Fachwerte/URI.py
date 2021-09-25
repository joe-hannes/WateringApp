class URI():
    """A class representing a Database URI

    A Database Uri has the following parts:
    :db_name:     default: None        - name of the DB
    :base_uri:    default: "localhost" - The base location of the db in the network
    :db_port:     default: None        - The port used by the db service
    :db_username: default: None        - the name of the db username
    :db_password: default: None        - the password for the db user
    :db_type:     default: "sqlite"    - the type of the db

    If db_type == "influx" and port is not set manually defaults db_port to 8086
    If db_type == "mysql+pymysql" and port is not set manually defaults db_port to 3306
    """

    def __init__(self, db_name= None, base_uri="192.168.178.27", db_port = None, db_username=None, db_password=None, db_type="sqlite"):
        self.__base_uri = base_uri
        self.__db_name = db_name
        self.__db_username = db_username
        self.__db_password = db_password

        # self.db_type = 'mysql+pymysql'
        self.__db_type = db_type

        if db_type != "influx" and db_type != "mysql+pymysql":
            self.__db_port = db_port
        elif db_port == None and db_type == "influx":
            self.__db_port = 8086
        elif base_uri == None and db_type == "mysql+pymysql":
            self.__db_port = 3306





    def set_username(self, username):
        self.__db_username = username

    def get_username(self):
        return self.__db_username

    def set_base_uri(self, base_uri):
        self.__base_uri = base_uri

    def get_base_uri(self):
        return self.__base_uri

    def get_db_port(self):
        return self.__db_port

    def set_db_port(self, db_port):
        self.__db_port = db_port

    def set_db_name(self, name):
        self.__db_name = name

    def get_db_name(self):
        return self.__db_name

    def set_password(self, password):
        self.__db_password = password

    def get_password(self):
        return self.__db_password

    def get_uri_string(self):
        if (self.__db_type == "sqlite"):
            return self.__db_type +':///' + \
                self.__db_name + '.db'
        elif (self.__db_type == "influx"):
            return self.__base_uri
        else:
            return self.__db_type + '://' + \
                self.__db_username + ':' + \
                self.__db_password + '@' + \
                self.__base_uri + ':' + \
                self.__db_port + '/' + \
                self.__db_name
