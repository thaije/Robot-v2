# This script uses software pwd on a sne73 chip to
# drive two dc motors
# Speed of the DC motors is based on average voltage
# Low duty cycle is short pulses with short pauses inbetween (low aver. voltage)
# High duty cycle is long pulses with long pauses inbetween (high aver. voltage)
# Max duty cycle is 100
# motor1 is left wheel
# motor2 is right wheel


import RPi.GPIO as GPIO
from time import sleep
#from handy_stuff.functions.functions import *


GPIO.setmode(GPIO.BCM)


class Motor:

    def __init__(self, pinForward, pinBackward, pinControl):
        """ Initialize the motor with its control pins and start pulse-width
             modulation """

        self.pinForward = pinForward
        self.pinBackward = pinBackward
        self.pinControl = pinControl
        GPIO.setup(self.pinForward, GPIO.OUT)
        GPIO.setup(self.pinBackward, GPIO.OUT)
        GPIO.setup(self.pinControl, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.pinForward, 100)
        self.pwm_backward = GPIO.PWM(self.pinBackward, 100)
        self.pwm_forward.start(0)
        self.pwm_backward.start(0)
        GPIO.output(self.pinControl, GPIO.HIGH)

    def forward(self, speed):
        """ pinForward is the forward Pin, so we change its duty
             cycle according to speed. """
        self.pwm_backward.ChangeDutyCycle(0)
        self.pwm_forward.ChangeDutyCycle(speed)

    def backward(self, speed):
        """ pinBackward is the forward Pin, so wwiringpi.pwmWrite(18,0)
        wiringpi.pwmWrite(13,0)e change its duty cycle according to speed. """
        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(speed)

    def stop(self):
        """ Set the duty cycle of both control pins to zero to
        stop the motor. """

        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)



#########################################################
# General functions
#########################################################

def set_wheel_drive_rates( wheels, speeds):
    if len(wheels) != len(speeds):
        raise ValueError('Number of wheels and speeds is not equal')

    for index, speed in enumerate(speeds):
        set_wheel_speed(wheel[index], speed)


def set_wheel_speed(wheel, speed):
    if speed == 0:
        wheel.stop()
    elif speed > 0:
        speed = clamp(speed, 0, 100)
        wheel.forward(speed)
    elif speed < 0:
        speed = clamp(speed, -100, 0)
        wheel.backward(speed)


# stop turning of wheels
def stop_wheels(wheels):
    for wheel in wheels:
        wheel.stop()


# Limit a value to a min and max
def clamp(n, minN, maxN):
    return max(min(maxN, n), minN)


def cleanup_motors(motors):
    print "Cleaning up motors"
    stop_wheels(motors)
    GPIO.cleanup()


def initialize_default_motors():
    print "Initializing motors with default settings"
    left_motor = Motor(23, 25, 24)
    right_motor = Motor(11, 10, 9)

    return [left_motor, right_motor]


# test with externally initialized motors and no cleanup
def test_wheels_external(motors):
    # try:
    print "testing first motor"
    motors[0].forward(100)
    sleep(2)
    motors[0].backward(100)
    sleep(1)
    motors[0].stop()

    print "testing second motor"
    motors[1].forward(100)
    sleep(2)
    motors[1].backward(100)
    sleep(1)
    motors[1].stop()
    # except:
    #     print "Error during testing of motors."
    # finally:
    stop_wheels(motors)


# test without having to set anything up
def test_wheels_allin():
    motors = initialize_default_motors()
    test_wheels_external(motors)
    cleanup_motors(motors)

#test_wheels_allin()
