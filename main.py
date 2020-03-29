from dotenv import load_dotenv
load_dotenv()

import logging
import requests
import signal

# Set up logging
logging.basicConfig(filename="robot.log", filemode="w", level=logging.INFO, format="%(asctime)s: %(name)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %I:%M:%S %p")
logger = logging.getLogger('Main')

import hnr_settings as settings
settings.init()
import hnr_socketio as SocketProgram

# Graceful exit from SIGINT
def signal_handler(sig, frame):
    logger.info("SIGINT detected, shutdown initiated")
    if settings.programRunning:
        settings.sio.disconnect()
        settings.firmataProgram.stop()
        settings.cameraProgram.stop()
        settings.programRunning = False
    raise SystemExit
signal.signal(signal.SIGINT, signal_handler)

def main():
    logger.info("Main program started")
    logger.debug(f"GUID is {settings.GUID}, server URL is {settings.SERVER_URL}, server-robot secret is {settings.SERVER_ROBOT_SECRET}")

    # Get Access token
    req_json = {
        "guid": settings.GUID,
        "secret": settings.SERVER_ROBOT_SECRET
    }
    req_response = requests.post(f"{settings.SERVER_URL}/access", json=req_json)
    req_code = req_response.status_code
    req_success = False

    # Request response handling
    if req_code == 201:
        settings.ACCESS_TOKEN = req_response.json()['token']
        logger.info("Access token request successful")
        logger.debug(f"Access token is {settings.ACCESS_TOKEN}")
        req_success = True
    elif req_code == 400:
        logger.error("Access token request failed with error code 400 (Incorrect parameters)")
    elif req_code == 401:
        logger.error("Access token request failed with error code 401 (Another robot already exists)")
    elif req_code == 403:
        logger.error("Access token request failed with error code 403 (The GUID has been taken)")
    elif req_code == 500:
        logger.error("Access token request failed with error code 500 (Error occured while attempting to query database)")
    else:
        logger.error(f"Access token request failed with unexpected error code {req_code}")

    if req_success:
        settings.socketProgram = SocketProgram
        settings.socketProgram.start()
    else:
        print("An error occured while getting the access token. Please check the logs for more information.")
        logger.info("Program shutdown due to unable to get the access token")
        raise SystemExit
                
if __name__ == "__main__":
    main()