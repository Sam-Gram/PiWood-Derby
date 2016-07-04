from displays import Displays
from sensors import Sensors
from gate import Gate

class Track():
    def __init__(self):
        self.sensors = Sensors()
        self.displays = Displays()
        self.gate = Gate()

    def startRace(self):
        self.gate.release()
        self.sensors.start()

    def stopRace(self):
        # No  need to keep sensing when no race is happening
        self.sensors.stop()
        # Make sure we can reset the gate
        self.gate.reset()
        self.displays.displayTimes(self.sensors.getTimes())

    def getTimes(self):
        return self.sensors.getTimes()
