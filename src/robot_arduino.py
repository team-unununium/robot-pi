from threading import Thread
import json
import logging
import time
import serial

import src.robot_settings as settings

logger = logging.getLogger("Arduino Module")

class ArduinoProgram:
    def __init__(self):
        logger.info("Arduino program initiated")
        self.working = False # Whether the module is up and running
        self.dataThread = Thread(target=self.dataHandler) # The thread managing the data input from the Arduino
        self.info = {} # The info of the Arduino

        if settings.MOCK_ARDUINO_ENABLED:
            logger.info("Arduino is being mocked, program will not connect to arduino port")
            self.working = True
            return

        try:
            self.serialPort = serial.Serial(settings.ARDUINO_PORT)
            self.serialPort.open()
            self.working = True
        except Exception as e:
            logger.error(f"Arduino program initiation failed with error message '{str(e)}'")
            self.working = False

    def start(self):
        if settings.MOCK_ARDUINO_ENABLED:
            logger.info("Mock arduino program started")
        elif self.working:
            logger.info("Arduino program started")
            self.dataThread.start()
        else:
            logger.warning(f"Arduino program is not working, cannot start program")
            print("An error occured while attempting to start the Arduino program. Please check the logs for more information.")

    def stop(self):
        self.working = False
        if self.working:
            logger.info("Arduino program stopped")
            if not settings.MOCK_ARDUINO_ENABLED:
                self.serialPort.close()
        else:
            logger.warning(f"Arduino program is not working (already stopped)")

    # Writes a symbol to the Arduino
    def writeToPort(self, dataString):
        if settings.MOCK_ARDUINO_ENABLED:
            logger.info("Mocked data: " + dataString)
        else:
            self.serialPort.write(str(dataString))

    # Main data handler
    def dataHandler(self):
        while self.working:
            currentLine = self.serialPort.readline()
            if currentLine is not None and len(currentLine.rstrip("\n")) > 0:
                try:
                    self.info = json.loads(currentLine.rstrip("\n"))
                    settings.socketProgram.updateData(self.info)
                except Exception as e:
                    logger.warn("Invalid JSON string received from Arduino, skipping")
            time.sleep(0.5)

    def startMoving(self):
        if self.working:
            self.writeToPort("%A")
            logger.debug("Outgoing command A (start moving) sent")
        else:
            logger.debug("Outgoing command A (start moving) called when Arduino program has not started")

    def stopMoving(self):
        if self.working:
            self.writeToPort("%B")
            logger.debug("Outgoing command B (stop moving) sent")
        else:
            logger.debug("Outgoing command B (stop moving) called when Arduino program has not started")

    def changeSpeed(self, data):
        if self.working:
            velocityData = data["velocity"]
            self.writeToPort(f"%C{str(velocityData)}")
            logger.debug(f"Outgoing command C (set velocity) sent with value {str(velocityData)}")
        else:
            logger.debug("Outgoing command C (set velocity) called when Arduino program has not started")

    def rotateCamera(self, data):
        logger.debug("Test")
        if self.working:
            velocityData = data["velocity"]
            self.writeToPort(f"%D{str(velocityData)}")
            logger.debug(f"Outgoing command D (rotate camera) sent with value {str(velocityData)}")
        else:
            logger.debug("Outgoing command D (rotate camera) called when Arduino program has not started")

    def rotate(self, data):
        if self.working:
            velocityData = data["velocity"]
            self.writeToPort(f"%E{str(velocityData)}")
            logger.debug(f"Outgoing command E (rotate robot) sent with value {str(velocityData)}")
        else:
            logger.debug("Outgoing command E (rotate robot) called when Arduino program has not started")

if __name__ == "__main__":
    logger.critical("Module robot_arduino ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")
