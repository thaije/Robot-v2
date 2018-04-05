#!/usr/bin/env python
import sys, time
import numpy as np
import cv2
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

# other functions
from tracking import *
import faceDetection as faceD

# how to run:
# on rpi:
# roscore
# rosrun raspicam raspicam_node _framerate:=2
# rosservice call /camera/start_capture

# on pc:
# rosrun rpi_robot objectDetection.py


class image_feature:
    def __init__(self):
        '''Initialize ros subscriber'''
        # subscribed Topic
        self.subscriber = rospy.Subscriber("/camera/image/compressed",
            CompressedImage, self.callback,  queue_size = 1)
        print "subscribed to /camera/image/compressed"


    def callback(self, ros_data):
        '''Callback function of subscribed topic.
        Here images get converted and features detected'''

        #### direct conversion to CV2 ####
        np_arr = np.fromstring(ros_data.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        img = cv2.flip( img, 0 )
        img = cv2.flip( img, 1 )
        height, width, channels = img.shape

        # check for faces, and track
        faces = faceD.faceDetection(img, draw=True)
        if faces != ():
            print "Found face"
            # track face
            # [midX, midY] = faceD.getCenterCoords(faceID=0)


        # Display the resulting img
        cv2.imshow('img',img)
        cv2.waitKey(2)


def main(args):
    # '''Initializes servos, opencv and ros node'''
    # global ver_servo, hor_servo, wheels
    # ver_servo = rospy.Publisher('ver_servo', Float32, queue_size=1)
    # hor_servo = rospy.Publisher('hor_servo', Float32, queue_size=1)
    #
    # print "starting up publishers.."
    # time.sleep(1)

    ic = image_feature()
    rospy.init_node('object_detection', anonymous=True)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image object detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
