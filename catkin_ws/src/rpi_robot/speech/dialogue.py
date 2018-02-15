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

    if "old" in command:
        # print "how old do you think I am?
        TTSclient("My body is 2 years old, but I am mature for my age", synthType)
        TTSclient("How old are you?")

    if command == "turn left":
        print "turn left"
    elif command == "turn right":
        print "turn right"


# listen to recognized speech
def main():
    rospy.init_node('dialogue', anonymous=True)

    # initialize dialogue log to an empty list
    rospy.set_param('/speech/dialogueLog', [])
    TTSclient("Hello, human", synthType)

    while not rospy.is_shutdown():

        print "Requesting speech"
        # Speak text and make sure we don't recognize our own text by reseting the last recognized word
        TTSclient("Please give me a command.", synthType)

        print "log 1:"
        print rospy.get_param("/speech/dialogueLog")

        # # block the speechrecognition while the robot is speaking
        # while rospy.get_param('/speech/robotSpeaking') and not rospy.is_shutdown():
        #     sleep(0.5)

        # the speech recognizer
        # sleep(1.0)
        # rospy.loginfo( "Robot done talking + 1s delay" )



        # get response from user
        latestSpeech = rospy.get_param('/speech/lastSpeechRecognized')
        while latestSpeech == "" and not rospy.is_shutdown():
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
