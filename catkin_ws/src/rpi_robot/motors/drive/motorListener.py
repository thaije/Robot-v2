#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import motors as motorControl
import time

motors = False
leftWheelSpeed = False
rightWheelSpeed = False

def setup():
    global motors
    motors = motorControl.initialize_default_motors()

def cleanup():
    motorControl.cleanup_motors(motors)

def leftWheel(speed):
    rospy.loginfo(rospy.get_caller_id() + ' Left wheel cmd %d', speed.data)

    global leftWheelSpeed
    if speed.data != leftWheelSpeed:
	motorControl.set_wheel_speed(motors[0], speed.data)
        leftWheelSpeed = speed.data


def rightWheel(speed):
    rospy.loginfo(rospy.get_caller_id() + ' Right wheel cmd %d', speed.data)

    global rightWheelSpeed
    if speed.data != rightWheelSpeed:
        motorControl.set_wheel_speed(motors[1], speed.data)
        rightWheelSpeed = speed.data



def listener():
    rospy.init_node('wheelListener', anonymous=True)

    rospy.Subscriber('lmotor_cmd', Float32, leftWheel)
    rospy.Subscriber('rmotor_cmd', Float32, rightWheel)

    rospy.spin()


if __name__ == '__main__':
    setup()
    try:
        listener()
    except KeyboardInterrupt:
	       print "interrupted by user"
    finally:
    	print "cleaning up"
    	cleanup()
