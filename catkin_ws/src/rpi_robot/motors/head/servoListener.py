#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
import servoPWM as servoControl
import time

servos = False

def setup():
    global servos
    servos = servoControl.initialize_default_servos()

def cleanup():
    servoControl.cleanup_servos(servos)

def verticalServo(pos):
    rospy.loginfo(rospy.get_caller_id() + ' vertical servo pos %d', pos.data)
    oldPos = servos[0].getPosition()
    servos[0].setPosition(oldPos + pos.data)


def horizontalServo(pos):
    rospy.loginfo(rospy.get_caller_id() + ' horizontal servo pos %d', pos.data)
    oldPos = servos[1].getPosition()
    servos[1].setPosition(oldPos + pos.data)


def listener():
    rospy.init_node('servoListener', anonymous=True)
    rospy.Subscriber('ver_servo', Float32, verticalServo)
    rospy.Subscriber('hor_servo', Float32, horizontalServo)
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
