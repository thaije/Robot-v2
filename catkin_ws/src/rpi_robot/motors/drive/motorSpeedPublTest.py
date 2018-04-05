#!/usr/bin/env python


import rospy
from std_msgs.msg import Float32
import time

def talker():
    pub_l = rospy.Publisher('lmotor_cmd', Float32, queue_size=10)
    pub_r = rospy.Publisher('rmotor_cmd', Float32, queue_size=10)
    rospy.init_node('wheelTester', anonymous=True)

    while not rospy.is_shutdown():
        print "Forward"
        pub_l.publish(100.0)
        pub_r.publish(100.0)
	time.sleep(1)

        print "Backward"
        pub_l.publish(-70.0)
	pub_r.publish(-70.0)
        time.sleep(1)

        pub_l.publish(0.0)
	pub_r.publish(0.0)
        print "Done"
        break



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
