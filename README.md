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
The Raspberry Pi module is in charge of facilitating communication between the Arduino and the server. It uses [picamera](https://picamera.readthedocs.io/) and [python-socketio](https://python-socketio.readthedocs.io/). The full list of requirements can be found in requirements.txt. It also provides the live video feed to the clients through a public livestream on Twitch. The identity of the raspberry pi is confirmed by the server through a common secret, which is the `SERVER_ROBOT_SECRET`. The communication protocol between the Raspberry Pi and the Arduino can be found in [diagram.uml](https://github.com/team-unununium/HnR-2020-VR-Pi/blob/master/diagram.uml) and [arduino_protocol.png](https://github.com/team-unununium/HnR-2020-VR-Pi/blob/master/arduino_protocol.png).

The following image is the protocol for communicating between the Raspberry Pi and the Arduino:
![Protocol UML](https://plantuml.pcchin.com/png/jP91ImCn48Nl-HNFWxKhjJ-Wi691H3neQVKcGknEky5i9cpIIX7zxKwsMwpRNZnuMZPvxyqta_6wZcPkl7OHuxfO6SVAxvrDZ5AE8u7NLEyK0paUOMmjvbnLsXK1kYO44eCE2COjhVnkgbUs0Gkk4JnHWHv81ubQm5JUKYLw7GqxfV8SivZAkYNoN4qCBYvtrKOuGV-MhELi3oKHF9OaNxmR8NaZyWXwanBA94RaPnT5qSPWvQAnC14r1Sy2hNOtKYl5_PHfUCW58R_MKHz1ka9V10KgWfRggKve3E4CXLYoRhWOcYYPc20EK6e1ZMPPnWFf1svMadatUxXlil3PLVJQi8Ln9fHK_29-ycAYnDnndQBVtgKdAVwPPigl75kOS6I2N-SomlJcg7Wj49aQ3eSpakLBXErYoT61BzdO_z7rWlwKjzksxSAuRUzPLtcatuxYeDzl "Protocol for Pi-Arduino communication")

## Progress
- [x] Main Program
- [x] Socket.IO Module
- [x] Arduino Module (Untested)
- [x] Settings Module

## How to install
After cloning the repository, just run  `pip3 install -r requirements.txt` then set up the following environment variables:
- `SERVER_URL`: The URL for the server module that the robot connects to.
- `SERVER_ROBOT_SECRET`: The secret used to verify the robot's identity with the server, this variable should be the same on the server module as well.

Some optional environment variables include:
- `INPUT_PIN`: A string for the input pin for the robot to listen from, defaults to d:0:i.
- `OUTPUT_PIN`: A string for the output pin for the robot to write to, defaults to d:0:o.

After that, just run `python main.py` and you should be good to go!
If you wish to transmit a livestream to the clients through Twitch, you would need to use an external script to do so. The link for the script that is currently being used by us can be found [here](https://gist.githubusercontent.com/russfeld/0878b1f8eaf7409136b9125ce5e1458f/raw/62824c1021f816a13046f1aba7722b8ac519c28d/picam-stream.sh).

## Installation notes
- The output of the program is sent to a `robot.log` file in the same directory as main.py, so the program may fail if the directory is not writable by the program. Thus, no output would appear on the console itself except for certain error messages.
- To shut down the program, you would need to send a SIGINT (Keyboard Interrupt) to it.
- For the environment variables, you may choose to input it with the command or set up a .env file in the project's root directory for the environment variables to be read. 
- As the module requires a live video feed, a camera module would need to be attached to the Raspberry Pi for the module to function.
- The port that the robot listens from and writes to are automatically assumed to be digital ports.

# If you wish to help

## Contributing
Any contribution is welcome, feel free to add any issues or pull requests to the repository.

## Licenses
This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).
