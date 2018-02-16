# Speech recognition setup


# Todo 2
- Servos
    - servo control with pigpio
    - service
    - publisher
- Speech recognition
    - Create small dict / lm
    - send audio to PC and do full dictionary speech processing
- Dialogue system

# ROS:

## How to ROS
- Topic: node publishes messages, node subscribed to a topic can receive these messages
- Services: A client node sends a request (what is 2+1?) to a Service node, the service node sends a response(2+1=3) back to the client
- Parameters: rosparam can be used to set, get, load, dump, delete and list parameters (e.g. intialization paramters).

## install catkin packages
- `source /opt/ros/kinetic/setup.bash`
- `cd /home/fedya/Desktop/robot/Robot-v2/catkin_ws`
- `catkin_make`
- `source catkin_ws/devel/setup.bash`

### camera packages
## Raspberry pi camera package 1
- https://github.com/UbiquityRobotics/raspicam_node
- `roscore`
- `roslaunch raspicam_node camerav2_1280x960.launch` or other launch file
- `rqt_image_view`

## raspberry pi camera package 2
- https://github.com/fpasteau/raspicam_node
- `roscore`
- `rosrun raspicam raspicam_node`
- `rosrun image_view image_view image:=/camera/image _image_transport:=compressed`


## Setup ROS connection on two devices (same network):
- enable ssh on both
- generate a ssh key if not already present on both
- put public key of either in ~/.ssh/authorized_keys of other
- If your users have the same name on both devices, skip this step. Otherwise: Define on each computer in the ssh config file as which user needs to be logged in when sshing to a certain host
    - `sudo nano /etc/ssh/ssh_config`
    - Add for instance (and save):
        - host fedya-rpi.local
        - hostname fedya-rpi.local
        - user fedya
    - Restart ssh to load changes: `sudo systemctl restart ssh`
    - Set enviromental variables of Raspberry Pi robot:
        - `export ROS_MASTER_URI=http://fedya-rpi.local:11311`
        - `export ROS_IP=[ip_of_rpi]`
    - Set enviromental variables of pc
        - `export ROS_MASTER_URI=http://fedya-rpo.local:11311`
        - `export ROS_IP=[IP_OF_PC -> NOT OF RPI]`
    - To make it easier you can put this stuff in ~/.bashrc so they are exported automatically for new terminals:
        - `export ROS_PACKAGE_PATH=/home/tjalling/Desktop/robot/Robot-v2/catkin_ws:$ROS_PACKAGE_PATH`
        - also add ROS_MASTER_URI and ROS_IP


- http://wiki.ros.org/ROS/NetworkSetup
- http://wiki.ros.org/ROS/Tutorials/MultipleMachinese
```
rpi:
ip: 192.168.178.68
hostname: fedya-rpi
user: fedya
password: kutraspberry
Command: ssh fedya@fedya-rpi.local

laptop:
hostname: tjalling-Lenovo-G780
ip: 192.168.178.66
user: tjalling
password: kutlinux
Command: ssh tjalling@tjalling-Lenovo-G780.local
```

### Topic publisher / Subscriber
- copy listener and talker from beginner_tutorials/scripts
- chmod +x file_name.py (for both files)
- roscore
- rosrun package_name listener.py/talker.py or listener/talker(for cpp)





# Hardware
## Parts:
- Raspberry pi 2b
- 2 V-tec 6v 177 RPM DC motors with double hall encoders (https://eckstein-shop.de/V-TEC-6V-Mini-25D-DC-Motor-Getriebe-Motor-Stirnradgetriebe-mit-Encoder-177-RPM-EN)
- 2 Pololu Wheel 90×10mm Pair - Black
- SN754410 H-bridge for DC motor control
- Castor/ ball wheel
- 2 Hitec HS-422 180 degree servo's with pan-tilt set
- Raspberry pi v2 camera mounted on pan-tilt set
- 3 HC-SR04 sonars, 1 mounted on pan-tilt set, 2 mounted at front at a 20°.
- Xiaomi 10000 mAh powerbank for rpi
- 3300 mAh NiMh battery for servos / dc motors
- 2 Pinout boards
- Pinout cables
 Wiring GPIO

## Wiring

### DC motors
- sn75 flipped to right, pins mentioned are BCM pin numbers
- BCM pin 23 - sn75 left 7
- BCM pin 24 - sn75 left 1
- BCM pin 10 - sn75 right 7
- BCM pin 9 - sn75 right 8
- BCM pin 25 - sn75 left 2
- BCM pin 11 - sn75 right 2
- Pin 2 (5v) - sn75 right 1
- Connect 6v external power to pinout board
- Connect pinout board + (6v) to sn75 left 8
- Pinout board ground to RPI ground
- Pinout board ground to: sn75 left 4 / 5 / sn75 right 4 / 5 (all 4)
- DC motor 1 (right) red cable (says m1 on motor) sn75 right 3
- DC motor 1 (right) white cable (says m2 on motor) to sn75 right 6
- DC motor 2 (left) red cable (says m1 on motor) to sn75 left 3
- DC motor 2 (left) white cable (says m2 on motor) to sn75 left 6

### DC motors encoder wiring
- 3v3 from rpi (pin 1) to pinout board (not same side as 6v)
- ground from rpi to pinout board
- 3v3 input pins from encoders to pinout board +
- ground pins from encoders to pinout board ground
- Right motor encoder output 1 green (says cm2 on motor) to BCM pin 17
- Right motor encoder output 2 yellow (says cm1 on motor) to BCM pin 27
- Left motor encoder ouput 1 green (says cm2 on motor) to BCM pin 14
- Left motor encoder ouput 2 yellow (says cm1 on motor) to BCM pin 15

Encoder: 1362 for 102cm = 1335 ticks per meter

### Head Servos
#### Servo 1: (vertical servo)
- Black: Ground pinout board
- Red: 6v on pinout board
- Yellow: BCM pin 13

#### Servo 2: (horizontal servo)
- Black: Ground pinout board
- Red: 6v on pinout board
- Yellow: BCM pin 18

### Ultrasound sonars
- 5v to pinout board + (extra row)
- Rpi ground to pinout ground
- See [this link](https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi) for the setup of the resistors

##  Sonar 1 (head)
- Ground to pinout ground
- Vcc to pinout +
- Trigger to BCM 20
- Echo to pinout board see link
- Pinout board cable between resistors to BCM 21 (echo)

## Sonar 2 (front left as seen from robot)
- Same as Sonar 1 except for Echo
- Echo to pinout board see link
- Trigg to BCM 5
- Pinout board cable between resistors to BCM 6 (echo)

## Sonar 3 (front right)
- Same as Sonar 1 except for Echo
- Echo to pinout board see link
- Trigg to BCM 19
- Pinout board cable between resistors to BCM 26 (echo)

# Software:

## Requirements
- ROS on RPI (I used Ubuntu 16.04 + ROS)
- pigpio for python
- wiringpi for python
