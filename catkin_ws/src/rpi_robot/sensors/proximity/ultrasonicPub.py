#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range

import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24

# measurement variables
maximumRange = 3.6
minimumRange = 0.0
range_msg = Range()

def setup():
    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    range_msg.radiation_type = Range.ULTRASOUND
    range_msg.field_of_view = 0.1 # fake
    range_msg.min_range = minimumRange
    range_msg.max_range = maximumRange


def getRangeUltrasound():
    # Trigger for 0.01ms
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        pulseStart = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        pulseEnd = time.time()

    # time difference between start and arrival
    pulseDuration = pulseEnd - pulseStart

    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    print "pulse duration:", pulseDuration
    distance = (pulseDuration * 17150 / 100)
    distance = round(distance,2)

    return distance

def talker():
    pub = rospy.Publisher('chatter', Range, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(20) # 10hz

    setup()

    i = 0
    while not rospy.is_shutdown():
        range_msg.range = getRangeUltrasound()
        i += 0.1
        hello_str = "hello world %s %0.3f" % (rospy.get_time(), range_msg.range)
	rospy.loginfo(hello_str)
        pub.publish(range_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
