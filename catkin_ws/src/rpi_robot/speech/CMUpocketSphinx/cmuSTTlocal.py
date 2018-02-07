import sys, traceback, time, subprocess

# This import will give us our wrapper for the Pocketsphinx library which we can use to get the voice commands from the
# user.
from scripts.recoMic.pocket_sphinx_listener_ros import PocketSphinxListener


def startPublSTT():

    # Now we set up the voice recognition using Pocketsphinx from CMU Sphinx.
    pocketSphinxListener = PocketSphinxListener(hmm="small", dic="small", lm="small")


    while True:
        try:
            command = pocketSphinxListener.getCommand().lower()

            # TODO: do something with the command
            print "Recognized: %s" % command
            # print command
            # print type(command)

            # TODO: Test without this shit
            # This will allow us to be good cooperators and sleep for a second.
            # print "I'm thinking now"
            time.sleep(1)

        except (KeyboardInterrupt, SystemExit):
            print 'Speech recognition exited. Goodbye.'
            sys.exit()
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception(exc_type, exc_value, exc_traceback,
                                      limit=2,
                                      file=sys.stdout)
            sys.exit()

startPublSTT()
