
'''This class is representing a Humidity value

'''

class Humidity():


    def __init__(self, value):

        self.__value = value

        self.__minValue = 692

        self.__maxValue = 1397

        self.__valueInPercent = 0

        assert(value < self.__minValue, 'Vorbedingung verletzt: Feuchtigkeit darf nicht kleiner als 692 sein.')
        assert(value > self.__maxValue, 'Vorbedingung verletzt: Feuchtigkeit darf nicht kleiner als 1397 sein.')



    def intToHumidity(self, value):

        '''Converts an Integer to a Humidity Unit

        @param value: the value to Converts
        @return the Humidity Unit
        
        '''
        return Humidity(value)




    def getValue(self):

        '''Returns the Value of the Humidity Unit

        @return the value in int

        '''

        return self.__value




    def inPercent(self):

        '''Converts the Humidity to percent eg. "100.0"

        @return the Humidity in Percent from 0 to 100

        '''

        range = self.__maxValue - self.__minValue
        value = self.__value - self.__minValue
        percent = float(100)/float(range)
        return 100 - round(percent*value)




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


        return ('{\"value\":\"' + self.getStringValue() + '\",' +
        '\"percentString\":\"' + self.inPercentString() + '\",' +
        '\"percent\":\"' + str(self.inPercent()) + '\"}')
