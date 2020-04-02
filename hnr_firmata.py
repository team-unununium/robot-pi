from threading import Thread
from pyfirmata2 import Arduino
import json
import logging
import time

import hnr_settings as settings

logger = logging.getLogger("Firmata Module")

# Converts a ASCII compatible character to a 8 bit array
def charToArray(value):
    valueArray = [int(d) for d in str(bin(ord(value)))[2::]]
    # 8 bits per byte
    while len(valueArray) < 8:
        valueArray.insert(0, 0)
    return valueArray

# Converts an 8 bit array to an ASCII compatible character
def arrayToChar(array):
    if not isinstance(array, list):
        raise ValueError(f"Type of input is of type {type(array)} instead of the expected list")
    elif len(array) != 8:
        raise ValueError(f"Length of input array incorrect, expected 8 instead of {len(array)}")
    else:
        index = 0
        total = 0
        array.reverse()
        for value in array:
            total += value * (2 ** index)
            index += 1
        return chr(total)

class FirmataProgram:
    def __init__(self):
        logger.info("Firmata program initiated")
        self.working = True # Whether the module is up and running
        self.arduinoOnline = False # Whether the Arduino says hi already
        self.transferringData = False # Whether there is currently a data transfer going on
        self.transferBit = 0 # The bit number that is being trasferred. The bits are converted to characters every 8 bits
        self.transferChr = "" # The character sent by the Arduino before the transfer starts
        self.dataThread = Thread(target=self.dataHandler) # The thread managing the data input from the Arduino
        self.dataString = "" # The current data string received by the Pi since the start of the transfer 
        self.lastEight = [] # The last 8 bits received from the Arduino
        self.info = {} # The info of the Arduino

        try:
            self.board = Arduino(Arduino.AUTODETECT)
            # TODO: Convert to actual pin (Assuming that pin is digital)
            self.inputPin = self.board.get_pin(settings.INPUT_PIN) # The pin that can read but not write
            self.outputPin = self.board.get_pin(settings.OUTPUT_PIN) # The pin that can write but not read
            logger.debug(f"Sampling period is 15ms, arduino port is {Arduino.AUTODETECT}")
        except Exception as e:
            logger.error(f"Firmata program initiation failed with error message '{str(e)}'")
            self.working = False

    def start(self):
        if self.working:
            logger.info("Firmata program started")
            self.inputPin.enable_reporting()
            self.dataThread.start()
            while not self.arduinoOnline:
                self.writeArray(charToArray("!")) # Saying hello to the Arduino
                time.sleep(1) # Check every second
            self.requestData()
        else:
            logger.warning(f"Firmata program is not working, cannot start program")
            print("An error occured while attempting to start the Firmata program. Please check the logs for more information.")

    def stop(self):
        if self.working:
            logger.info("Firmata program stopped")
            self.board.samplingOff()
            self.board.exit()

            self.working = False
            self.arduinoOnline = False
            self.transferringData = False
        else:
            logger.warning(f"Firmata program is not working, cannot stop program")
            print("An error occured while attempting to stop the Firmata program. Please check the logs for more information.")

    # Initializes the transfer related variables
    def prepTransfer(self, transferChr):
        self.transferringData = True
        self.transferBit = 0
        self.transferChr = transferChr
        self.dataString = ""

    # Writes a binary array to the Arduino
    def writeArray(self, array):
        for bit in array:
            self.outputPin.write(bit)

    # Main data handler
    def dataHandler(self):
        while self.working:
            self.lastEight.append(int(round(self.pin.read())))
            # Insert array to 8 bytes
            while len(self.lastEight) < 8:
                self.lastEight.insert(0, 0)
            # Trim array to 8 bytes
            if len(self.lastEight) > 8:
                self.lastEight = self.lastEight[-8:]

            # Check if any data transfer is going on
            currentChr = arrayToChar(self.lastEight)
            if self.transferringData:
                self.transferBit += 1
                if self.transferBit == 8:
                    # This character will be recorded in the data string
                    self.transferBit = 0
                if currentChr == "&":
                    # Stop transferring data and record transferred data
                    # The resetting of the variables used will be done during prepTransfer of the next data transfer
                    self.transferringData = False
                    if self.transferChr == "@" or self.transferChr == "%":
                        # Convert data string (JSON) to dictionary
                        receivedInfo = json.loads(self.dataString)
                        if self.transferChr == "@":
                            # Full data transfer, replaces existing data
                            self.info = receivedInfo
                        elif self.transferChr == "%":
                            # Partial data transfer, updates specific keys
                            for key in receivedInfo:
                                self.info[key] = receivedInfo[key]
                        settings.socketProgram.updateData(self.info)
                    else:
                        logger.warn(f"Invalid data transfer received from Arduino with transferChr {self.transferChr} and data {self.dataStrubg}")
                else:
                    self.dataString += currentChr
            else:
                # Checks the current chracter
                if currentChr == "&":
                    logger.warning(f"Terminating character received despite no data transfer in progress")
                elif currentChr == "@":
                    self.prepTransfer(currentChr)
                elif currentChr == "%":
                    self.prepTransfer(currentChr)
                elif currentChr == "!":
                    self.arduinoOnline = True # Arduino says hi
    
    def requestData(self):
        self.writeArray(charToArray("@")) # Send me all the data

    def startMoving(self):
        self.writeArray(charToArray("*")) # Start moving

    def stopMoving(self):
        self.writeArray(charToArray("~")) # Stop moving

    def rotate(self, data):
        self.writeArray(charToArray("^")) # Rotation data incoming
        for char in str(data):
            self.writeArray(charToArray(char))
        self.writeArray(charToArray("&")) # Data transfer complete

if __name__ == "__main__":
    logger.critical("Module hnr_firmata ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")