from dotenv import load_dotenv
load_dotenv()

import logging
import platform
import requests
import signal

# Set up logging (Do not output to console)
if platform.system() == "Windows":
    logging.basicConfig(filename="NUL", level=logging.INFO)
else:
    # MacOS and Linux both have /dev/null
    logging.basicConfig(filename="/dev/null", level=logging.INFO)
formatter = logging.Formatter(fmt="%(asctime)s: %(name)s - %(levelname)s: %(message)s", datefmt="%d-%m-%Y %I:%M:%S %p")

# Info level only filter
class InfoOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == "INFO"

# Separate info loggers from the rest
log_error = logging.FileHandler("robot-error.log", "w+")
log_error.setLevel(logging.WARNING)
log_error.setFormatter(formatter)
log_info = logging.FileHandler("robot-info.log", "w+")
log_info.setLevel(logging.INFO)
log_info.setFormatter(formatter)
log_info.addFilter(InfoOnlyFilter())

logging.getLogger('').addHandler(log_error)
logging.getLogger('').addHandler(log_info)
logger = logging.getLogger("Main")

# User defined modules
import src.robot_settings as settings
settings.init()
import src.robot_socketio as SocketProgram
import src.robot_video as VideoProgram

# Graceful exit from SIGINT
def signal_handler(sig, frame):
    logger.info("SIGINT detected, shutdown initiated")
    if settings.programStarted:
        settings.sio.disconnect()
        settings.arduinoProgram.stop()
        settings.programStarted = False
    raise SystemExit
signal.signal(signal.SIGINT, signal_handler)

# Main program start
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
        settings.videoProgram = videoProgram
        settings.videoProgram.start()
    else:
        print("An error occured while getting the access token. Please check the logs for more information.")
        logger.info("Program shutdown due to unable to get the access token")
        raise SystemExit
                
if __name__ == "__main__":
    main()