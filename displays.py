from Adafruit_LED_Backpack import SevenSegment

class Displays():
    def __init__(self):
        # Change busnum to 0 if using a pi older than B+
        self.blueDisplay   = SevenSegment.SevenSegment(address=0x70, busnum = 1)
        self.redDisplay    = SevenSegment.SevenSegment(address=0x71, busnum = 1)
        self.greenDisplay  = SevenSegment.SevenSegment(address=0x72, busnum = 1)

        self.displayList = [self.blueDisplay, self.redDisplay, self.greenDisplay]

        # Needed to allow displays to work
        for display in self.displayList:
            display.begin()

    # Takes a set of 3 numbers and displays them in order: blue, red and green
    def displayTimes(self, timesList):
        for i, display in enumerate(self.displayList):
            display.clear()

            # Ensure that the the number fits on the displays
            # Adjust the digit place depending if the time is ten seconds or greater

            display.print_float(timesList[i] % 100, decimal_digits=(3 if timesList[i] < 10 else 2))
            display.write_display()

    def clear(self):
        for display in self.displayList:
            display.clear()
            display.write_display()

    def displayHex(self, hexList):
        for i, display in enumerate(self.displayList):
            display.clear()
            display.print_hex(hexList[i])
            display.write_display()
