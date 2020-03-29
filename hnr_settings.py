from os import environ
import logging
import socketio
import uuid

def init():
    logging.info("Settings file initiated")
    # Main programs
    global cameraProgram
    global firmataProgram
    global robotProgram
    global socketProgram

    # Static variables
    global GUID
    global SERVER_URL
    global SERVER_ROBOT_SECRET
    global ACCESS_TOKEN
    global RESOLUTION
    global FRAMERATE

    # Dynamic variables
    global sio
    global programRunning

    # Initialize static variables
    GUID = str(uuid.uuid4())
    SERVER_URL = environ.get("SERVER_URL")
    SERVER_ROBOT_SECRET = environ.get("SERVER_ROBOT_SECRET")
    RESOLUTION = environ.get("RESOLUTION")
    FRAMERATE = environ.get("FRAMERATE")

    # Initialize dynamic variables
    sio = socketio.Client(reconnection_attempts=10)
    programRunning = True

    # Variable checking
    # Must-provide variables
    if SERVER_URL is None:
        logging.critical("SERVER_URL not provided as environment variable")
        raise ValueError("SERVER_URL should be provided as environment variable")
    elif SERVER_ROBOT_SECRET is None:
        logging.critical("SERVER_ROBOT_SECRET not provided as environment variable")
        raise ValueError("SERVER_ROBOT_SECRET should be provided as environment variable")

    # Optional variables
    if RESOLUTION is None:
        logging.info("RESOLUTION not provided, defaults to 720p")
        RESOLUTION = (640, 480)
    if FRAME_RATE is None:
        logging.info("FRAME_RATE not provided, defaults to 24")
        FRAMERATE = 30

if __name__ == "__main__":
    logging.critical("Module hnr_settings ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")