#!/usr/bin/env python

import rospy
from std_msgs.msg import Int16
import encoder

def publishTicks():
    # init encoder
    pi = pigpio.pi()
    encoder = init_left_encoder(pi)

    # init node
    pub = rospy.Publisher('lwheel', Int16, queue_size=10)
    rospy.init_node('lwheelTicks', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():

        data = "left ticks: %d" % encoder.ticks
        rospy.loginfo(data)
        pub.publish(encoder.ticks)
        rate.sleep()

    # cleanup encoder
    encoder.cancel()
    pi.stop()

if __name__ == '__main__':
    try:
        publishTicks()
    except rospy.ROSInterruptException:
        pass
