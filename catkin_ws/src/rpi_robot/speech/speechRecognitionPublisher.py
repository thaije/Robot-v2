#!/usr/bin/env python
import rospy, rospkg
from std_msgs.msg import String

# import CMUpocketSphinx.cmuSTTlocal as cmuSTTlocal
from CMUpocketSphinx.scripts.recoMic.pocket_sphinx_listener_ros import PocketSphinxListener

speechRecognizer = "cmu"


def speechPubl():
    # get path to current package
    rospack = rospkg.RosPack()
    path = rospack.get_path('rpi_robot') + "/speech/"

    if speechRecognizer == "cmu":
        print "Using CMU speech recognizer"
        pocketSphinxListener = PocketSphinxListener(path=path, hmm="small", dic="small", lm="small")

    pub = rospy.Publisher('recognizedSpeech', String, queue_size=10)
    rospy.init_node('recognizedSpeech', anonymous=True)
    rate = rospy.Rate(10) # 10hz


    while not rospy.is_shutdown():
        command = ""

        if speechRecognizer == "cmu":
            command = pocketSphinxListener.getCommand().lower()

        print "Recognized: %s" % command

        # TODO: save command to paramter server

        rospy.loginfo(command + str(rospy.get_time()) )
        pub.publish(command)
        rate.sleep()

if __name__ == '__main__':
    try:
        speechPubl()
    except rospy.ROSInterruptException:
        pass

# cmuSTTlocal.startPublSTT()
