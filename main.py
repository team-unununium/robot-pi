from dotenv import load_dotenv
from os import environ

import logging
import requests
import signal
import socketio
import uuid

from hnr_camera import CameraProgram
from hnr_firmata import FirmataProgram
import hnr_socketio as SocketProgram

# Set up logging
logging.basicConfig(filename="robot.log", filemode="w", level=logging.INFO, format="%(asctime)s: %(levelname)s: %(message)s", datefmt="%d-%m-%Y %I:%M:%S %p")

# Graceful exit from SIGINT
def signal_handler(sig, frame):
    logging.info("SIGINT detected, shutdown initiated")
    raise SystemExit
signal.signal(signal.SIGINT, signal_handler)

# Get environment variables
load_dotenv()
SERVER_URL = environ.get("SERVER_URL")
SERVER_ROBOT_SECRET = environ.get("SERVER_ROBOT_SECRET")
if SERVER_URL is None or SERVER_ROBOT_SECRET is None:
    logging.critical("SERVER_URL or SERVER_ROBOT_SECRET not provided as environment variable")
    raise ValueError("SERVER_URL and SERVER_ROBOT_SECRET should be provided as environment variable")

# Init variables
GUID = str(uuid.uuid4())
ACCESS_TOKEN = None
sio = socketio.Client(reconnection_attempts=10)

def startPrograms():
    FirmataProgram().start()
    CameraProgram().start()

def main():
    logging.info(f"Main program started, GUID is {GUID}, server URL is {SERVER_URL}, server-robot secret is {SERVER_ROBOT_SECRET}")

    # Get Access token
    req_json = {
        "guid": GUID,
        "secret": SERVER_ROBOT_SECRET
    }
    req_response = requests.post(f"{SERVER_URL}/access", json=req_json)
    req_code = req_response.status_code
    req_success = False

    # Request response handling
    if req_code == 201:
        ACCESS_TOKEN = req_response.json()['token']
        logging.info(f"Access token request successful, access token is {ACCESS_TOKEN}")
        req_success = True
    elif req_code == 400:
        logging.error("Access token request failed with error code 400 (Incorrect parameters)")
    elif req_code == 401:
        logging.error("Access token request failed with error code 401 (Another robot already exists)")
    elif req_code == 403:
        logging.error("Access token request failed with error code 403 (The GUID has been taken)")
    elif req_code == 500:
        logging.error("Access token request failed with error code 500 (Error occured while attempting to query database)")
    else:
        logging.error(f"Access token request failed with unexpected error code {req_code}")

    if req_success:
        SocketProgram.start(GUID, SERVER_URL, ACCESS_TOKEN)
    else:
        print("An error occured while getting the access token. Please check the logs for more information.")
        logging.info("Program shutdown due to unable to get the access token")
        raise SystemExit
                
if __name__ == "__main__":
    main()