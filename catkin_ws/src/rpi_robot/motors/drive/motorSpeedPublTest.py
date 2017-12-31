#!/usr/bin/env python


import rospy
from std_msgs.msg import Int16
import time

def talker():
    pub = rospy.Publisher('lmotor_cmd', Int16, queue_size=10)
    rospy.init_node('wheelTester', anonymous=True)

    while not rospy.is_shutdown():
        print "Forward"
        pub.publish(70)
        time.sleep(1)
        print "Backward"
        pub.publish(0)
        print "Done"
        break



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
