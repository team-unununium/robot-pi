from os import environ
import logging
import socketio
import uuid

logger = logging.getLogger("Settings")

def init():
    logger.info("Settings file initiated")
    # Main programs
    global arduinoProgram
    global socketProgram

    # Static variables
    global GUID
    global SERVER_URL
    global SERVER_ROBOT_SECRET
    global ACCESS_TOKEN
    global ARDUINO_PORT

    # Dynamic variables
    global sio
    global programStarted
    global programRunning
    global disconnectCount

    # Initialize static variables
    GUID = str(uuid.uuid4())
    SERVER_URL = environ.get("SERVER_URL")
    SERVER_ROBOT_SECRET = environ.get("SERVER_ROBOT_SECRET")
    ARDUINO_PORT = environ.get("ARDUINO_PORT")

    # Initialize dynamic variables
    arduinoProgram = None
    socketProgram = None

    sio = socketio.Client(reconnection_attempts=10)
    programStarted = True
    programRunning = False
    disconnectCount = 0

    # Variable checking
    # Must-provide variables
    if SERVER_URL is None:
        logger.critical("SERVER_URL not provided as environment variable")
        raise ValueError("SERVER_URL should be provided as environment variable")
    elif SERVER_ROBOT_SECRET is None:
        logger.critical("SERVER_ROBOT_SECRET not provided as environment variable")
        raise ValueError("SERVER_ROBOT_SECRET should be provided as environment variable")

    # Optional variables
    if ARDUINO_PORT is None:
        logger.info("ARDUINO_PORT not provided, defaults to /dev/ttyUSB0")
        ARDUINO_PORT = "/dev/ttyUSB0"
    else:
        logger.info(f"ARDUINO_PORT is {ARDUINO_PORT}")

if __name__ == "__main__":
    logger.critical("Module hnr_settings ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")