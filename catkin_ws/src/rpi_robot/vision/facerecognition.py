#!/usr/bin/env python


import sys, time
import numpy as np
import cv2
import roslib
import rospy

# Ros Messages
from sensor_msgs.msg import CompressedImage

# how to run:
# on rpi:
# roscore
# rosrun raspicam raspicam_node
# rosservice call /camera/start_capture
# rosrun rpi_robot servoListener.py

# on pc:
# rosrun rpi_robot facerecognition.py



resX = 640
resY = 480

face_cascade = cv2.CascadeClassifier('opencv_files/haarcascade_frontalface_default.xml')
face_alt_cascade = cv2.CascadeClassifier('opencv_files/haarcascade_frontalface_alt.xml')
profile_face_cascade = cv2.CascadeClassifier('opencv_files/haarcascade_profileface.xml')
eye_cascade = cv2.CascadeClassifier('opencv_files/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('opencv_files/haarcascade_smile.xml')
left_eye_cascade = cv2.CascadeClassifier('opencv_files/haarcascade_lefteye_2splits.xml')
right_eye_cascade = cv2.CascadeClassifier('opencv_files/haarcascade_righteye_2splits.xml')

ver_servo = False
hor_servo = False

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
        height, width, channels = img.shape

        # cv2.imshow('cv_img', img)
        # cv2.waitKey(2)

        # detect faces
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        face_detected = False
        for (x,y,w,h) in faces:
            face_detected = True
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

            # search region of interest (face) for eyes
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = img[y:y+h, x:x+w]
            # eyes = eye_cascade.detectMultiScale(roi_gray)

            # eyes = eye_cascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in eyes:
            #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            left_eye = left_eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in left_eye:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(51,153,255),2)

            right_eye = right_eye_cascade.detectMultiScale(roi_gray)
            for (ex,ey,ew,eh) in right_eye:
                cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(51,255,255),2)

            # smiles = smile_cascade.detectMultiScale(roi_gray)
            # for (ex,ey,ew,eh) in smiles:
            #     cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,0,255),2)

        if not face_detected:
            # search complete img for eyes
            eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
            for (ex,ey,ew,eh) in eyes:
                cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

        # search complete img for profile
        # profile = profile_face_cascade.detectMultiScale(gray, 1.3, 5)
        # for (ex,ey,ew,eh) in profile:
        #     cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,0,0),2)


        if face_detected:
            [x, y, w, h] = faces[0]
            [midX, midY] = x + 0.5 * w, y + 0.5 * h
            centerOnFace(midX, midY, width, height)

        # Display the resulting img
        cv2.imshow('img',img)
        cv2.waitKey(2)


# center on middle 20%
def centerOnFace(midX, midY, width, height):
    global ver_servo, hor_servo

    offset = 0.1

    if midX > width * (0.5 + offset):
        hor_servo.pub(-100)
    elif midX < width * (0.5 - offset):
        hor_servo.pub(100)

    if midY > height * (0.5 + offset):
        ver_servo.pub(-100)
    elif midY < height * (0.5 - offset):
        ver_servo.pub(100)


def main(args):
    '''Initializes and cleanup ros node'''
    ic = image_feature()
    rospy.init_node('face_detection', anonymous=True)

    global ver_servo, hor_servo
    ver_servo = rospy.Publisher('ver_servo', Float32, queue_size=10)
    hor_servo = rospy.Publisher('hor_servo', Float32, queue_size=10)

    try:
        rospy.spin()
    except KeyboardInterrupt:
        print "Shutting down ROS Image feature detector module"
    cv2.destroyAllWindows()
    head.cleanup_servos(servos)

if __name__ == '__main__':
    main(sys.argv)
