#!/usr/bin/env python


import rospy
from std_msgs.msg import Float32
import time

def talker():
    pub = rospy.Publisher('lmotor_cmd', Float32, queue_size=10)
    rospy.init_node('wheelTester', anonymous=True)

    while not rospy.is_shutdown():
        print "Forward"
        pub.publish(70.0)
        time.sleep(1)

        print "Backward"
        pub.publish(-70.0)
        time.sleep(1)

        pub.publish(0.0)
        print "Done"
        break



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
