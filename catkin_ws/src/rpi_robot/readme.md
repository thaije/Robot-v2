# Teleoperation

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
