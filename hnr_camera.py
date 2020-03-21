from io import BytesIO
from picamera import PiCamera

class CameraProgram:
    def __init__(self):
        self.stream = BytesIO()
        self.camera = PiCamera()

    # TODO: Complete
