#!/usr/bin/env python
import sys
import rospy
from rpi_robot.srv import *

def TTSclient(text, speechsynth):
    rospy.wait_for_service('TextToSpeech')
    try:
        TTSobj = rospy.ServiceProxy('TextToSpeech', TTS)
        resp1 = TTSobj(text, speechsynth)
        return resp1.result
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [text speechsynth]"%sys.argv[0]

if __name__ == "__main__":
    if len(sys.argv) == 3 and isinstance(sys.argv[1], basestring) and isinstance(sys.argv[2], basestring):
        text = sys.argv[1]
        speechsynth = sys.argv[2]
    else:
        print usage()
        sys.exit(1)
    print "Requesting TTS of '%s' with '%s' speechsynth" % (text, speechsynth)
    print "Response is: %s" % TTSclient(text, speechsynth)
