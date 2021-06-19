from os import environ
import logging
import socketio
import uuid

logger = logging.getLogger("Settings")

def init():
    logger.info("=" * 30)
    logger.info("Unununium Robot (Raspberry Pi)")
    logger.info("=" * 30)
    logger.info("Settings file initiated")
    # Main programs
    global arduinoProgram
    global socketProgram
    global videoProgram

    # Static variables
    global GUID
    global SERVER_URL
    global SERVER_ROBOT_SECRET
    global ACCESS_TOKEN
    global ARDUINO_PORT
    global BUFFER_DURATION

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
    BUFFER_DURATION = environ.get("BUFFER_DURATION")

    # Initialize dynamic variables
    arduinoProgram = None
    socketProgram = None
    videoProgram = None

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

    if BUFFER_DURATION is None:
        logger.info("BUFFER_DURATION not provided, defaults to 0.4 seconds")
        BUFFER_DURATION = 0.4
    elif BUFFER_DURATION.isnumeric():
        logger.info(f"BUFFER_DURATION is {BUFFER_DURATION}")
    else:
        logger.warning("Invalid BUFFER_DURATION provided, defaults to 0.4 seconds")
        BUFFER_DURATION = 0.4

if __name__ == "__main__":
    logger.critical("Module robot_settings ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")