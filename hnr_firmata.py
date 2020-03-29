from pyfirmata2 import Arduino, util
import logging

logger = logging.getLogger("Firmata Module")

class FirmataProgram:
    def __init__(self):
        logger.info("Firmata program initiated")
        self.samplingPeriod = 15 # In ms
        self.working = True
        try:
            self.board = Arduino(Arduino.AUTODETECT)
            logger.debug(f"Sampling period is 15ms, arduino port is {Arduino.AUTODETECT}")
        except Exception as e:
            logger.error(f"Firmata program initiation failed with error message '{str(e)}'")
            self.working = False

    def start(self):
        if self.working:
            logger.info("Firmata program started")
            # TODO: Set up actual port connection
            self.board.digital[0].register_callback(self.dataCallback)
            self.board.samplingOn(self.samplingRate)
            self.board.digital[0].enable_reporting()
            self.board.digital[0].write(1) # Saying hello to the Arduino
        else:
            logger.warning(f"Firmata program is not working, cannot start program")
            print("An error occured while attempting to start the Firmata program. Please check the logs for more information.")

    def dataCallback(self, data):
        # Main data handler
        # TODO: Complete data handler
        pass

    def stop(self):
        if self.working:
            logger.info("Firmata program stopped")
            self.board.samplingOff()
            self.board.exit()
        else:
            logger.warning(f"Firmata program is not working, cannot stop program")
            print("An error occured while attempting to stop the Firmata program. Please check the logs for more information.")

if __name__ == "__main__":
    logger.critical("Module hnr_firmata ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")