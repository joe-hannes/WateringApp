# Simple demo of continuous ADC conversion mode for channel 0 of the ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain
import time

from WateringApp.Motor import Motor

# Import the ADS1x15 module.
from .ADS1x15 import ADS1015
import threading

from WateringApp.Fachwerte.Humidity import Humidity
from WateringApp.SoilSensor import SoilSensor

from flask import g, Flask

from .Models import Widget

from influxdb import InfluxDBClient


STOP = False

class WateringSystem(object):


    def __init__(self):

        self.__adc= ADS1015()
        self.__motor = Motor()

        self.__stop_flag = False


        self.__errorMsg = "Error: something is wrong. Aborting program to prevent flooding living room"
        self.__ws_status = 0
        self.statusText = ""
        self.__humidity = Humidity(900)
        self.__sensor = SoilSensor(1)

        self.__activationLevel = 0
        self.__state = 0
        self.startSystem()


    def stop(self):
        self.__stop_flag = True


    def get_status(self):
        return self.__ws_status

    def set_activationLevel(self, value):
        self.__activationLevel = value

    def get_activationLevel(self):
        return self.__activationLevel

    def set_state(self, value):
        self.__activationLevel = value

    def get_state(self):
        return self.__activationLevel

    def log_data(self):
        percent = humidity.inPercent()
        value = humidity.getValue()

        json_body = [
            {
                "measurement": "humidity",
                "fields": {
                    "value": value,
                    "percent": percent
                }
            }

        ]

        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('humidity')
        wasSuccessfull = client.write_points(json_body)
        return wasSuccessfull




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
        global STOP
        counter = 0
        channels = 4
        time.sleep(3);
        daemon = threading.currentThread()


        # g.db.Widget.query.first().activationLevel

        # self.__activationLevel = g.db.Widget.query.first().activationLevel
        # self.__state = g.db.Widget.query.first().widgetState

        daemon = threading.Thread(name='startSystem',
                                  target=self.startSystem, args=())



        while True:
            humidity = self.__sensor.getHumidity()
            print("activationLevel: " + str(self.__activationLevel))
            print("STOP: " + str(STOP))

            if time.time() - start > 60:
                start = time.time()
                log_data(humidity)
                print('logged data to influxdb')


            if (humidity.inPercent() < self.__activationLevel) and (self.__state):
                startTime = time.time()
                currentTime = startTime

                currentTime = time.time()
                counter+=1
                print("Counter: " + str(counter))
                print('Channel 1: {0}'.format(self.__sensor.getHumidity().getValue()))
                print("Low humidity Level. Starting pump.")
                self.__ws_status = 1
                self.decodeStatus()
                self.__motor.continuous("right")


            else:
                counter = 0
                self.__ws_status = 0
                self.decodeStatus()
                print('Channel 3: {0}'.format(self.__sensor.getHumidity().getValue()))
                self.__motor.stop()
                time.sleep(30)

            if counter == 5:
                print(self.__errorMsg)
                self.__ws_status = -1
                self.decodeStatus()
                self.__motor.stop()
                break

            if STOP :
                print(self.__errorMsg)
                self.__ws_status = -1
                self.decodeStatus()
                self.__motor.stop()
                break

            if getattr(daemon,"stop", True) :
                print(self.__errorMsg)
                self.__ws_status = -1
                self.decodeStatus()
                self.__motor.stop()
                break
