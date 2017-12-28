#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
import motors

motors = False
leftWheelSpeed = False
rightWheelSpeed = False

def setup():
    global motors
    motors = motors.initialize_default_motors()

def cleanup():
    motors.cleanup_motors(motors)

def leftWheel(speed):
    rospy.loginfo(rospy.get_caller_id() + 'Left wheel cmd %d', speed.data)

    set_wheel_speed(motors[1], speed)
    global leftWheelSpeed
    if speed.data != leftWheelSpeed:
        global
        set_wheel_speed(motors[1], speed.data)
        leftWheelSpeed = speed.data


def rightWheel(speed):
    rospy.loginfo(rospy.get_caller_id() + 'Right wheel cmd %d', speed.data)

    global rightWheelSpeed
    if speed.data != rightWheelSpeed:
        global
        set_wheel_speed(motors[0], speed.data)
        rightWheelSpeed = speed.data



def listener():
    rospy.init_node('wheelListener', anonymous=True)

    rospy.Subscriber('lmotor', Int16, leftWheel)
    rospy.Subscriber('rmotor', Int16, rightWheel)

    rospy.spin()


if __name__ == '__main__':
    setup()
    listener()
    cleanup()
