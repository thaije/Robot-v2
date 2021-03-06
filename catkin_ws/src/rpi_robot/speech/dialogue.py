#!/usr/bin/env python
import sys
import rospy
from time import sleep
from rpi_robot.srv import *
from std_msgs.msg import String
from geometry_msgs.msg import Twist


# use default synth defined in launch file
synthType = rospy.get_param("/speech/TTSdef")
pub = False

# Text to speech client
# TODO: move this to TTS folder and import
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
        TTSclient("My body is 2 years old, but I am mature for my age.", synthType)
        TTSclient("How old are you?", synthType)

    if command == "turn left":
        TTSclient("Turning left", synthType)
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0;
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = -1.0
		pub.publish(twist)

    elif command == "turn right":
        TTSclient("Turning right", synthType)
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0;
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 1.0
		pub.publish(twist)



def init():
    rospy.init_node('dialogue', anonymous=True)

    global pub
    pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

    # initialize dialogue log to an empty list
    rospy.set_param('/speech/dialogueLog', [])



# listen to recognized speech
def main():
    TTSclient("Hello, human", synthType)

    while not rospy.is_shutdown():

        print "Requesting speech"
        # Speak text and make sure we don't recognize our own text by reseting the last recognized word
        TTSclient("How can I help you?", synthType)
        sleep(1.0)

        print "log 1:"
        print rospy.get_param("/speech/dialogueLog")

        # enable conversational speech recognition
        rospy.set_param('/speech/speechRecognitionMode', 1)

        # get response from user
        rospy.set_param('/speech/lastSpeechRecognized', "")
        latestSpeech = rospy.get_param('/speech/lastSpeechRecognized')
        while latestSpeech == "" and not rospy.is_shutdown():
            sleep(1)
            latestSpeech = rospy.get_param('/speech/lastSpeechRecognized')

        # disable speech recognition
        rospy.set_param('/speech/speechRecognitionMode', 0)

        # Save latest recognized speech to dialogue
        addToDialogueLog("user1", latestSpeech)

        # confirm speech to user
        rospy.loginfo( "I heard you say: \"" + latestSpeech + "\"" )
        TTSclient("I heard you say: " + latestSpeech, synthType)

        # execute command
        execute(latestSpeech)

        sleep(2.0)




if __name__ == "__main__":
    try:
        init()
        main()
    except rospy.ROSInterruptException:
        pass
