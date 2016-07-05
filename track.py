import time
from displays import Displays
from sensors import Sensors
from gate import Gate

class Track():
    def __init__(self):
        self.sensors = Sensors()
        self.displays = Displays()
        self.gate = Gate()

    def startRace(self):
        self.displays.clear()
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

    def test(self):
        self.gate.release()
        time.sleep(2)
        self.gate.reset()
        self.displays.displayHex([0xba5e, 0xba11, 0x0])
        time.sleep(2)
        self.displays.displayHex([0x0, 0xcafe, 0xbabe])
        time.sleep(2)
        self.displays.displayHex([0xdead, 0x0, 0xbeef])
        time.sleep(2)
        self.displays.clear()
        time.sleep(1)
        currentTime = time.time()
        while (currentTime + 10.0) > time.time():
            self.displays.displayTimes(self.sensors.getState())
