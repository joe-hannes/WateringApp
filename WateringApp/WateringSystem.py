
import threading
import math
import requests
import time

from flask import g, Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import concurrent.futures as cf

from WateringApp.ADS1x15 import ADS1015
from WateringApp.Fachwerte.Humidity import Humidity
from WateringApp.Fachwerte.URI import URI
from WateringApp.materialien.SoilSensor import SoilSensor
from WateringApp.materialien.Motor import Motor
from WateringApp.Models import Widget, Settings
from WateringApp.extensions import db, client
from WateringApp.config import API_KEY, SQLALCHEMY_DATABASE_URI

# uri = URI(DB_BASE_URI, DB_NAME, DB_USERNAME, DB_PASSWORD)
# uri = uri.get_uri_string()
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind = engine)
session = Session()


STOP = False
class WateringSystem(object):

    def __init__(self):
        # logging.basicConfig()
        # logging.getLogger().setLevel(logging.WARN)

        self.__adc= ADS1015()
        self.__motor = Motor()
        self.__stop_flag = False
        self.__executor = cf.ThreadPoolExecutor()
        self.__last_activation = 0
        self.__errorMsg = "Error: something is wrong. Aborting program to prevent flooding living room"
        self.__ws_status = 0
        self.statusText = ""
        self.__humidity = Humidity(900)
        self.__sensor = (SoilSensor(1), SoilSensor(2), SoilSensor(3))
        self.__started = False

        self.__reservoir_size = 0
        self.__consumption = 0
        self.__water_level = 0
        self.__last_activation = 0

        self.__activation_level = 0
        self.__widget_state = False
        self.__start_time = time.time()

        self.__temp_map = []


    # def get_last_activation(self):
    #     with session as sess:
    #         self.__last_activation = sess.query(Widget).first().last_activation
    #     return self.__last_activation


    # def set_last_activation(self, last_activation):
    #     Widget.query().filter_by(id=1).last_activation = last_activation


    def update_water_level(self, sess):
        sess.query(Widget).first().current_water_level -= self.__consumption
        sess.commit()
        self.__water_level -= self.__consumption

    def update_last_activation(self, sess):
        self.__last_activation = time.time()
        print('activation_time: {}'.format(self.__last_activation))

        if sess.query(Widget).first() == None:
            print('Widget has no entry yet. creating new')
            widget = Widget(last_activation = self.__last_activation)
            sess.add(widget)
            sess.commit()
        else:
            print('updating existing widget entry: {}'.format(math.floor(self.__last_activation)))
            sess.query(Widget).first().last_activation = math.floor(self.__last_activation)
            sess.commit()

    def update_reservoir_size(self, value):
        with session as sess:
            self.__reservoir_size = value
            sess.query(Settings).first().reservoir_size = value
            sess.commit()

    def update_consumption(self, value):
        with session as sess:
            self.__consumption = value

    def calculate_refill(self, activation_time):
        interval = activation_time - self.__last_activation
        print(f'intervall: {interval}')
        print(f'water_level: {self.__water_level}')
        max_pump_activations = math.floor(self.__water_level / self.__consumption)
        return interval * max_pump_activations

    def estimate_interval(self, temperature=0):
        pass
        # TODO: implement estimation of the pump activation interval baed on the temperature



    def stop(self):
        self.__stop_flag = True


    def get_status(self):
        return self.__ws_status

    def set_water_level(self, value):
        self.__water_level = value

    def set_activation_level(self, value):
        print(f'activation_level set: {value}')
        self.__activation_level = value
        # with session as sess:
        #     WateringSystem.activationLevel = sess.query(Widget).first().activation_level

    def get_activationLevel(self):

        return self.__activation_level

    def set_state(self, value):
        print(f'widget_state set: {value}')
        self.__widget_state = value
        with session as sess:
            self.__water_level = sess.query(Widget).first().current_water_level
            self.__consumption = sess.query(Settings).first().consumption
            self.__reservoir_size = sess.query(Settings).first().reservoir_size
        # with session as sess:
        #     WateringSystem.state = sess.query(Widget).first().widget_state

    def get_state(self):
        return self.__widget_state

    def get_water_level(self):
        return self.__water_level

    def log_activation(self):
        client.switch_database('activation')
        json_body = [
            {
                "measurement": "activation",
                "fields": {
                    "value": 1
                }
            },

        ]

        was_successfull = client.write_points(json_body)
        return was_successfull

    def log_temperature(self, sess):

        # TODO: catch exception
        location = sess.query(Settings).first().location

        base_url = 'http://api.openweathermap.org/data/2.5/'
        type = ['weather', 'history']


        concat_url = base_url + type[0] + '?q=' + location + '&appid=' + API_KEY
        # print('concat_url: {}'.format(concat_url))
        conversion_val = 273.15

        r = requests.get(concat_url)

        temp = r.json()['main']['temp'] - conversion_val
        # print(temp)

        client.switch_database('humidity')
        json_body = [
            {
                "measurement": "temperature",
                "fields": {
                    "value": temp
                }
            },
        ]
        # TODO: HANDLE EXCEPTION
        was_successfull = client.write_points(json_body)

        return was_successfull



    def log_humidity(self, humidity, interval):

        json_body = []
        i = 0

        # print('time: {} '.format(time.time() - self.__start_time))
        if time.time() - self.__start_time > interval:
            self.__start_time = time.time()
            # percent = humidity.inPercent()
            # value = humidity.getValue()
            print('start logging humidity to influx db')

            for hum in humidity:
                json_body.append(
                    {
                        "measurement": "humidity",
                        "tags": {
                            "sensor": i
                        },
                        "fields": {
                            "value": hum.getValue(),
                            "percent": hum.inPercent()
                        }
                    })
                i += 1
            # print('json_body: {}'.format(json_body))

            client.switch_database('humidity')
            # HANDLE EXCEPTION
            wasSuccessfull = client.write_points(json_body)
            if wasSuccessfull:
                print('logged data to influxdb')
            else:
                print('an error occured logging temperature to influxdb')
        # return wasSuccessfull




    def decodeStatus(self):

        if self.__ws_status == 0:
            self.statusText = "All good"
        if self.__ws_status == 1:
            self.statusText = "Running Pump"
        if self.__ws_status == -1:
            self.statusText = "Error. Pump running for too long. Automatic System deactivated. Please use /start to start it again."


    def startSystem(self):
        self.__motor.stop()
        start = time.time()
        engine2 = create_engine(SQLALCHEMY_DATABASE_URI)
        Session = sessionmaker(bind = engine2)
        session2 = Session()


        counter = 0
        channels = 4
        time.sleep(3);


        # MAIN LOOP
        while True:
            humidity = [sensor.getHumidity() for sensor in self.__sensor]
            # print('humidity: {}'.format(humidity))

            self.log_humidity(humidity, 60)

            if self.__widget_state:
                with session2 as sess:
                    print(f'logging temperature: {time.time()}')
                    self.log_temperature(sess)
                    print('done logging temperature!')


            # TODO: how to handle the startup scenario
            print('widget_state: {}\n\
                activation_level: {}\n\
                waterlevel({}) - consumption({}) = {}\nfrom {}'
                .format(
                    self.__widget_state,
                    self.__activation_level,
                    self.__water_level,
                    self.__consumption,
                    self.__water_level - self.__consumption,
                    self))

            print('self.__activation_level:  {} humidity: {}'
                .format(self.__activation_level, humidity[2].inPercent()))

            if (self.__activation_level > humidity[2].inPercent()) and \
                self.__water_level - self.__consumption >= 0 and \
                self.__widget_state:

                counter+=1


                with session2 as sess:
                    print('updating water_level')
                    self.update_water_level(sess)
                    print('water_level updated!')
                    self.log_activation()
                    self.update_last_activation(sess)

                print("Low humidity Level. Starting pump.")
                self.__ws_status = 1
                self.decodeStatus()
                self.__motor.continuous("right")
                print('done pumping for 30 sec')


            else:
                counter = 0
                self.__ws_status = 0
                self.decodeStatus()
                print('Channel 3: {0}'.format(self.__sensor[0].getHumidity().getValue()))
                # self.__motor.stop()

                # wait a bit to not constantly check for changes
                time.sleep(30)

            if counter == 5:
                print(self.__errorMsg)
                self.__ws_status = -1
                self.decodeStatus()
                self.__motor.stop()
                break


    def start(self):
        t1 = self.__executor.submit(self.startSystem)
        # t1.result()




wsys = WateringSystem()
