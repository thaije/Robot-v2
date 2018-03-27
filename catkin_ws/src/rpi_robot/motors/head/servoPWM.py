import pigpio
import time

pi = pigpio.pi()

# Servo class with all information and methods for the wiringpi objects
class Servo:

    def __init__(self, pin, minPos, maxPos, centerPosition):
        """ Initialize the motor with its pins, min, max and
        center positions"""

        self.pin = pin
        self.minPos = minPos
        self.maxPos = maxPos
        self.centerPosition = centerPosition
        self.setPosition(self.centerPosition)
        # sleep 0.15s for every 100 ticks movement
        self.secs_per_100 = 0.15

    # set the position of the servo
    def setPosition(self, position):
        new_pos = clamp(position, self.minPos, self.maxPos)

        # calc change
        delta = abs(new_pos - self.position)

        self.position = new_pos
        pi.set_servo_pulsewidth(self.pin, self.position)

        # give the servo some time to move to the target pos
        wait_time = (self.secs_per_100 / 100) * delta
        print wait_time
        time.sleep(wait_time)
        pi.set_servo_pulsewidth(self.pin, 0)

    def center(self):
        self.setPosition(self.centerPosition)

    def stop(self):
        pi.set_servo_pulsewidth(self.pin, 0)

    def getPosition(self):
        return self.position



#############################################################
# General functions
#############################################################
# limit a value to a min and max
def clamp(n, minN, maxN):
    return max(min(maxN, n), minN)


def initialize_default_servos():
    print "Initializing default servos"
    verticalServo = Servo(pin=13, minPos=600, maxPos=1750, centerPosition=800) # 600=down 1750=up
    horizontalServo = Servo(pin=18, minPos=600, maxPos=2400, centerPosition=1500) # 600=left 2400=right

    return [verticalServo, horizontalServo]


def cleanup_servos(servos):
    print "Cleaning up servos"
    for servo in servos:
        servo.center()

        # wait for the servo to center
        time.sleep(1)

        for servo in servos:
            servo.stop()


# test with externally initialized servos and no cleanup
def test_servos_external(servos):
    print "Testing Servos"
    dtMin, dtMax = 600, 2400
    dt = dtMin
    while True:
        try:
            print dt
            servos[0].setPosition(dt)
            servos[1].setPosition(dt)
            dt += 100
            if dt > dtMax:
                dt = dtMin
            time.sleep(1)
        except:
            servos[0].stop()
            servos[1].stop()
            print "Exiting."
            break


# test without having to set anything up
def test_servos_allin():
    servos = initialize_default_servos()
    test_servos_external(servos)
    cleanup_servos(servos)

#test_servos_allin()
