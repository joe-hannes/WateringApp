
'''This class is representing a Humidity value

'''

class Humidity():


    def __init__(self, value):

        self.__minValue = 10100
        self.__maxValue = 22300


        self.__value = value

        # try:
        #     assert self.istGueltig(value), 'Vorbedingung verletzt: Feuchtigkeit muss zwischen 10100 und 22300 liegen. Ist aber: ' + str(value)
        # except AssertionError:
        #     self.__value = -1



        self.__valueInPercent = 0



    def istGueltig(self, humidity):
        return humidity >= self.__minValue and humidity <= self.__maxValue

    @staticmethod
    def intToHumidity(value):

        '''Converts an Integer to a Humidity Unit

        @param value: the value to convert
        @return the Humidity Unit

        '''
        return Humidity(value)


    def __eq__(self, other):
        if not isinstance(other, Humidity):
            return False

        return self.__value == other.__value

    def __hash__(self):
        return hash(self.__value)


    def getValue(self):

        '''Returns the Value of the Humidity Unit

        @return the value in int

        '''

        return  self.__value




    def inPercent(self):

        '''Converts the Humidity to percent eg. "100.0"

        @return the Humidity in Percent from 0 to 100

        '''

        if self.__value == 0:
            return 0

        range = self.__maxValue - self.__minValue
        value = self.__value - self.__minValue
        percent = float(100) / float(range)
        return round(100 - percent*value)




    def inPercentString(self):

        '''Returns Humidity in Percent as a String e.g "100%"

        @return the humidity as Str

        '''

        return str(self.inPercent()) + "%"




    def getStringValue(self):

        '''Returns Humidity value as a String eg. "100"

        @return the humidity value as Str

        '''

        return str(self.getValue())



    def toJSONString(self):

        '''Return a String with the values as JSON Format "{'key':'value','key2':'value2'}"

        @return the string in JSON Format

        '''

        humidityDict = {
            "value": self.getStringValue(),
            "percentString": self.inPercentString(),
            "percent": self.inPercent()
        }
        return humidityDict
        # return ('\"{\"value\":\"' + self.getStringValue() + '\", ' +
        # '\"percentString\":\"' + self.inPercentString() + '\", ' +
        # '\"percent\":\"' + str(self.inPercent()) + '\"}\"')


    def getMinValue(self):

        ''' Returns Humidity min value

        @return the humidity value as Str

        '''

        return self.__minValue



    def setMinValue(self, value):

        ''' Sets Humidity minimum value

        '''
        self.__minValue = value


    def getMaxValue(self):

        ''' Returns maximum Humidity value

        @return the humidity min value

        '''

        return self.__maxValue


    def setMaxValue(self, value):

        ''' Sets maximum Humidity value

        '''

        self.__maxValue = value
