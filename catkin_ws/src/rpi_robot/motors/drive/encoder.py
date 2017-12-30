# Class from Pigpio website to decode rotary encoder pulses
# Url: http://abyz.co.uk/rpi/pigpio/examples.html#Python code
# assumes two hal encoders per motor, each generating a tick on up and down of
# voltage, thus 4 ticks per rotation of motor = rotation of wheel * gear ratio

# run pigpio before running

import pigpio

class decoder:

    """Class to decode mechanical rotary encoder pulses."""

    def __init__(self, pi, gpioA, gpioB):

        """
        Instantiate the class with the pi and gpios connected to
        rotary encoder contacts A and B.  The common contact
        should be connected to ground.  The callback is
        called when the rotary encoder is turned.  It takes
        one parameter which is +1 for clockwise and -1 for
        counterclockwise.

        EXAMPLE

        import time
        import pigpio

        import rotary_encoder

        pos = 0

        def callback(way):

            global pos

            pos += way

            print("pos={}".format(pos))

        pi = pigpio.pi()

        decoder = rotary_encoder.decoder(pi, 7, 8, callback)

        time.sleep(300)

        decoder.cancel()

        pi.stop()

        """

        self.pi = pi
        self.gpioA = gpioA
        self.gpioB = gpioB

        self.ticks = 0

        self.levA = 0
        self.levB = 0

        self.lastGpio = None

        self.pi.set_mode(gpioA, pigpio.INPUT)
        self.pi.set_mode(gpioB, pigpio.INPUT)

        self.pi.set_pull_up_down(gpioA, pigpio.PUD_UP)
        self.pi.set_pull_up_down(gpioB, pigpio.PUD_UP)

        self.cbA = self.pi.callback(gpioA, pigpio.EITHER_EDGE, self._pulse)
        self.cbB = self.pi.callback(gpioB, pigpio.EITHER_EDGE, self._pulse)

    def _pulse(self, gpio, level, tick):

        """
        Decode the rotary encoder pulse.

                   +---------+         +---------+      0
                   |         |         |         |
         A         |         |         |         |
                   |         |         |         |
         +---------+         +---------+         +----- 1

             +---------+         +---------+            0
             |         |         |         |
         B   |         |         |         |
             |         |         |         |
         ----+         +---------+         +---------+  1
        """

        if gpio == self.gpioA:
            self.levA = level
        else:
            self.levB = level;

        if gpio != self.lastGpio: # debounce
            self.lastGpio = gpio

            if gpio == self.gpioA and level == 1:
                if self.levB == 1:
                    self.ticks += 1
            elif gpio == self.gpioB and level == 1:
                if self.levA == 1:
                    self.ticks -= 1

    def cancel(self):

        """
        Cancel the rotary encoder decoder.
        """

        self.cbA.cancel()
        self.cbB.cancel()



##################################################################
# General functions
##################################################################
def init_right_encoder(pi):
    decoderRight = decoder(pi, 17, 27)
    return decoderRight

def init_left_encoder(pi):
    decoderLeft = decoder(pi, 14, 15)
    return decoderLeft


# test with externally initialized servos and no cleanup
def test_encoders_external(pi, encoders):
    import wheelMotors as wheel_controller

    print "Testing encoders"

    # reset wheel encoder ticks
    global wheels_ticks_left
    global wheels_ticks_right
    wheels_ticks_left = 0
    wheels_ticks_right = 0

    # test / run motors
    motors = wheel_controller.initialize_default_motors()
    wheel_controller.test_wheels_external(motors)

    # print encoder ticks
    print "Left wheel encoder ticks:", wheels_ticks_left
    print "Right wheel encoder ticks:", wheels_ticks_right


# test without having to set anything up
def test_encoders_allin():
    pi = pigpio.pi()
    encoders = initialize_default_encoders(pi)

    test_encoders_external(pi, encoders)
    cleanup_wheel_encoders(encoders)
    pi.stop()

#test_encoders_allin()
