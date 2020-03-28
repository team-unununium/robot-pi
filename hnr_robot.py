import logging

# TODO: Complete RobotProgram
class RobotProgram:
    def __init__(self):
        logging.info("Robot program initialized")

    def start(self):
        logging.info("Robot program started")

    def rotate(self, data):
        logging.info("Robot starting to rotate")

    def startMoving(self):
        logging.info("Robot starting to move")

    def stopMoving(self):
        logging.info("Robot is now stopping")

    def requestData(self):
        logging.info("Full data requested from robot")

if __name__ == "__main__":
    logging.critical("Module hnr_robot ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")