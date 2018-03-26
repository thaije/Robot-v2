#!/usr/bin/env python
import rospy
from rpi_robot.srv import *
import speechSynths
from time import sleep



def handleTTS(req):
    speechsynth = req.speechsynth
    response = True

    rospy.loginfo( "New speech command: \"" + req.text + "\"")
    rospy.loginfo( "Using speechsynth: " + speechsynth)

    # Announce that we are going to speak to the rest of the system, and block STT
    rospy.set_param('/speech/robotSpeaking', True)

    # Speak the text with the requested speechsynth if it exists
    if speechsynth == "espeak":
        speechSynths.espeak(req.text)
    elif speechsynth == "festival":
        speechSynths.festival(req.text)
    elif speechsynth == "flite":
        speechSynths.flite(req.text)
    else:
        response = False
    rospy.loginfo( "Done speaking" )

    # we are done speaking, reset system variable
    rospy.set_param('/speech/robotSpeaking', False)

    # update latest spoken speech to dialogue log
    dialogueLog = rospy.get_param("/speech/dialogueLog", [])
    dialogueLog.append(["self", rospy.get_time(), req.text])
    rospy.set_param('/speech/dialogueLog', dialogueLog)

    # Return a True response, or an error if the speechsynth didn't exist
    if response:
        rospy.loginfo( "Speech synthesis exiting \n" )
        return TTSResponse("True")

    rospy.loginfo( "Error in speechsynthesis, synth does not exist? ")
    return TTSResponse("Error, speechsynth \"" + speechsynth + "\" does not exist")


def TTSserver():
    rospy.init_node('TTS_request_server')
    s = rospy.Service('TextToSpeech', TTS, handleTTS)
    rospy.loginfo( "TTS Server ready to convert text to speech." )
    rospy.spin()


if __name__ == "__main__":
    TTSserver()
