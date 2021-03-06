import RPi.GPIO as GPIO

class Gate():
    def __init__(self):
        if GPIO.getmode() != GPIO.BOARD:
            GPIO.setmode(GPIO.BOARD)

        # Pin for the solenoid release gate
        self.gateOutputPin = 33

        # Setup GPIO pin
        GPIO.setup(self.gateOutputPin, GPIO.OUT)

    def release(self):
        GPIO.output(self.gateOutputPin, True)

    def reset(self):
        GPIO.output(self.gateOutputPin, False)

