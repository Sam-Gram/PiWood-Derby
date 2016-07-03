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

# Initialize Displays
for display in displayList:
    display.begin()

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

        # Ensure that the the number fits on the displays
        # Adjust the digit place depending if the time is ten seconds or greater
        display.print_float(timesList[i] % 100, decimal_digits=(3 if timesList[i] < 10.0 else 2))
        display.write_display()


def my_callback(channel):
    timesList[inputList.index(channel)] = time.time() - startTime
    global numCallbackCalls
    numCallbackCalls += 1
    if numCallbackCalls == 3:
        displayTimes()

    print(channel)


for input_ in inputList:
    GPIO.add_event_detect(input_, GPIO.FALLING,
                          callback=my_callback,
                          bouncetime=300)

# Main loop for test
while True:
    time.sleep(0.0001)

