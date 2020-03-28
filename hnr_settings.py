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

    # Dynamic variables
    global sio

    # Initialize certain variables
    GUID = str(uuid.uuid4())
    SERVER_URL = environ.get("SERVER_URL")
    SERVER_ROBOT_SECRET = environ.get("SERVER_ROBOT_SECRET")
    sio = socketio.Client(reconnection_attempts=10)

    # Variable checking
    if SERVER_URL is None:
        logging.critical("SERVER_URL not provided as environment variable")
        raise ValueError("SERVER_URL should be provided as environment variable")
    elif SERVER_ROBOT_SECRET is None:
        logging.critical("SERVER_ROBOT_SECRET not provided as environment variable")
        raise ValueError("SERVER_ROBOT_SECRET should be provided as environment variable")

if __name__ == "__main__":
    logging.critical("Module hnr_settings ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")