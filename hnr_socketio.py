from os import environ
from main import sio, GUID

SERVER_URL = environ.get("SERVER_URL")
SERVER_ROBOT_SECRET = environ.get("SERVER_ROBOT_SECRET")
if SERVER_URL is None or SERVER_ROBOT_SECRET is None:
    raise ValueError("SERVER_URL and SERVER_ROBOT_SECRET should be provided as environment variable")

def start():
    print(f"Current server is {SERVER_URL}")
    sio.connect(SERVER_URL)
    sio.wait()

@sio.event
def connect():
    print("Connected to server, authenticating")

# TODO: Functions

@sio.event
def disconnect():
    print("Disconnected from server")

if __name__ == "__main__":
    raise RuntimeError("This file is a module and should not be run as a program")