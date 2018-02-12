#!/usr/bin/env python
import sys
import rospy
from time import sleep
from rpi_robot.srv import *
from std_msgs.msg import String

# use default synth defined in launch file
synthType = rospy.get_param("/speech/TTSdef")

# Text to speech client
def TTSclient(text, speechsynth):
    rospy.wait_for_service('TextToSpeech')
    try:
        TTSobj = rospy.ServiceProxy('TextToSpeech', TTS)
        resp1 = TTSobj(text, speechsynth)
        return resp1.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


# add speech to the dialogue log
def addToDialogueLog(user, text):
    dialogueLog = rospy.get_param("/speech/dialogueLog", [])
    dialogueLog.append([user, rospy.get_time(), text])
    rospy.set_param('/speech/dialogueLog', dialogueLog)


def execute(command):
    print "Processing command:", command

    if command == "turn left":
        print "turn left"
    elif command == "turn right":
        print "turn right"


# listen to recognized speech
def main():
    rospy.init_node('dialogue', anonymous=True)

    # initialize dialogue log to an empty list
    rospy.set_param('/speech/dialogueLog', [])

    while not rospy.is_shutdown():

        print "Requesting speech"
        # Speak text and make sure we don't recognize our own text by reseting the last recognized word
        TTSclient("Hello, human, please give me a command.", synthType)

        print "log 1:"
        print rospy.get_param("/speech/dialogueLog")

        sleep(3.0)
        print "Reset last speech recognized",  rospy.get_time()

        # get response from user
        rospy.set_param('/speech/lastSpeechRecognized', "")
        latestSpeech = rospy.get_param('/speech/lastSpeechRecognized')
        while latestSpeech == "":
            sleep(1)
            latestSpeech = rospy.get_param('/speech/lastSpeechRecognized')


        # Save latest recognized speech to dialogue
        addToDialogueLog("user1", latestSpeech)

        print "log 2:"
        print rospy.get_param("/speech/dialogueLog")

        # confirm speech to user
        TTSclient("I heard you say: " + latestSpeech, synthType)

        print "log 3:"
        print rospy.get_param("/speech/dialogueLog")

        # execute command
        execute(latestSpeech)

        return True




if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
