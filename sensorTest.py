import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

blueInputPin = 11
redInputPin = 13
greenInputPin = 15

GPIO.setup(blueInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(redInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(greenInputPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    time.sleep(1)
    print("Blue ", GPIO.input(blueInputPin))
    print("Red " , GPIO.input(redInputPin))
    print("Green", GPIO.input(greenInputPin))
