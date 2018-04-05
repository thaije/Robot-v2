#!/usr/bin/env python
import sys, time
import numpy as np
import cv2
import roslib
import rospy
import rospkg

# Ros Messages
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

rospack = rospkg.RosPack()
path = rospack.get_path('rpi_robot') + "/vision/"

face_cascade = cv2.CascadeClassifier(path + 'opencv_files/haarcascade_frontalface_default.xml')
# face_alt_cascade = cv2.CascadeClassifier(path + 'opencv_files/haarcascade_frontalface_alt.xml')
# profile_face_cascade = cv2.CascadeClassifier(path + 'opencv_files/haarcascade_profileface.xml')
# eye_cascade = cv2.CascadeClassifier(path + 'opencv_files/haarcascade_eye.xml')
# smile_cascade = cv2.CascadeClassifier(path + 'opencv_files/haarcascade_smile.xml')
left_eye_cascade = cv2.CascadeClassifier(path + 'opencv_files/haarcascade_lefteye_2splits.xml')
right_eye_cascade = cv2.CascadeClassifier(path + 'opencv_files/haarcascade_righteye_2splits.xml')


def faceDetection(img):

    # detect faces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    face_detected = False

    for (x,y,w,h) in faces:
        face_detected = True
        cv2.rectangle(img,(x,y),(x+w,y+h),faceColor,2)

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

    # if not face_detected:
    #     # search complete img for eyes
    #     eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    #     for (ex,ey,ew,eh) in eyes:
    #         cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    # search complete img for profile
    # profile = profile_face_cascade.detectMultiScale(gray, 1.3, 5)
    # for (ex,ey,ew,eh) in profile:
    #     cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,0,0),2)

    # # Display the resulting img
    # cv2.imshow('img', img)
    # cv2.waitKey(2)

    if face_detected:
        return faces

    return False


def getFaceCenter(faceID):
    [x, y, w, h] = faces[faceID]
    [midX, midY] = x + 0.5 * w, y + 0.5 * h
