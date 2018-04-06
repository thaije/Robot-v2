#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import servoPWM as servoControl
import time

servos = False
wheels = False

def setup():
    global servos
    servos = servoControl.initialize_default_servos()

def cleanup():
    servoControl.cleanup_servos(servos)

def verticalServo(pos):
    rospy.loginfo(rospy.get_caller_id() + ' vertical servo pos %d', pos.data)

    # calc new servo position
    (minPos, maxPos) = servos[0].getMinMax()
    oldPos = servos[0].getPosition()
    newPos = oldPos + pos.data
    servos[0].setPosition(newPos)

    trackingMode = rospy.get_param("/speech/trackingMode")
    # if tracking mode is passive or active, move wheels when servo is at max pos
    if trackingMode > 0:
        if newPos > maxPos:
            rospy.loginfo("Move wheels till robot has turned 180 degrees")
            # twist = createTwist(80, -80)



def horizontalServo(pos):
    rospy.loginfo(rospy.get_caller_id() + ' horizontal servo pos %d', pos.data)

    # calc and set new servo position
    (minPos, maxPos) = servos[1].getMinMax()
    oldPos = servos[1].getPosition()
    newPos = oldPos + pos.data
    servos[1].setPosition(newPos)


    trackingMode = rospy.get_param("/speech/trackingMode")
    # if tracking mode is passive or active, move wheels when servo is at max pos
    if trackingMode > 0:
        if newPos < minPos:
            delta = minPos - newPos
            rospy.loginfo("Move wheels left")
            # twist = createTwist(80, -80)

        elif newPos > maxPos:
            delta = newPos - maxPos
            rospy.loginfo("Move wheels right")
            # twist = createTwist(-80, 80)


def createTwist(left, right):
    twist = Twist()
    twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
	twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = th*turn
    return twist


def listener():
    global wheels

    rospy.init_node('servoListener', anonymous=True)
    rospy.Subscriber('ver_servo', Float32, verticalServo, queue_size=1)
    rospy.Subscriber('hor_servo', Float32, horizontalServo, queue_size=1)
    wheels = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

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
