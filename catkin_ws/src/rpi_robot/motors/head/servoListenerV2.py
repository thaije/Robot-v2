#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist
import servoPWM as servoControl
from time import sleep

servos = False
wheels = False
hz = 30
r = 1.0 / hz
seconds = 0.3


# Listens for commands to change the servos to a certain position, commands are
# relative to the current position

def setup():
    global servos
    servos = servoControl.initialize_default_servos()

def cleanup():
    servoControl.cleanup_servos(servos)

def verticalServo(pos):
    rospy.loginfo(rospy.get_caller_id() + ' vertical servo pos %d, horizontal servo pos %d' % (pos.verticalServo, pos.horizontalServo))

    servosCommand = [-1, -1]

    # only process a valid motor command
    if pos.verticalServo != 0:
        # calc new servo position (relative from previous)
        (minPos, maxPos) = servos[0].getMinMax()
        oldPos = servos[0].getPosition()
        newPos = oldPos + pos.verticalServo
        # servos[0].setPosition(newPos)
        servosCommand[0] = newPos

        trackingMode = rospy.get_param("/vision/trackingMode")
        # if tracking mode is passive or active, move wheels when servo is at max pos
        if trackingMode > 0:
            if newPos > maxPos:
                rospy.loginfo("Move wheels till robot has turned 180 degrees")
                # twist = createTwist(80, -80)


    # only process a valid motor command
    if pos.horizontalServo != 0:
        # calc and set new servo position
        (minPos, maxPos) = servos[1].getMinMax()
        oldPos = servos[1].getPosition()
        newPos = oldPos + pos.data

        #TODO: only move wheels if past max position
        trackingMode = rospy.get_param("/vision/trackingMode")
        if trackingMode == 0:
            # servos[1].setPosition(newPos)
            servosCommand[1] = newPos

        # if tracking mode is passive or active, move wheels when servo is at max pos
        # and don't move the servo
        else:
            if newPos < minPos:
                delta = minPos - newPos
                twist = createTwist(0, 80)
                rospy.loginfo("Move wheels left")

                index = 0
                # publish motor commands for x seconds
                while not rospy.is_shutdown():
                    wheels.publish(twist)
                    index += 1
                    if index == seconds * hz:
                        break
                    sleep(r)
                # servos[1].setPosition(oldPos + 75)

            elif newPos > maxPos:
                delta = newPos - maxPos
                twist = createTwist(0, -80)
                rospy.loginfo("Move wheels right")

                index = 0
                # publish motor commands for x seconds
                while not rospy.is_shutdown():
                    wheels.publish(twist)
                    index += 1
                    if index == seconds * hz:
                        break
                    sleep(r)
                # servos[1].setPosition(oldPos - 75)
            else:
                # servos[1].setPosition(newPos)
                servosCommand[1] = newPos


def createTwist(x, th):
    twist = Twist()
    twist.linear.x = x
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = th
    return twist


def listener():
    global wheels

    rospy.init_node('servoListener', anonymous=True)
    rospy.Subscriber('ver_servo', Float32, verticalServo, queue_size=1)
    rospy.Subscriber('hor_servo', Float32, horizontalServo, queue_size=1)
    wheels = rospy.Publisher('twist', Twist, queue_size = 1)

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
