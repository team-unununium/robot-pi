import logging
import requests

from hnr_arduino import ArduinoProgram
import hnr_settings as settings
from hnr_settings import sio

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
    # The event may fire multiple times
    if settings.arduinoProgram is None:
        settings.arduinoProgram = arduinoProgram()
        settings.arduinoProgram.start()
    settings.programRunning = True

@settings.sio.event
def unauthorized(data):
    # No further action needed as server should disconnect within a few seconds
    logger.error(f"Unauthorized to connect to server through Socket.IO, message is {data['message']}")
    settings.disconnectCount += 1
    if settings.disconnectCount == 10:
        logger.error("Socket connection has been rejected 10 times, exiting")
        print("An error occured in establishing a connection to the Socket.IO server. Please check the logs for more information.")
        sio.disconnect()

@settings.sio.event
def robotRotateCamera(data):
    if settings.programRunning:
        logger.info("Received request to rotate robot camera")
        settings.arduinoProgram.rotateCamera(data)
    else:
        logger.warning("Received request to rotate robot camera but Arduino program is not running")

@settings.sio.event
def robotRotate(data):
    if settings.programRunning:
        logger.info("Received request to rotate robot")
        settings.arduinoProgram.rotate(data)
    else:
        logger.warning("Received request to rotate robot but Arduino program is not running")

@settings.sio.event
def robotStartMoving(data):
    if settings.programRunning:
        logger.info("Received request to start moving robot")
        settings.arduinoProgram.startMoving()
    else:
        logger.warning("Received request to start moving robot but Arduino program is not running")

@settings.sio.event
def robotStopMoving(data):
    if settings.programRunning:
        logger.info("Received request to stop moving robot")
        settings.arduinoProgram.stopMoving()
    else:
        logger.warning("Received request to stop moving robot but Arduino program is not running")

@settings.sio.event
def robotChangeSpeed(data):
    if settings.programRunning:
        logger.info("Received request to change the velocity of the robot")
        settings.arduinoProgram.changeSpeed(data)
    else:
        logger.warning("Received request to change the velocity of the robot but Arduino program is not running")

@settings.sio.event
def disconnect():
    logger.info("Disconnected from server")

if __name__ == "__main__":
    logger.critical("Module hnr_socketio ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")