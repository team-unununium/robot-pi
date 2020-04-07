from aiortc import RTCIceCandidate, RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from av import VideoFrame
from io import BytesIO
from threading import Thread
from picamera import PiCamera, PiCameraError

import logging
import numpy
import time

import hnr_settings as settings

logger = logging.getLogger("Camera Module")

class CameraProgram:
    def __init__(self):
        logger.info("Camera program initiated")
        self.working = True
        self.called = False
        try:
            # Initialize camera
            self.camera = PiCamera()
            self.camera.resolution = settings.RESOLUTION
            self.camera.framerate = settings.FRAMERATE

            # Initialize streaming variables
            self.stream = BytesIO()
            self.currentFrame = numpy.empty((self.camera.resolution[1], self.camera.resolution[0], 3), dtype=numpy.uint8) # The 1 and 0 needs to be this way due to how numpy does its stuff
            print(self.currentFrame.shape)

            # Initialize aiortc variables
            self.rtcPeerConnection = RTCPeerConnection()
            self.peerList = []

            self.recordingThread = Thread(target=self.recordVid)
        except PiCameraError as e:
            logger.error(f"Camera program initiation failed with error message '{str(e)}'")
            self.working = False

    def recordVid(self):
        if self.working:
            logger.info("Recording thread started")
            # Warm up camera before starting the recording
            self.camera.start_preview()
            time.sleep(2)

            # Start of recording loop
            while self.recording:
                for foo in self.camera.capture_continuous(self.stream, 'jpeg', use_video_port=True):
                    if not self.recording:
                        break
                    self.stream.truncate()
                    self.stream.seek(0)
                    # In case the value is changed in the middle of the processing thread
                    currentFrame = self.stream.getvalue()
                    Thread(target=self.uploadFrame, args=[currentFrame]).start()
        else:
            logger.warning("Camera program is not working, cannot start recording thread")
            print("An error occured while attempting to start the recording thread. Please check the logs for more information.")
    
    def uploadFrame(self, currentFrame):
        # Testing with Twitch streaming for now
        pass

    def start(self):
        if self.working:
            logger.info("Camera program started")
            self.recording = True
            self.recordingThread.start()
        else:
            logger.warning("Camera program is not working, cannot start program")
            print("An error occured while attempting to start the Camera program. Please check the logs for more information.")

    def stop(self):
        if self.working:
            logger.info("Camera program stopped")
            self.recording = False
            self.recordingThread.join()
        else:
            logger.warning("Camera program is not working (already stopped)")

    def addPeer(self, peer):
        if self.working:
            logger.info("A peer has been successfully added")
            self.peerList.append(peer)
            # TODO: Add peer
        else:
            logger.warning("Camera program is not working, cannot add peer")
            print("An error occured while attempting to add a peer. Please check the logs for more information.")

    def removePeer(self, peer):
        if self.working:
            try:
                logger.info("A peer has been successfully removed")
                self.peerList.remove(peer)
                # TODO: Remove peer
            except ValueError:
                logger.warning(f"Invalid peer {str(peer)} received to be removed")
        else:
            logger.warning("Camera program is not working, cannot remove peer")
            print("An error occured while attempting to remove a peer. Please check the logs for more information.")

if __name__ == "__main__":
    logger.critical("Module hnr_camera ran as program, exiting")
    raise RuntimeError("This file is a module and should not be run as a program")