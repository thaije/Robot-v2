# Teleoperation

- `catkin_make`
- `chmod +x file.py`

## Method 1: differential_drive + teleop_twist_keyboard
- Install ROS teleop_twist_keyboard
- git clone ROS differential_drive package
- run roscore on RPi
- `roslaunch rpi_robot diff_drive_rpi.launch` on rpi
- `roslaunch rpi_robot diff_drive_pc.launch` on pc
- control with keyboard on pc such as described in the print of roslaunch


# camera:
See https://github.com/UbiquityRobotics/raspicam_node
https://github.com/fpasteau/raspicam_node



# Servos

facedetection -> pub
Send a command every frame

Servolistener -> sub
Listen to every command and execute immediately

ServoPWM
SetPosition(pos)
smallWait
Set to 0


Conclusions:
Servos are set to 0, so smallWait is executed
The facedetection sends a new servo command -> while previous servo command hasn't been completed yet -> new servo command based on old image

Todo:
Find out if servolistener calls ServoPWM in parallel / overwrites previous command, or if they are called sequentially and wait for previous to finish
    -> make test servo publisher, which calls servoPWM -> do large movement with very small smallWait
    -> if servo doesn't make complete movement, servoPWM calls overwrite eachother
    ---> Sensor changes are executed sequentially, but don't overwrite eachother.
Problem is object tracking specific, test by adding a block to new command dependent on delta to facedetection.py
    -> potentially: add ignoreNewCommandsFrom service to servolistener, to ignore servo commands from specific source
