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
## install package
- `source /opt/ros/kinetic/setup.bash`
- `cd /home/fedya/Desktop/robot/Robot-v2/catkin_ws`
- `catkin_make`

## run package
- `roscore`