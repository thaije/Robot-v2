#!/usr/bin/env python
from rpi_robot.srv import ToggleSpeechRec
import rospy

# do steps at http://wiki.ros.org/ROS/Tutorials/CreatingMsgAndSrv

pocketsphinxActivated = False

def handle_sphinx_toggle(req):
    print "Toggle:", req.toggle

    # toggle on
    if not pocketsphinxActivated:
        pocketsphinxActivated = True;
        return ToggleSpeechRecResponse("Toggled on");

    # otherwise toggle off
    pocketsphinxActivated = False
    return ToggleSpeechRecResponse("Toggled off")


def toggle_pocketsphinx():
    rospy.init_node('toggle_pocketsphinx_server')
    s = rospy.Service('toggle_pocketsphinx', ToggleSpeechRec, handle_sphinx_toggle)
    print "Ready to toggle Pocketsphinx Speech recognition on/off."
    rospy.spin()

if __name__ == "__main__":
    toggle_pocketsphinx()
