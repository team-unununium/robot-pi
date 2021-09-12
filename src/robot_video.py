from io import BytesIO
from threading import Thread, Condition
from picamera import PiCamera
import logging
import time

import src.robot_settings as settings

logger = logging.getLogger("Video Stream")

# https://randomnerdtutorials.com/video-streaming-with-raspberry-pi-camera/
class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = BytesIO()
        self.condition = Condition()
    
    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class VideoProgram:
    def __init__(self):
        logger.info("Video program initiated")
        self.working = True # Whether the module is up and running
        self.dataThread = Thread(target=self.videoThread)
        self.output = StreamingOutput()
        try:
            self.camera = PiCamera()
        except Exception as e:
            logger.warning("Unable to retrieve PiCamera, maybe camera is not connected?")
            print("An error occured while attempting to start the video program. Please check the logs for more information.")
            self.working = False

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
        self.camera.start_recording(self.output, format='mjpeg')
        while True:
            self.frame = None
            with self.output.condition:
                self.output.condition.wait()
                self.frame = self.output.frame
            settings.socketProgram.sendVideoFootage(self.frame)

    def stop(self):
        if self.working:
            self.working = False
            self.camera.stop_recording()
            logger.info("Video program stopped")
        else:
            logger.warning(f"Video program is not working (already stopped)")

if __name__ == "__main__":
    logger.critical("Module robot_video ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")
