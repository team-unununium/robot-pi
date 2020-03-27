from io import BytesIO
from picamera import PiCamera
import logging

class CameraProgram:
    def __init__(self):
        logging.info("Camera program initiated")
        self.stream = BytesIO()
        self.camera = PiCamera()

    # TODO: Complete

if __name__ == "__main__":
    logging.critical("Module hnr_camera ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")