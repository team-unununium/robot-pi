from pyfirmata2 import Arduino, util

class FirmataProgram:
    def __init__(self):
        self.samplingPeriod = 15 # In ms
        self.board = Arduino(Arduino.AUTODETECT)

    def start(self):
        self.board.analog[0].register_callback(self.dataCallback)
        self.board.samplingOn(self.samplingRate)
        self.board.analog[0].enable_reporting()

    def dataCallback(self, data):
        # Main data handler
        # TODO: Complete
        pass

    def stop(self):
        self.board.samplingOff()
        self.board.exit()

if __name__ == "__main__":
    raise RuntimeError("This file is a module and should not be run as a program")