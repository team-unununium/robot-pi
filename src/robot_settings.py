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
    global videoProgram

    # Static variables
    global GUID
    global SERVER_URL
    global SERVER_ROBOT_SECRET
    global ACCESS_TOKEN
    global ARDUINO_PORT

    # WebRTC server variables
    global STUN_URL
    global TURN_URL
    global TURN_USERNAME
    global TURN_PASSWORD
    global TURN_TRANSPORT
    global TURN_TLS

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
    STUN_URL = environ.get("STUN_URL")
    TURN_URL = environ.get("TURN_URL")
    TURN_USERNAME = environ.get("TURN_USERNAME")
    TURN_PASSWORD = environ.get("TURN_PASSWORD")
    TURN_TRANSPORT = environ.get("TURN_TRANSPORT")
    TURN_TLS = environ.get("TURN_TLS")

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
    
    if STUN_URL is None:
        logger.info("STUN_URL not provided, defaults to stun1.l.google.com:19302")
        STUN_URL = "stun1.l.google.com:19302"
    elif len(STUN_URL.split(":")) > 2:
        logger.critical("STUN_URL format not recognised")
        raise ValueError("STUN_URL format should be in the format of domain.com:port or domain.com")
    elif len(STUN_URL.split(":")) == 2 and not STUN_URL.split(":")[1].isnumeric():
        logger.critical("Port for STUN_URL invalid")
        raise ValueError("The port for STUN_URL should be a number")
    else:
        logger.info(f"STUN_URL is {STUN_URL}")
    
    if TURN_URL is None:
        logger.info("TURN_URL not provided, turn server will not be used")
    elif len(TURN_URL.split(":")) > 2:
        logger.critical("TURN_URL format not recognised")
        raise ValueError("TURN_URL format should be in the format of domain.com:port or domain.com")
    elif len(TURN_URL.split(":")) == 2 and not TURN_URL.split(":")[1].isnumeric():
        logger.critical("Port for TURN_URL invalid")
        raise ValueError("The port for TURN_URL should be a number")
    else:
        logger.info(f"TURN_URL is {TURN_URL}")
    
    if TURN_USERNAME is None:
        logger.info("TURN_USERNAME not provided, will not be supplied")
    else:
        logger.info(f"TURN_USERNAME is {TURN_USERNAME}")

    if TURN_PASSWORD is None:
        logger.info("TURN_PASSWORD not provided, will not be supplied")

    TURN_TRANSPORT = TURN_TRANSPORT.lower()
    if TURN_TRANSPORT is None:
        logger.info("TURN_TRANSPORT not provided, defaults to udp")
        TURN_TRANSPORT = "udp"
    elif TURN_TRANSPORT != "udp" and TURN_TRANSPORT != "tcp":
        logger.critical("Invalid TURN_TRANSPORT value read from environment variable")
        raise ValueError("TURN_TRANSPORT should be either udp or tcp")
    else:
        logger.info(f"TURN_URL is udp")

    TURN_TLS = TURN_TLS.lower()
    if TURN_TLS == "true" or TURN_TLS == "t" or TURN_TLS == "y" or TURN_TLS == "yes":
        TURN_TLS = True
        logger.info("TLS enabled for TURN server")
    else:
        TURN_TLS = False
        logger.info("TLS disabled for TURN server")

if __name__ == "__main__":
    logger.critical("Module robot_settings ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")