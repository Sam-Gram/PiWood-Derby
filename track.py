import time
from displays import Displays
from sensors import Sensors

class Track():
    def __init__(self):
        self.sensors = Sensors()
        self.displays = Displays()

    def startRace(self):
        self.displays.clear()
        self.sensors.start()

    def stopRace(self):
        # No  need to keep sensing when no race is happening
        self.sensors.stop()
        self.displays.displayTimes(self.sensors.getTimes())
        return self.sensors.getTimes()

    def getTimes(self):
        return self.sensors.getTimes()

    def test(self):
        self.displays.displayHex([0xba5e, 0xba11, 0x0])
        time.sleep(2)
        self.displays.displayHex([0x0, 0xcafe, 0xbabe])
        time.sleep(2)
        self.displays.displayHex([0xdead, 0x0, 0xbeef])
        time.sleep(2)
        self.displays.clear()
        time.sleep(1)
        currentTime = time.time()
        while (currentTime + 12.0) > time.time():
            self.displays.displayTimes(self.sensors.getState())
            print self.sensors.getGateInput()
        self.displays.clear()
