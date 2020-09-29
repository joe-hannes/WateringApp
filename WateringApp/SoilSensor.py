from WateringApp.Humidity import Humidity
# Import the ADS1x15 module.
from WateringApp.ADS1x15 import ADS1015

class SoilSensor:
    def __init__(self):

        self.__adc = ADS1015()
        self.__humidity = Humidity(900)
        self.__GAIN = 1

    def getHumidity(self, channel):
        humidity = self.__humidity.intToHumidity(self.__adc.read_adc(channel, gain=self.__GAIN))
        return humidity
