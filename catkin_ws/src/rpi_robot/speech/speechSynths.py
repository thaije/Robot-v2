#!/usr/bin/env python
import rospy, rospkg
import subprocess


def espeak(text):
    subprocess.call('espeak '+text, shell=True)


def festival(text):
    subprocess.call('echo '+text + '|festival --tts', shell=True)


def flite(text):
    rospack = rospkg.RosPack()
    path = "file://" + rospack.get_path('rpi_robot') + "/speech/cmu_us_bdl.flitevox"
    print "Path for Flite is: ", path
    subprocess.call('flite -voice '+ path + ' \"' + text + '\"', shell=True) # shell=True is important!
