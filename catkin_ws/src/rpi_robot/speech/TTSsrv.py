#!/usr/bin/env python
import rospy
from rpi_robot.srv import *
import speechSynths


def handleTTS(req):
    speechsynth = req.speechsynth
    response = True

    # Speak the text with the requested speechsynth if it exists
    if speechsynth == "espeak":
        speechSynths.espeak(req.text)
    else:
        response = False

    # Return a True response, or an error if the speechsynth didn't exist
    if response:
        print "Returning 'True' for speaking: %s. With speech synth: %s" % (req.text, speechsynth)
        return TTSResponse("True")

    print "Returning 'Error, speechsynth does not exist' for speaking: %s. With speech synth: %s" % (req.text, speechsynth)
    return TTSResponse("Error, speechsynth " + speechsynth + " does not exist")


def TTSserver():
    rospy.init_node('TTS_request_server')
    s = rospy.Service('TextToSpeech', TTS, handleTTS)
    print "Ready to convert text to speech."
    rospy.spin()


if __name__ == "__main__":
    TTSserver()
