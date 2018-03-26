#!/usr/bin/env python
from pocketsphinx import *
import pyaudio
import gevent
import rospy


# Options:
# hmm = "small" . Default is CMU default.
# dic = "small" . Default is "small"
# LM = "small" . Default is "small"

class PocketSphinxListener(object):
    def __init__(self, path, hmm=False, dic=False, lm=False):

        rospy.loginfo( "Initializing CMU Sphinx speech recognizer" )

        # defaults
        model_path = get_model_path()
        self.hmm = os.path.join(model_path, 'en-us')
        self.dic = path + 'CMUpocketSphinx/dicts/limited_dict.dic'
        self.lm = path + 'CMUpocketSphinx/lang_models/limited_lang_model.lm'

        if hmm == "small":
            rospy.loginfo( "Using small acoustic model")
            self.hmm = path + 'CMUpocketSphinx/acoustic_models/cmusphinx-en-us-ptm-5.2'
        elif hmm == "cmu":
            rospy.loginfo( "Using CMU acoustic model")
            self.hmm = os.path.join(model_path, 'en-us')

        if dic == "small":
            rospy.loginfo( "Using small dictionary")
            self.dic = path + 'CMUpocketSphinx/dicts/limited_dict.dic'
        else:
            rospy.loginfo( "Using small dictionary")

        if lm == "small":
            rospy.loginfo( "Using small language model")
            self.lm = path + 'CMUpocketSphinx/lang_models/limited_lang_model.lm'
        else:
            rospy.loginfo( "Using small language model")



        self.bitesize = 512

        self.debug = False

        self.config = Decoder.default_config()
        self.config.set_string('-hmm', self.hmm)
        # The language model is a statistical model that you can use to determine what words the user is trying to say.
        # This can be used in place of a predetermined grammar file.
        self.config.set_string('-lm', self.lm)
        self.config.set_string('-dict', self.dic)

        # Comment out the following line to get debugging output from the decoder. This is useful if the program is failing
        # with an error such as "argument 1 of type 'Decoder *'"
        if not self.debug:
            self.config.set_string('-logfn', '/dev/null')

    	# Alan force log
    	self.config.set_string('-verbose', 'no')
     # 	self.config.set_string('-logfn', 'psphinx.log')

        self.config.set_boolean("-allphone_ci", True)

        self.decoder = Decoder(self.config)

        self.pyAudio = pyaudio.PyAudio()

    # check if the mode of Speech Recognition was changed (e.g. disabled),
    # and stop processing if so
    def checkIfCanceled(self):
        if rospy.get_param('/speech/speechRecognitionMode') != 1:
            rospy.loginfo( "Speech Recognition mode has been changed, returning")

            # stop audio stream
            try:
                self.decoder.end_utt()
                self.stream.stop_stream()
                self.stream.close()
            except:
                pass
            return True
        return False

    def getCommand(self, debug=False):
        # Check if we are in debugging mode, either for the getCommand method or for the entire class
        if self.debug or debug:
            debug = True

        # We're going to set up the stream from pyAudio that well be using to get the user's speech from the microphone.
        self.stream = self.pyAudio.open(format=pyaudio.paInt16,
                                       channels=1,
                                       rate=16000,
                                       input=True,
                                       frames_per_buffer=self.bitesize)

        # Let the use know that we're ready for them to speak
        rospy.loginfo( "STT waiting for more input: ")
        # print "Need more input"

        # This is a flag that we'll use in a bit to determine whether we are going from silence to speech
        # or from speech to silence.
        utteranceStarted = False

        # This will tell PocketSphinx to start decoding the "utterance". When we are finished with our audio
        # we will tell PocketSphinx that the utterance is over.
        self.decoder.start_utt()

        # We want this to loop for as long as it takes to get the full sentence from the user. We only exit with a
        # return statement when we have our best guess of what the person said.
        while True:
            if self.checkIfCanceled():
                return ""

            try:
                # This takes a small sound bite from the microphone to process.
                soundBite = self.stream.read(self.bitesize)
            except Exception as e:
                pass

            # If we've got something from the microphone, we should begin processing it.
            if soundBite:
                if self.checkIfCanceled():
                    return ""

                self.decoder.process_raw(soundBite, False, False)
                inSpeech = self.decoder.get_in_speech()
                # The following checks for the transition from silence to speech.
                # We're going to set a flag to reflect this.
                if inSpeech and not utteranceStarted:
                    utteranceStarted = True
                # The following checks for the transition from speech to silence.
                # This is our cue to check what was said and do something useful with it.
                if not inSpeech and utteranceStarted:
                    # We tell PocketSphinx that the user is finished saying what they wanted
                    # to say, and that it should makes it's best guess as to what thay was.
                    self.decoder.end_utt()

                    if self.checkIfCanceled():
                        return ""

                    # The following will get a hypothesis object with, amongst other things,
                    # the string of words that PocketSphinx thinks the user said.
                    self.hypothesis = self.decoder.hyp()
                    if self.hypothesis is not None:
                        bestGuess = self.hypothesis.hypstr

                        if self.checkIfCanceled():
                            return ""

                        # We are done with the microphone for now so we'll close the stream.
                        self.stream.stop_stream()
                        self.stream.close()
                        # We have what we came for! A string representing what the user said.
                        # We'll now return it to the runMain function so that it can be
                        # processed and some meaning can be gleamed from it.
                        return bestGuess
                # The following is here for debugging to see what the decoder thinks we're saying as we go
                if debug and self.decoder.hyp() is not None:
                    print self.decoder.hyp().hypstr
