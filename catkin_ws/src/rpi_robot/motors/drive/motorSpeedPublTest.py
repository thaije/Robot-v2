#!/usr/bin/env python


import rospy
from std_msgs.msg import Int16
import time

def talker():
    pub = rospy.Publisher('lmotor', Int16, queue_size=10)
    rospy.init_node('wheelTester', anonymous=True)
    # rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        # hello_str = "testing wheel world %s" % rospy.get_time()
        # rospy.loginfo(hello_str)
        pub.publish(50)
        time.sleep()
        pub.publish(0)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
