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
    global CAMERA_WIDTH
    global CAMERA_HEIGHT
    global CAMERA_FPS

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
    CAMERA_WIDTH = environ.get("CAMERA_WIDTH")
    CAMERA_HEIGHT = environ.get("CAMERA_HEIGHT")
    CAMERA_FPS = environ.get("CAMERA_FPS")

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
    
    if CAMERA_WIDTH is None:
        logger.info("CAMERA_WIDTH not provided, defaults to 1280")
        CAMERA_WIDTH = 1280
    elif CAMERA_WIDTH.isDigit():
        logger.info(f"CAMERA_WIDTH is {CAMERA_WIDTH}")
    else:
        logger.warning("Invalid CAMERA_WIDTH provided, defaults to 1280")
        CAMERA_WIDTH = 1280

    if CAMERA_HEIGHT is None:
        logger.info("CAMERA_HEIGHT not provided, defaults to 720")
        CAMERA_HEIGHT = 720
    elif CAMERA_HEIGHT.isDigit():
        logger.info(f"CAMERA_HEIGHT is {CAMERA_HEIGHT}")
    else:
        logger.warning("Invalid CAMERA_HEIGHT provided, defaults to 720")
        CAMERA_HEIGHT = 720
    
    if CAMERA_FPS is None:
        logger.info("CAMERA_FPS not provided, defaults to 30")
        CAMERA_FPS = 30
    elif CAMERA_FPS.isDigit():
        logger.info(f"CAMERA_FPS is {CAMERA_FPS}")
    else:
        logger.warning("Invalid CAMERA_FPS provided, defaults to 30")
        CAMERA_FPS = 30

if __name__ == "__main__":
    logger.critical("Module robot_settings ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")