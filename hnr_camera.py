from io import BytesIO
from picamera import PiCamera
import logging

# TODO: Complete CameraProgram
class CameraProgram:
    def __init__(self):
        logging.info("Camera program initiated")
        self.stream = BytesIO()
        self.camera = PiCamera()

    def start(self):
        logging.info("Camera program started")

    def addPeer(self, peer):
        logging.info("A peer has been successfully added")

    def removePeer(self, peer):
        logging.info("A peer has been successfully removed")

if __name__ == "__main__":
    logging.critical("Module hnr_camera ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")