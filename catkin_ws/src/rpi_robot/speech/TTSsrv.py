#!/usr/bin/env python
import rospy
from rpi_robot.srv import *
import speechSynths
from time import sleep


def unblockSpeech(event):
    # reset last recognized speech
    rospy.loginfo( "Reset last speech recognized.")
    rospy.set_param('/speech/lastSpeechRecognized', "")

    # unblock speech, or not if the robot is talking
    if not rospy.get_param('/speech/robotSpeaking'):
        rospy.loginfo( "Unblocked speech recognition \n" )
        rospy.set_param('/speech/blockSpeechRecognition', False)
    else:
        rospy.loginfo( "Failed to unblock STT, robot speaking")


def handleTTS(req):
    speechsynth = req.speechsynth
    response = True

    rospy.loginfo( "New speech command: \"" + req.text + "\"")
    rospy.loginfo( "Using speechsynth: " + speechsynth)

    # Announce that we are going to speak to the rest of the system, and block STT
    rospy.set_param('/speech/robotSpeaking', True)
    rospy.set_param('/speech/blockSpeechRecognition', True)

    # Speak the text with the requested speechsynth if it exists
    if speechsynth == "espeak":
        speechSynths.espeak(req.text)
    elif speechsynth == "festival":
        speechSynths.festival(req.text)
    elif speechsynth == "flite":
        speechSynths.flite(req.text)
    else:
        response = False
    rospy.loginfo( "Done speaking \n" )

    # we are done speaking, reset system variable
    rospy.set_param('/speech/robotSpeaking', False)

    # update latest spoken speech to dialogue log
    dialogueLog = rospy.get_param("/speech/dialogueLog", [])
    dialogueLog.append(["self", rospy.get_time(), req.text])
    rospy.set_param('/speech/dialogueLog', dialogueLog)


    # unblock speech recognition after a second
    rospy.loginfo( "Wait for a second before unblocking speech recognition" )
    rospy.Timer(rospy.Duration(2), unblockSpeech, oneshot=True)


    # Return a True response, or an error if the speechsynth didn't exist
    if response:
        rospy.loginfo( "Speech synthesis exiting" )
        return TTSResponse("True")

    rospy.loginfo( "Error in speechsynthesis, synth does not exist?")
    return TTSResponse("Error, speechsynth \"" + speechsynth + "\" does not exist")


def TTSserver():
    rospy.init_node('TTS_request_server')
    s = rospy.Service('TextToSpeech', TTS, handleTTS)
    rospy.loginfo( "TTS Server ready to convert text to speech." )
    rospy.spin()


if __name__ == "__main__":
    TTSserver()
