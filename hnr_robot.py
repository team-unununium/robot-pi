import logging

logger = logging.getLogger("Robot module")

# TODO: Complete RobotProgram
class RobotProgram:
    def __init__(self):
        logger.info("Robot program initialized")

    def start(self):
        logger.info("Robot program started")

    def stop(self):
        logger.info("Robot program stopped")

    def rotate(self, data):
        logger.info("Robot starting to rotate")

    def startMoving(self):
        logger.info("Robot starting to move")

    def stopMoving(self):
        logger.info("Robot is now stopping")

    def requestData(self):
        logger.info("Full data requested from robot")

if __name__ == "__main__":
    logger.critical("Module hnr_robot ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")