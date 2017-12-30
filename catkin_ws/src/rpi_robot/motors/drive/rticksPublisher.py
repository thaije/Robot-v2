#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
import encoder

def publishTicks():
    # init encoder
    pi = pigpio.pi()
    enc = encoder.init_right_encoder(pi)

    # init node
    pub = rospy.Publisher('rwheel', Int16, queue_size=10)
    rospy.init_node('rwheelTicks', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():

        data = "right ticks: %d" % enc.ticks
        rospy.loginfo(data)
        pub.publish(enc.ticks)
        rate.sleep()

    # cleanup encoder
    enc.cancel()
    pi.stop()

if __name__ == '__main__':
    try:
        publishTicks()
    except rospy.ROSInterruptException:
        pass
