import unittest
from WateringApp.Humidity import Humidity

class TestHumidity(unittest.TestCase):




    def testIntToHumidity(self):
        humidity2 = Humidity.intToHumidity(692)
        humidity = Humidity(692)

        self.assertTrue(humidity2 == humidity)




    def testGetValue(self):
        humidity = Humidity(692)
        self.assertTrue((humidity.getValue() == 692))





    def testInPercent(self):

        humidity = Humidity(692).inPercent()
        humidity50 = Humidity((1397+692)/2).inPercent()
        print(humidity)
        print(humidity50)
        self.assertTrue((humidity == round(float(0))))
        self.assertTrue((humidity50 == round(float(50))))




    def testInPercentString(self):

        humidity = Humidity(692).inPercent()
        self.assertTrue((str(humidity) + "%" == "0%"))




    def testGetStringValue(self):

        humidity = Humidity(692).getStringValue()
        self.assertTrue(humidity == "692")



    def testToJSONString(self):

        testDict = {
            "value": "692",
            "percentString": "0%",
            "percent": 0
        }

        humidity = Humidity(692)

        self.assertTrue(humidity.toJSONString() == testDict)


    if __name__ == '__main__':
        unittest.main()
