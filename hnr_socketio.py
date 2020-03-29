import logging
import requests

from hnr_camera import CameraProgram
from hnr_firmata import FirmataProgram
from hnr_robot import RobotProgram
import hnr_settings as settings

logger = logging.getLogger("Socket Module")

def start():
    logger.info("Initiated Socket.IO connection with server")
    settings.sio.connect(settings.SERVER_URL)
    settings.sio.wait()

    # Anything after this should not be accessible as the program should pause indefinitely at settings.sio.wait()
    logger.warning("Unable to connect to server through Socket.IO, deleting client data from database then exiting")
    req_json = {
        "guid": settings.GUID,
        "token": settings.ACCESS_TOKEN
    }
    req_response = requests.delete(f"{settings.SERVER_URL}/access", json=req_json)
    req_code = req_response.status_code

    # Request response handling
    if req_code == 204:
        logger.info("Deletion request successful, client data deleted from database")
    elif req_code == 400:
        logger.error("Deletion request failed with error code 400 (Incorrect parameters)")
    elif req_code == 404:
        logger.error("Deletion request failed with error code 404 (Client could not be found)")
    elif req_code == 500:
        logger.error("Deletion request failed with error code 500 (Error occured while attempting to query database)")
    else:
        logger.error(f"Deletion request failed with unknown error code {req_code}")
    print("An error occured while connecting to the Socket.IO server. Please check the logs for more information.")

def sendSessionInfo(data):
    settings.sio.emit("robotSendSessettings.sionInfo", data)

def updateData(data):
    settings.sio.emit("robotSendSessettings.sionInfo", data)

@settings.sio.event
def connect():
    logger.info("Socket.IO connection with server established, authenticating")
    settings.sio.emit("authentication", { 
        "guid": settings.GUID,
        "token": settings.ACCESS_TOKEN
    })

@settings.sio.event
def authenticated(data):
    logger.info("Authentication successful, starting the Arduino and PiCamera modules")
    settings.firmataProgram = FirmataProgram()
    settings.firmataProgram.start()

    settings.cameraProgram = CameraProgram()
    settings.cameraProgram.start()

    settings.robotProgram = RobotProgram()
    settings.robotProgram.start()

@settings.sio.event
def unauthorized(data):
    # No further action needed as server should disconnect within a few seconds
    logger.error(f"Unauthorized to connect to server through Socket.IO, message is {data['message']}")

@settings.sio.event
def robotAddPeer(data):
    logger.info("Received request to add peer")
    settings.cameraProgram.addPeer(data)

@settings.sio.event
def robotRemovePeer(data):
    logger.info("Received request to remove peer")
    settings.cameraProgram.addPeer(data)

@settings.sio.event
def robotAddMultiplePeers(dataList):
    logger.info("Received request to add multiple peers")
    if isinstance(dataList, list):
        for data in dataList:
            settings.cameraProgram.addPeer(data)
    else:
        logger.warning(f"Data provided to add multiple peers is of type {type(dataList)} instead of the expected list")

@settings.sio.event
def robotRotate(data):
    logger.info("Received request to rotate robot")
    settings.robotProgram.rotate(data)

@settings.sio.event
def robotStartMoving(data):
    logger.info("Received request to start moving robot")
    settings.robotProgram.startMoving()

@settings.sio.event
def robotStopMoving(data):
    logger.info("Received request to stop moving robot")
    settings.robotProgram.stopMoving()

@settings.sio.event
def robotRequestUpdateAll():
    settings.robotProgram.requestData()

@settings.sio.event
def disconnect():
    logger.info("Disconnected from server")

if __name__ == "__main__":
    logger.critical("Module hnr_socketio ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")