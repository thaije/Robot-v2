from time import sleep
import sys
import servos
import picamera
import rpiVision

verticalServo = horizontalServo = False

def loop():

    print "Start picamera"

    camera = picamera.PiCamera()
    # the camera has been mounted upside down so flip it
    camera.vflip = True
    camera.brightness = 60 # tested during night

    # take a picture:
    # camera.capture('image.jpg')

    # capture video
    # camera.start_recording('video.h264')
    # sleep(5)
    # camera.stop_recording()

    # Stream video
    # connect from outside with ssh to camera

    # See an preview (stop with Ctrl+D)
    camera.start_preview()
    sleep(5)
    camera.stop_preview()


def init():
    global verticalServo
    global horizontalServo
    [verticalServo, horizontalServo] = servos.initialize_default_servos()



def main():

    try:
        init()
        loop()

    except KeyboardInterrupt:
        print "User cancelled"

    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

    finally:
        print "Cleaning up.."
        servos.cleanup_servos([verticalServo, horizontalServo])


if __name__ == "__main__":
    main()
