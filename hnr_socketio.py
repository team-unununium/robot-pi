import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

# TODO: Functions

@sio.event
def disconnect():
    print("Disconnected from server")

def start():
    sio.connect("https://unununium-vr-server.herokuapp.com/")
    sio.wait()

def stop():
    pass