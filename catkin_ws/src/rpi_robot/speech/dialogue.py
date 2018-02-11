#!/usr/bin/env python
import sys
import rospy
from time import sleep
from rpi_robot.srv import *
from std_msgs.msg import String

synthType = "flite"

# Text to speech client
def TTSclient(text, speechsynth):
    rospy.wait_for_service('TextToSpeech')
    try:
        TTSobj = rospy.ServiceProxy('TextToSpeech', TTS)
        resp1 = TTSobj(text, speechsynth)
        return resp1.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def command(text):
    print "Processing command:", text

    if text == "go left":
        print "go left"
    elif text == "go right":
        print "go right"


# listen to recognized speech
def main():
    rospy.init_node('dialogue', anonymous=True)

    while not rospy.is_shutdown():
        print "Requesting speech"
        TTSclient("Hello, human. Please give me a command.", synthType)
        return True

        latestSpeech = False
        command = False

        #TODO: get command from parameter server
        while not latestSpeech:
            sleep(1.0)

        # Confirm recognized speech
        command = latestSpeech
        latestSpeech = False
        TTSclient("I heard you say: " + command, synthType)

        # execute command
        execute(command)



if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
