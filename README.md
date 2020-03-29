# H&R 2020 - VR Robot Explorer
 **[Our Devpost](https://devpost.com/software/hnr2020-vr-robot)**

This is basically a robot which is controlled by VR. The robot has two cameras and some sensors which are used to give users data about the environment the robot is in. Input from the camera and sensors is displayed on the VR headset. The clients can rotate their headset, which will cause the robot's camera to rotate in the same direction, and by touching the side button of the headset, the robot will start or stop moving.

The project consists of 4 main modules: The client, server, Raspberry Pi and Arduino. All 4 modules communicate with each other either directly or through another module to ensure that the robot functions as expected.

## Module list
 - [Client Module](https://github.com/team-unununium/HnR-2020-VR-Client)
 - [Server Module](https://github.com/team-unununium/HnR-2020-VR-Server)
 - [Raspberry Pi Module](https://github.com/team-unununium/HnR-2020-VR-Pi)
 - [Arduino Module](https://github.com/team-unununium/HnR-2020-VR-Arduino)

# Current module - Raspberry Pi
The Raspberry Pi module is in charge of facilitating communication between the Arduino and the server. It uses [picamera](https://picamera.readthedocs.io/), [python-socketio](https://python-socketio.readthedocs.io/) and [pyFirmata2](https://github.com/berndporr/pyFirmata2). The full list of requirements can be found in requirements.txt. It also provides the live video feed to the clients. The identity of the raspberry pi is confirmed by the server through a common secret, which is the `SERVER_ROBOT_SECRET`.

## Progress
- [x] Main Program
- [x] Socket.IO Module
- [ ] Camera Module
- [ ] Firmata Module
- [ ] Robot Module
- [x] Settings Module

## How to install
Before cloning the repository, you need to install the following dependencies (outside of pip3) on your system due to [aiortc](https://github.com/aiortc/aiortc)'s requirements:
- OpenSSL 1.0.2 or greater
- FFmpeg 4.0 or greater
- LibVPX for video encoding / decoding
- Opus for audio encoding / decoding

For more information on aiortc's dependencies, visit their [repository page](https://github.com/aiortc/aiortc) for more information.

After cloning the repository, just run  `pip3 install -r requirements.txt` then set up the following environment variables:
- `SERVER_URL`: The URL for the server module that the robot connects to.
- `SERVER_ROBOT_SECRET`: The secret used to verify the robot's identity with the server, this variable should be the same on the server module as well.

Some optional environment variables include:
- `RESOLUTION`: A tuple representing the resolution of the camera, defaults to 480p (640 * 480).
- `FRAMERATE`: An integer representing the frame rate of the camera, defaults to 30 fps.

After that, just run `python main.py`  and you should be good to go!
 
## Installation notes
- The output of the program is sent to a `robot.log` file in the same directory as main.py, so the program may fail if the directory is not writable by the program. Thus, no output would appear on the console itself except for certain error messages.
- To shut down the program, you would need to send a SIGINT (Keyboard Interrupt) to it.
- For the environment variables, you may choose to input it with the command or set up a .env file in the project's root directory for the environment variables to be read. 
- As the module requires a live video feed, a camera module would need to be attached to the Raspberry Pi for the module to function.

# If you wish to help

## Contributing
Any contribution is welcome, feel free to add any issues or pull requests to the repository.

## Licenses
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
