from io import BytesIO
from threading import Thread
from picamera import PiCamera
import logging
import time

import src.robot_settings as settings

logger = logging.getLogger("Video Stream")

class VideoProgram:
    def __init__(self):
        logger.info("Video program initiated")
        self.working = True # Whether the module is up and running
        self.dataThread = Thread(target=self.videoThread)
        self.camera = PiCamera()

    def start(self):
        if self.working:
            logger.info("Video program started")
            self.dataThread.start()
        else:
            logger.warning(f"Video program is not working, cannot start program")
            print("An error occured while attempting to start the video program. Please check the logs for more information.")

    # Main data handler
    def videoThread(self):
        self.camera.start_preview()
        time.sleep(1) # Waiting time for camera to start up
        self.camera.stop_preview()
        self.camera.resolution = (settings.CAMERA_WIDTH, settings.CAMERA_HEIGHT)
        self.camera.framerate = settings.CAMERA_FPS
        stream = BytesIO()
        while self.working:
            self.camera.start_recording(stream, format='h264', quality=21)
            self.camera.wait_recording(settings.BUFFER_DURATION)
            self.camera.stop_recording()
            stream.seek(0)
            bufferBytes = stream.read()
            stream.seek(0)
            stream.truncate()
            Thread(target=self.sendFootage, args=(bufferBytes,)).start()

    def sendFootage(self, bufferBytes):
        if settings.socketProgram is not None:
            settings.socketProgram.sendVideoFootage(bufferBytes)

    def stop(self):
        if self.working:
            self.working = False
            logger.info("Video program stopped")
        else:
            logger.warning(f"Video program is not working (already stopped)")

if __name__ == "__main__":
    logger.critical("Module robot_video ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")
