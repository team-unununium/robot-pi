import logging
import requests

from hnr_camera import CameraProgram
from hnr_firmata import FirmataProgram
from hnr_robot import RobotProgram
from hnr_settings import sio
import hnr_settings as settings

def start():
    logging.info("Initiated Socket.IO connection with server")
    sio.connect(settings.SERVER_URL)
    sio.wait()

    # Anything after this should not be accessible as the program should pause indefinitely at sio.wait()
    logging.warning("Unable to connect to server through Socket.IO, deleting client data from database then exiting")
    req_json = {
        "guid": settings.GUID,
        "token": settings.ACCESS_TOKEN
    }
    req_response = requests.delete(f"{settings.SERVER_URL}/access", json=req_json)
    req_code = req_response.status_code

    # Request response handling
    if req_code == 204:
        logging.info("Deletion request successful, client data deleted from database")
    elif req_code == 400:
        logging.error("Deletion request failed with error code 400 (Incorrect parameters)")
    elif req_code == 404:
        logging.error("Deletion request failed with error code 404 (Client could not be found)")
    elif req_code == 500:
        logging.error("Deletion request failed with error code 500 (Error occured while attempting to query database)")
    else:
        logging.error(f"Deletion request failed with unknown error code {req_code}")
    print("An error occured while connecting to the Socket.IO server. Please check the logs for more information.")

def sendSessionInfo(data):
    sio.emit("robotSendSessionInfo", data)

def updateData(data):
    sio.emit("robotSendSessionInfo", data)

@sio.event
def connect():
    logging.info("Socket.IO connection with server established, authenticating")
    sio.emit("authentication", { 
        "guid": settings.GUID,
        "token": settings.ACCESS_TOKEN
    })

@sio.event
def authenticated(data):
    logging.info("Authentication successful, starting the Arduino and PiCamera modules")
    settings.firmataProgram = FirmataProgram()
    settings.firmataProgram.start()

    settings.cameraProgram = CameraProgram()
    settings.cameraProgram.start()

    settings.robotProgram = RobotProgram()
    settings.robotProgram.start()

@sio.event
def unauthorized(data):
    # No further action needed as server should disconnect within a few seconds
    logging.error(f"Unauthorized to connect to server through Socket.IO, message is {data['message']}")

@sio.event
def robotAddPeer(data):
    logging.info("Received request to add peer")
    settings.cameraProgram.addPeer(data)

@sio.event
def robotRemovePeer(data):
    logging.info("Received request to remove peer")
    settings.cameraProgram.addPeer(data)

@sio.event
def robotAddMultiplePeers(dataList):
    logging.info("Received request to add multiple peers")
    if isinstance(dataList, list):
        for data in dataList:
            settings.cameraProgram.addPeer(data)
    else:
        logging.warning(f"Data provided to add multiple peers is of type {type(dataList)} instead of the expected list")

@sio.event
def robotRotate(data):
    logging.info("Received request to rotate robot")
    settings.robotProgram.rotate(data)

@sio.event
def robotStartMoving(data):
    logging.info("Received request to start moving robot")
    settings.robotProgram.startMoving()

@sio.event
def robotStopMoving(data):
    logging.info("Received request to stop moving robot")
    settings.robotProgram.stopMoving()

@sio.event
def robotRequestUpdateAll():
    settings.robotProgram.requestData()

@sio.event
def disconnect():
    logging.info("Disconnected from server")

if __name__ == "__main__":
    logging.critical("Module hnr_socketio ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")