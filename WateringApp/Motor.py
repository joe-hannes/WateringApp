
import RPi.GPIO as GPIO
import time

class Motor(object):
    def __init__(self):
        self.__enable = 4
        self.__dirPin = 20
        self.__stepPin = 21

        GPIO.setwarnings(False)

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.__dirPin, GPIO.OUT)
        GPIO.setup(self.__stepPin, GPIO.OUT)
        GPIO.setup(self.__enable,GPIO.OUT)



    def __driveMotor(self):
        steps =  5*200
        delay =  0.0005
        start = time.time()

        while time.time() - start <= 30.0:
            for i in range(steps):
                # print("step: " + str(i))
                GPIO.output(self.__stepPin, GPIO.LOW)
                time.sleep(delay)
                GPIO.output(self.__stepPin, GPIO.HIGH)
                time.sleep(delay)
        # GPIO.output(self.__enable,GPIO.HIGH)



    def continuous(self,direction):
        print("Motor started")

        GPIO.output(self.__enable,GPIO.LOW)

        if direction == "left":
            GPIO.output(self.__dirPin, GPIO.LOW)
            self.__driveMotor()
        elif direction == "right":
            GPIO.output(self.__dirPin, GPIO.HIGH)
            self.__driveMotor()
        else:
            print("Invalid direction parameter. Please use 'left' or 'right'")






    def stop(self):
        print("Motor stopped")
        GPIO.output(self.__enable,GPIO.HIGH)
