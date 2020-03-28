from pyfirmata2 import Arduino, util
import logging

class FirmataProgram:
    def __init__(self):
        logging.info("Firmata program initiated")
        self.samplingPeriod = 15 # In ms
        self.working = True
        try:
            self.board = Arduino(Arduino.AUTODETECT)
            logging.debug(f"Sampling period is 15ms, arduino port is {Arduino.AUTODETECT}")
        except Exception as e:
            logging.error(f"Firmata program initiation failed with error message '{str(e)}'")
            self.working = False

    def start(self):
        if self.working:
            logging.info("Firmata program started")
            # TODO: Set up actual port connection
            self.board.digital[0].register_callback(self.dataCallback)
            self.board.samplingOn(self.samplingRate)
            self.board.digital[0].enable_reporting()
            self.board.digital[0].write(1) # Saying hello to the Arduino
        else:
            logging.error(f"Firmata program is not working, cannot start program")
            print("An error occured while attempting to start the Firmata program. Please check the logs for more information.")

    def dataCallback(self, data):
        # Main data handler
        # TODO: Complete data handler
        pass

    def stop(self):
        self.board.samplingOff()
        self.board.exit()

if __name__ == "__main__":
    logging.critical("Module hnr_firmata ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")