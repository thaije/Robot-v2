# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.vflip = True
# camera.brightness = 60
camera.resolution = (640, 480)
camera.framerate = 2
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# capture frames from the camera
# for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    image = frame.array

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # define range of green color in HSV
    # lower_blue = np.array([0,50,50])
    # upper_blue = np.array([30,255,255])
    # lower_blue = np.array([50,50,50])
    # upper_blue = np.array([70,255,255])
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)


    # open and closing to reduce noise
    # http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html#morphological-ops
    kernel = np.ones((2,2),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(image, image, mask= mask)

    # cv2.imshow('frame',image)
    # cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    # canny edge detection
    # edges = cv2.Canny(image,100,200)
    # cv2.imshow('edges', edges)




    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    # https://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv/
    # ball tracking?

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
