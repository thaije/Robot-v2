#!/usr/bin/env python
from time import sleep

import rospy
from geometry_msgs.msg import Twist

def talker():
    pub = rospy.Publisher('twist', Twist, queue_size = 1)
    rospy.init_node('wheelTesterTwist', anonymous=True)

    tw = createTwist(0, 90)
    print tw

    index = 0

    seconds = 0.2
    hz = 50

    r = rospy.Rate(hz)
    while not rospy.is_shutdown():
        pub.publish(tw)
        r.sleep()

        index += 1
        if index == seconds * hz:
            break



def createTwist(x, th):
    print "Twist with linX %d, angX %d" % (x, th)

    twist = Twist()
    twist.linear.x = x
    twist.linear.y = 0
    twist.linear.z = 0
    twist.angular.x = 0
    twist.angular.y = 0
    twist.angular.z = th
    return twist


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
