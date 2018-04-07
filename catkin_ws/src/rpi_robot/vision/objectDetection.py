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
import tracking
import faceDetection as faceD

ver_servo = False
hor_servo = False

# how to run:
# on rpi:
# roslaunch rpi_robot diff_drive_rpi.launch
# roslaunch rpi_robot vision_rpi.launch

# on pc:
# roslaunch rpi_robot diff_drive_pc.launch
# roslaunch rpi_robot vision_pc.launch


class image_feature:
    def __init__(self):
        # Initialize ros subscriber
        self.subscriber = rospy.Subscriber("/camera/image/compressed",
            CompressedImage, self.callback,  queue_size = 1)
        rospy.loginfo("Subscribed to /camera/image/compressed")


    def callback(self, ros_data):
        '''Callback function of subscribed topic.
        Here images get converted and features detected'''

        # convert input stream to OpenCV image
        np_arr = np.fromstring(ros_data.data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        img = cv2.flip( img, 0 )
        img = cv2.flip( img, 1 )
        height, width, channels = img.shape

        # check for faces, and track
        faces = faceD.faceDetection(img, draw=True)
        if faces != ():
            rospy.loginfo("Face detected")
            # track face
            [midX, midY] = faceD.getFaceCenter(faces, faceID=0)
            tracking.centerOnObject(midX, midY, width, height, ver_servo, hor_servo)

        # Display the resulting img
        cv2.imshow('img',img)
        cv2.waitKey(2)


def main(args):
    # Initialize servos
    global ver_servo, hor_servo
    ver_servo = rospy.Publisher('ver_servo', Float32, queue_size=1)
    hor_servo = rospy.Publisher('hor_servo', Float32, queue_size=1)

    rospy.loginfo("Starting up servo publishers..")
    time.sleep(1)

    # start up image processing
    ic = image_feature()
    rospy.init_node('object_detection', anonymous=True)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image object detector module"
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
