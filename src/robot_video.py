import logging
from av import VideoFrame

import src.robot_settings as settings

logger = logging.getLogger("Video Stream")

class VideoProgram:
    def __init__(self):
        logger.info("Video program initiated")
        self.working = True # Whether the module is up and running

    def start(self):
        if self.working:
            logger.info("Video program started")
        else:
            logger.warning(f"Video program is not working, cannot start program")
            print("An error occured while attempting to start the video program. Please check the logs for more information.")

    def stop(self):
        if self.working:
            logger.info("Video program stopped")
            self.working = False
        else:
            logger.warning(f"Video program is not working (already stopped)")
