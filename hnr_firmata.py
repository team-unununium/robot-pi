from pyfirmata2 import Arduino, util
import logging

class FirmataProgram:
    def __init__(self):
        self.samplingPeriod = 15 # In ms
        self.board = Arduino(Arduino.AUTODETECT)
        logging.info(f"Firmata program initiated, sampling period is 15ms, arduino port is {Arduino.AUTODETECT}")

    def start(self):
        logging.info("Firmata program started")
        self.board.digital[0].register_callback(self.dataCallback)
        self.board.samplingOn(self.samplingRate)
        self.board.digital[0].enable_reporting()
        self.board.digital[0].write(1) # Saying hello to the Arduino

    def dataCallback(self, data):
        # Main data handler
        # TODO: Complete
        pass

    def stop(self):
        self.board.samplingOff()
        self.board.exit()

if __name__ == "__main__":
    logging.critical("Module hnr_firmata ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")