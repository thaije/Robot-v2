#!/usr/bin/env python
import sys, time
import numpy as np
import roslib
import rospy


# Ros Messages
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32



# how much servoticks do you need to move for the image to move 1% = 7
servoticks_per_img_perc = 6
# defines the middle of the screen where correction isn't needed, in percentage of image
# is used for up, right, down and left
face_offset = 0.1
# defines how long to block image processing after servo movement, usefull for higher framerates
# secs_per_100 = 0.01

# Center the object in the image, with the servo change relative to the
# distance of the center
def centerOnObject(midX, midY, width, height, ver_servo, hor_servo):
    # trackingMode = rospy.get_param("/vision/trackingMode")

    err = 0
    movedTicks = 0

    right = midX > ( width * (0.5 + face_offset) )
    left = midX < ( width * (0.5 - face_offset) )
    up = midY < ( height * (0.5 - face_offset) )
    down = midY > ( height * (0.5 + face_offset) )

    # check if we need to move horizontally
    if right or left:
        # blockedImageProcessing = True
        if right: # is right
            err = ( width * (0.5 + face_offset) ) - midX
            rospy.loginfo("Object is " + str(err) + " right from center")
        else: # is left
            err = ( width * (0.5 - face_offset) ) - midX
            rospy.loginfo("Object is " + str(err) + " left from center")

        # calc error
        err_percentage = (-err / float(width)) * 100
        adj = err_percentage * servoticks_per_img_perc
        rospy.loginfo("Err percent of object is:" + str(err_percentage) + " -> adjust:" + str(adj) + " ticks")

        hor_servo.publish(adj)
        movedTicks = abs(adj)

    # check if we need to move vertically
    if up or down:
        blockedImageProcessing = True
        if down: # is down
            err = ( height * (0.5 + face_offset) ) - midY
            rospy.loginfo("Object is " + str(err) + " down from center")
        else: # is up
            err = ( height * (0.5 - face_offset) ) - midY
            rospy.loginfo("Object is " + str(err) + " up from center")

        # calc error
        err_percentage = (err / float(width)) * 100
        adj = err_percentage * servoticks_per_img_perc
        rospy.loginfo("Err percent of object is:" + str(err_percentage) + " -> adjust:" + str(adj) + " ticks")

        ver_servo.publish(adj)

        # track the largest servo movement
        if abs(adj) > movedTicks:
            movedTicks = abs(adj)

    # If the head was moved, block following image processing for a certain period
    # if movedTicks > 0:
    #     waitFor = abs(movedTicks / 100.0) * secs_per_100
    #     print "Servo moved %d ticks, waiting for: %.2f seconds\n" % (movedTicks, waitFor)
    #     # block image processing based based on the largest servo movement done
    #     rospy.Timer(rospy.Duration(waitFor), unblockImageProcessing, oneshot=True)
