from io import BytesIO
from picamera import PiCamera

class CameraProgram:
    def __init__(self):
        self.stream = BytesIO()
        self.camera = PiCamera()

    # TODO: Complete

if __name__ == "__main__":
    raise RuntimeError("This file is a module and should not be run as a program")