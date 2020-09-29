# Simple demo of continuous ADC conversion mode for channel 0 of the ADS1x15 ADC.
# Author: Tony DiCola
# License: Public Domain
import time

from WateringApp.Motor import Motor

# Import the ADS1x15 module.
from ADS1x15 import ADS1015
import threading

from WateringApp.Humidity import Humidity
from WateringApp.SoilSensor import SoilSensor



# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.

class WateringSystem(object):

    def __init__(self):

        self.__adc= ADS1015()
        self.__motor = Motor()

        self.__stop_flag = False


        self.__errorMsg = "Error: something is wrong. Aborting program to prevent flooding living room"
        self.__ws_status = 0
        self.statusText = ""
        self.__humidity = Humidity(900)
        self.__sensor = SoilSensor()


    def stop(self):
        self.__stop_flag = True


    def getStatus(self):
        return self.__ws_status



    def decodeStatus(self):

        if self.__ws_status == 0:
            self.statusText = "All good"
        if self.__ws_status == 1:
            self.statusText = "Running Pump"
        if self.__ws_status == -1:
            self.statusText = "Error. Pump running for too long. Automatic System deactivated. Please use /start to start it again."


    def start(self):
        self.__motor.stop()
        start = time.time()
        counter = 0
        channels = 4
        time.sleep(3);
        while True:
            humidity = self.__sensor.getHumidity(3)
            if humidity.getValue() > 900 and counter < 5:
                startTime = time.time()
                currentTime = startTime
                while startTime - currentTime < 30:
                    currentTime = time.time()
                    counter+=1
                    print("Counter: " + str(counter))
                    print('Channel 3: {0}'.format(self.__sensor.getHumidity(3).getValue()))
                    print("Low humidity Level. Starting pump.")
                    self.__ws_status = 1
                    self.decodeStatus()
                    self.__motor.continuous()


            else:
                counter = 0
                self.__ws_status = 0
                self.decodeStatus()
                print('Channel 3: {0}'.format(self.__sensor.getHumidity(3).getValue()))
                self.__motor.stop()
                time.sleep(30)

            if counter == 5:
                print(self.__errorMsg)
                self.__ws_status = -1
                self.decodeStatus()
                self.__motor.stop()
                break
