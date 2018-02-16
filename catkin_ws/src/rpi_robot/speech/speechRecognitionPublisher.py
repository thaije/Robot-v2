#!/usr/bin/env python
import rospy, rospkg
from std_msgs.msg import String
from CMUpocketSphinx.scripts.recoMic.pocket_sphinx_listener_ros import PocketSphinxListener

# use default speechRecognizer defined in launch file
speechRecognizer = rospy.get_param("/speech/STTdef")




def main():
    # get path to current package
    rospack = rospkg.RosPack()
    path = rospack.get_path('rpi_robot') + "/speech/"

    # init ROS node stuff
    pub = rospy.Publisher('recognizedSpeech', String, queue_size=10)
    rospy.init_node('recognizedSpeech', anonymous=True)
    rate = rospy.Rate(2) # 10hz
    model = False
    rospy.set_param('/speech/lastSpeechRecognized', "")
    
    rospy.loginfo( "Initialized Speech Recognition" )

    # init speech recognizer to use
    if speechRecognizer == "cmu":
        rospy.loginfo("Using CMU speech recognizer")
        model = PocketSphinxListener(path=path, hmm="small", dic="small", lm="small")

    while not rospy.is_shutdown():
        command = ""

        # skip if speechRecognition was canceled
        if rospy.get_param('/speech/speechRecognitionMode') != 1:
            rate.sleep()
            continue

        # get the recognized speech
        if speechRecognizer == "cmu":
            command = model.getCommand().lower()

        # log reconized speech
        rospy.loginfo("Recognized: \"" + command + "\"")

        # Save text to paramter server, and publish recognized speech
        rospy.set_param('/speech/lastSpeechRecognized', command)
        pub.publish(command)

        # wait for next iteration
        rate.sleep()




if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
