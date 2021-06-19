import time



from WateringApp.materialien.Motor import Motor

# Import the ADS1x15 module.
from .ADS1x15 import ADS1015
import concurrent.futures

from WateringApp.Fachwerte.Humidity import Humidity
from WateringApp.materialien.SoilSensor import SoilSensor

from flask import g, Flask

from .Models import Widget, Settings

from influxdb import InfluxDBClient

from .extensions import db

from sqlalchemy import create_engine
from sqlalchemy.orm import Session




import math

__adc= ADS1015()
__motor = Motor()

__stop_flag = False


__errorMsg = "Error: something is wrong. Aborting program to prevent flooding living room"
__ws_status = 0
statusText = ""
__humidity = Humidity(900)
__sensor = (SoilSensor(1), SoilSensor(2), SoilSensor(3))

__reservoir_size = 0
__consumption = 0
__water_level = 0
__last_activation = 0
__interval = 0

__activation_level = 0
__widget_state = 0
__start_time = time.time()



# def set_last_activation(, last_activation):
#     Widget.query().filter_by(id=1).last_activation = last_activation


def set_consumption(consumtion):
    __consumption = consumption
    return __last_activation

def set_water_level(current_water_level):
    __water_level = current_water_level
    return __water_level

def set_reservoir_size(resevoir_size):
    __reservoir_size = reservoir_size
    return __reservoir_size

def set_last_activation(last_activation):
    __last_activation = last_activation
    return __last_activation

def update_water_level():
    __water_level - __consumption

def update_last_activation(last_activation):
    __last_activation = last_Activation


def calculate_refill(activation_time):
    interval = activation_time - __last_activation
    max_pump_activations = math.floor(__reservoir_size / __consumption)
    return interval * max_pump_activations

def estimate_interval(temperature=0):
    pass
    # TODO: implement estimation of the pump activation interval baed on the temperature



def stop():
    __stop_flag = True


def get_status():
    return __ws_status

def set_activationLevel(value):
    __activation_level = value
    # with session as sess:
    #     WateringSystem.activationLevel = sess.query(Widget).first().activation_level

def get_activationLevel():
    return __activationLevel

def set_state(value):
    __widget_state = value
    # with session as sess:
    #     WateringSystem.state = sess.query(Widget).first().widget_state

def get_state():
    return __activationLevel

def log_humidity(humidity, interval):

    json_body = []
    i = 0

    print('time: {} '.format(time.time() - __start_time))

    if time.time() - __start_time > interval:
        __start_time = time.time()
        # percent = humidity.inPercent()
        # value = humidity.getValue()


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

        print('json_body: {}'.format(json_body))



        client = InfluxDBClient(host='localhost', port=8086)
        client.switch_database('humidity')
        wasSuccessfull = client.write_points(json_body)
        print('logged data to influxdb')
    # return wasSuccessfull




def decodeStatus():

    if __ws_status == 0:
        statusText = "All good"
    if __ws_status == 1:
        statusText = "Running Pump"
    if __ws_status == -1:
        statusText = "Error. Pump running for too long. Automatic System deactivated. Please use /start to start it again."


def startSystem():
    global STOP
    __motor.stop()
    start = time.time()

    counter = 0
    channels = 4
    time.sleep(3);

    # print('widget_state: {}\nactivation_level: {}'.format(__widget_state, __activation_level))

    while True:
        humidity = [sensor.getHumidity() for sensor in __sensor]

        # print('humidity: {}'.format(humidity))

        # humidity = self.__sensor[0].getHumidity()
        # print("activationLevel: " + str(__activationLevel))
        # print("STOP: " + str(STOP))



        # TODO: fix this
        # log_humidity(humidity, 60)


        # print('humidity_in_percent: {}'.format(humidity[0].inPercent()))

        # TODO: how to handle the startup scenario
        # print(f'widget_state: {__widget_state}\nactivation_level: {__activation_level}')
        print('widget_state: {}\nactivation_level: {}'.format(__widget_state, __activation_level))
        if (humidity[0].inPercent() < __activation_level) and (__widget_state):
            counter+=1
            calculate_refill(time.time())
            print("Counter: " + str(counter))
            print('Channel 1: {0}'.format(__sensor[0].getHumidity().getValue()))
            print("Low humidity Level. Starting pump.")
            __ws_status = 1
            decodeStatus()
            __motor.continuous("right")


        else:
            counter = 0
            __ws_status = 0
            decodeStatus()
            print('Channel 3: {0}'.format(__sensor[0].getHumidity().getValue()))
            # __motor.stop()
            # print('widget_state: {}\nactivation_level: {}'.format(__widget_state, __activation_level))

            # wait a bit to not constantly check for changes
            time.sleep(30)

        if counter == 5:
            print(__errorMsg)
            __ws_status = -1
            decodeStatus()
            # __motor.stop()
            break

        # if STOP :
        #     print(self.__errorMsg)
        #     self.__ws_status = -1
        #     self.decodeStatus()
        #     self.__motor.stop()
        #     break

        # if getattr(daemon,"stop", True) :
        #     print(self.__errorMsg)
        #     self.__ws_status = -1
        #     self.decodeStatus()
        #     self.__motor.stop()
        #     break

def start():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(startSystem)
