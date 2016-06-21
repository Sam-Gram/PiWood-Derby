import time
import signal
import sys
import RPi.GPIO as GPIO
from Adafruit_LED_Backpack import SevenSegment

GPIO.setmode(GPIO.BOARD)

# The inputs being used 
blueInputPin = 11
redInputPin = 13
greenInputPin = 15


GPIO.setup(blueInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(redInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(greenInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

blueDisplay = SevenSegment.SevenSegment(address=0x70, busnum=1)
redDisplay = SevenSegment.SevenSegment(address=0x71, busnum=1)
greenDisplay = SevenSegment.SevenSegment(address=0x72, busnum=1)

# List of displays
displayList = [blueDisplay, redDisplay, greenDisplay]

# List of GPIO inputs
inputList = [blueInputPin, redInputPin, greenInputPin]

# Turn off displays when killed
def signal_handler(signal, frame):
    for display in displayList:
        display.clear()
        display.write_display()
    sys.exit()

signal.signal(signal.SIGINT, signal_handler)

startTime = time.time()

numCallbackCalls = 0

blueTime = 0
redTime = 0
greenTime = 0

timesList = [blueTime, redTime, greenTime]

def displayTimes():
    for i, display in enumerate(displayList):
        display.clear()
        display.print_float(timesList[i], decimal_digits=3)
        display.write_display()


def my_callback(channel):
    timesList[inputList.index(channel)] = time.time() - startTime
    global numCallbackCalls
    numCallbackCalls += 1
    if numCallbackCalls == 3:
        displayTimes()

    print(channel)
        # sleep(1.5)  # confirm the movement by waiting 1.5 sec
        # if GPIO.input(7): # and check again the input
        #     # stop detection for 20 sec
        #     GPIO.remove_event_detect(7)
        #     sleep(20)
        #     GPIO.add_event_detect(7, GPIO.RISING, callback=my_callback, bouncetime=300)


for input_ in inputList:
    GPIO.add_event_detect(input_, GPIO.FALLING,
                          callback=my_callback,
                          bouncetime=300)

# TODO move to events
while True:
    time.sleep(0.0001)
    # for i in range(3):
    #     displayList[i].clear()
    #     displayList[i].print_hex(GPIO.input(inputList[i]))
    #     displayList[i].write_display()
