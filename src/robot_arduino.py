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
        self.arduinoOnline = False # Whether the Arduino is detected
        self.dataThread = Thread(target=self.dataHandler) # The thread managing the data input from the Arduino
        self.info = {} # The info of the Arduino

        try:
            self.serialPort = serial.Serial(settings.ARDUINO_PORT)
            self.serialPort.open()
        except Exception as e:
            logger.error(f"Arduino program initiation failed with error message '{str(e)}'")
            self.working = False

    def start(self):
        if self.working:
            logger.info("Arduino program started")
            self.dataThread.start()
        else:
            logger.warning(f"Arduino program is not working, cannot start program")
            print("An error occured while attempting to start the Arduino program. Please check the logs for more information.")

    def stop(self):
        if self.working:
            logger.info("Arduino program stopped")
            self.serialPort.close()
            self.working = False
            self.arduinoOnline = False
        else:
            logger.warning(f"Arduino program is not working (already stopped)")

    # Writes a symbol to the Arduino
    def writeToPort(self, dataString):
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
        self.writeToPort("%A")

    def stopMoving(self):
        self.writeToPort("%B")

    def changeSpeed(self, data):
        velocityData = data["velocity"]
        self.writeToPort(f"%C{str(velocityData)}")

    def rotateCamera(self, data):
        velocityData = data["velocity"]
        self.writeToPort(f"%D{str(velocityData)}")

    def rotate(self, data):
        velocityData = data["velocity"]
        self.writeToPort(f"%E{str(velocityData)}")

if __name__ == "__main__":
    logger.critical("Module robot_arduino ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")
