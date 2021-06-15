from WateringApp.Fachwerte.Humidity import Humidity
# Import the ADS1x15 module.
from WateringApp.ADS1x15 import ADS1115

class SoilSensor:

    AMOUNT = 3

    def __init__(self, channel):
        self.__adc = ADS1115()
        self.__channel = channel
        self.__humidity = Humidity(900)
        self.__GAIN = 1


    def getHumidity(self):
        raw_val = self.__adc.read_adc(self.__channel, gain=self.__GAIN)
        # print('raw value: ' + str(raw_val))
        humidity = self.__humidity.intToHumidity(raw_val)
        hum_val = humidity.getValue()
        if hum_val < humidity.getMinValue() and hum_val > 100:
            humidity.setMinValue(hum_val)
        if hum_val > humidity.getMaxValue():
            humidity.setMaxValue(hum_val)
        # self.__adc.stop_adc();
        return humidity
