# Robot-v2

## Usefull links
[Raspberry PI pinout](https://pinout.xyz/)
[Image processing with Opencv on RPI](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_table_of_contents_imgproc/py_table_of_contents_imgproc.html)



## RPI setup:
Parts:
- 2 HItec HS-442 servos mounted on eachother to get 2 DOF
- pi camera v2
- external battery for servos

Pin setup:
- verticalServo BCM pin=13
- horizontalServo BCM pin=18
- external battery to breadboard
- servo power to breadboard
- RPI ground to breadboard (important!)


# settings:
Ubuntu login
User fedya
Login kutraspberry

ssh: `ssh fedya@192.168.178.68`
password: `kutraspberry`

# ROS:
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

- http://wiki.ros.org/ROS/NetworkSetup
- http://wiki.ros.org/ROS/Tutorials/MultipleMachines
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
