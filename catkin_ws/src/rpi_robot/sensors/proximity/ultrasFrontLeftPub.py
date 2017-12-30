#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Range

import RPi.GPIO as GPIO
import time

# ultrasound sensor left

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 5
GPIO_ECHO = 6

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
    
    pulseStart = -1
    pulseEnd = -1

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
    distance = (pulseDuration * 17150 / 100)
    distance = round(distance,2)

    return distance

def talker():
    pub = rospy.Publisher('ultrasonicLeft', Range, queue_size=10)
    rospy.init_node('ultrasonicLeft', anonymous=True)
    rate = rospy.Rate(20) # 10hz

    setup()

    while not rospy.is_shutdown():
        range_msg.range = getRangeUltrasound()
        ultr_str = "Ultrasonic front left distance %0.3f at time %s" % (range_msg.range, rospy.get_time())
        rospy.loginfo(ultr_str)
        pub.publish(range_msg)
        rate.sleep()
    GPIO.cleanup()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
