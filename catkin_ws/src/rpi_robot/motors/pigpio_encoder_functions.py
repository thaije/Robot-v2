# Uses decoder class to keep track of the movement
# of the wheels

import sys
import time
import pigpio
import RPi.GPIO as GPIO

import pigpio_encoder
import wheelMotors as dcMotorControl

# One rotation is 360 ticks
# Forwards is positive, backwards is negative

leftEncoderTicks = 0
rightEncoderTicks = 0
pi = None

# update left wheel encoder ticks
def callbackLeftWheel(way):
    global leftEncoderTicks

    leftEncoderTicks += way

    print("left={}".format(leftEncoderTicks))

# update right wheel encoder ticks
def callbackRightWheel(way):
    global rightEncoderTicks

    rightEncoderTicks += way

    print("right={}".format(rightEncoderTicks))


# stop the decoders
def cleanupEncoders():
    time.sleep(1)
    global decoderLeft
    global decoderRight

    decoderLeft.cancel()
    decoderRight.cancel()

    global pi
    pi.stop()


def checkEncoders(seconds):

    try:
        motors = dcMotorControl.initialize_default_motors()

        motors[0].forward(100)
        motors[1].forward(100)

        timed = 0
        while(timed < seconds):
            time.sleep(0.1)
            timed += 0.1


        print "stopping motors"
        dcMotorControl.stop_wheels(motors)
        dcMotorControl.cleanup(motors)

        # check if it continues turning during breaking
        timed = 0
        while(timed < 1):
            time.sleep(0.1)
            timed += 0.1
        # print encoder ticks
        print("Final encoder ticks left={}".format(leftEncoderTicks))
        print("Final encoder ticks right={}".format(rightEncoderTicks))
    except:
        print "error"
        #dcMotorControl.cleanup([motor1, motor2])


def encoderTest():
    # setup the encoders when the script is imported
    pi = pigpio.pi()

    decoderLeft = pigpio_encoder.decoder(pi, 14, 15, callbackLeftWheel)
    decoderRight = pigpio_encoder.decoder(pi, 17, 27, callbackRightWheel)

    print "Starting motors"
    checkEncoders(4)

    decoderLeft.cancel()
    decoderRight.cancel()
    pi.stop()
    GPIO.cleanup()

encoderTest()
