#!/usr/bin/env python
import rospy, rospkg
from std_msgs.msg import String

# import CMUpocketSphinx.cmuSTTlocal as cmuSTTlocal
from CMUpocketSphinx.scripts.recoMic.pocket_sphinx_listener_ros import PocketSphinxListener

# use default speechRecognizer defined in launch file
speechRecognizer = rospy.get_param("/speech/STTdef")


def speechPubl():
    # get path to current package
    rospack = rospkg.RosPack()
    path = rospack.get_path('rpi_robot') + "/speech/"

    # init speech recognizer to use
    if speechRecognizer == "cmu":
        rospy.loginfo("Using CMU speech recognizer")
        pocketSphinxListener = PocketSphinxListener(path=path, hmm="small", dic="small", lm="small")

    # init ROS node stuff
    pub = rospy.Publisher('recognizedSpeech', String, queue_size=10)
    rospy.init_node('recognizedSpeech', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # setup ROS variable for latest recognized text
    rospy.set_param('/speech/lastSpeechRecognized', "")

    while not rospy.is_shutdown():
        command = ""

        # Don't do speech recognition if it is blocked
        if rospy.get_param('/speech/blockSpeechRecognition'):
            rate.sleep()
            continue

        if speechRecognizer == "cmu":
            command = pocketSphinxListener.getCommand().lower()

        # Double check if speech recognition is not blocked
        if rospy.get_param('/speech/blockSpeechRecognition'):
            rate.sleep()
            continue

        # log reconized speech
        rospy.loginfo("Recognized: \"" + command + "\"")

        # Save text to paramter server, and publish recognized speech
        rospy.set_param('/speech/lastSpeechRecognized', command)
        pub.publish(command)

        # wait for next iteration
        rate.sleep()

if __name__ == '__main__':
    try:
        speechPubl()
    except rospy.ROSInterruptException:
        pass

# cmuSTTlocal.startPublSTT()
