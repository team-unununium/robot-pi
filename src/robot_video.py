from io import BytesIO
from threading import Thread
from picamera import PiCamera
import logging
import struct
import time

import src.robot_settings as settings

logger = logging.getLogger("Video Stream")

class VideoProgram:
    def __init__(self):
        logger.info("Video program initiated")
        self.working = False # Whether the module is up and running
        self.dataThread = Thread(target=self.videoThread)
        self.camera = PiCamera()

    def start(self):
        if self.working:
            try:
                logger.info("Video program started")
                self.working = True
                self.dataThread.start()
            except Exception as e:
                logger.error(f"ICE handshake failed with the following error: {str(e)}")
                print("An error occured while attempting to start the video program. Please check the logs for more information.")
                self.working = False
        else:
            logger.warning(f"Video program is not working, cannot start program")
            print("An error occured while attempting to start the video program. Please check the logs for more information.")

    # Main data handler
    def videoThread(self):
        self.camera.start_preview()
        time.sleep(2) # Waiting time for camera to start up
        while self.working:
            bufferStart = time.time()
            stream = BytesIO()
            bufferBytes = bytes()
            # From Basic Recipe 8 from picamera
            for foo in self.camera.capture_continuous(stream, 'jpeg'):
                # Write the length of the capture to the stream and flush to
                # ensure it actually gets sent
                bufferBytes += struct.pack('<L', stream.tell())
                # Rewind the stream and send the image data over the wire
                stream.seek(0)
                bufferBytes += stream.read()
                # If we've been capturing for more than 30 seconds, quit
                if time.time() - bufferStart > settings.BUFFER_DURATION:
                    break
                # Reset the stream for the next capture
                stream.seek(0)
                stream.truncate()
            bufferBytes += struct.pack('<L', 0)
            settings.socketProgram.sendVideoFootage(bufferBytes)

    def stop(self):
        if self.working:
            logger.info("Video program stopped")
            self.working = False
        else:
            logger.warning(f"Video program is not working (already stopped)")

if __name__ == "__main__":
    logger.critical("Module robot_video ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")
