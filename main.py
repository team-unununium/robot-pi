from dotenv import load_dotenv
from threading import Thread
import socketio
import uuid

from hnr_camera import CameraProgram
from hnr_firmata import FirmataProgram
import hnr_socketio as SocketProgram

# Initialize certain variables before starting program
load_dotenv()
GUID = str(uuid.uuid4()) # GUID does not need to be stored as server does not double check
sio = socketio.Client()

def main():
    # TODO: Complete
    SocketProgram.start()
    pass
                
if __name__ == "__main__":
    main()