import time
import signal
import sys
import RPi.GPIO as GPIO

GPIO.cleanup()

def my_callback(channel):
    print("Changed!")


if GPIO.getmode() != GPIO.BOARD:
    GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(37, GPIO.RISING,
                                 callback=my_callback,
                                 bouncetime=300)
currentTime = time.time()
while (currentTime + 12.0) > time.time():
    time.sleep(0.5)
    print GPIO.input(37)

