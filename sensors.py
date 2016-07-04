import time
import signal
import sys
import RPi.GPIO as GPIO

class Sensors():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        # The inputs being used
        self.blueInputPin  = 11
        self.redInputPin   = 13
        self.greenInputPin = 15

        # List of GPIO inputs
        self.inputList = [self.blueInputPin,
                          self.redInputPin,
                          self.greenInputPin]

        # GPIO.PUD_UP Handles bouncing signals
        # Setup GPIO pins
        for input_ in self.inputList:
            GPIO.setup(input_, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.startTime = 0.0

        self.timesList = [0, 0, 0]

        self.numCallbacks = 0

    def my_callback(self, channel):
        self.timesList[self.inputList.index(channel)] = time.time() - self.startTime

        GPIO.remove_event_detect(channel)
        print(channel)


    def getTimes(self):
        return self.timesList

    # The callback is called in it's own thread
    def start(self):
        self.startTime = time.time()
        self.timesList = [0] * 3
        self.numCallbackCalls = 0
        for input_ in self.inputList:
            GPIO.add_event_detect(input_, GPIO.FALLING,
                                 callback=self.my_callback,
                                 bouncetime=300)


    def stop(self):
        for input_ in self.inputList:
            GPIO.remove_event_detect(input_)
