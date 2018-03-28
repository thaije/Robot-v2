#!/usr/bin/env python
from std_msgs.msg import Float32
import roslib
import rospy

import sys, time

# Test the servo listener by publishing servo commands quickly after eachother



ver_servo = False
hor_servo = False


def main():
    rospy.init_node('servo_test', anonymous=True)

    ver_servo = rospy.Publisher('ver_servo', Float32, queue_size=1)
    hor_servo = rospy.Publisher('hor_servo', Float32, queue_size=1)

    # let node startup
    time.sleep(2)
    print "starting"

    counter = 0
    hor_servo.publish(64)
    # while not rospy.is_shutdown() and counter < 3:
    #     hor_servo.publish(1000)
    #     print "right"
    #     time.sleep(0.5)
    #
    #     hor_servo.publish(-1000)
    #     print "left"
    #     time.sleep(0.5)
    #
    #     counter += 1

# 65 ticks per 10percent


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
