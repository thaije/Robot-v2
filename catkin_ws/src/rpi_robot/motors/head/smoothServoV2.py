import servoPWM as servoControl
import math
from time import sleep

# Script which controls movement of 1 or multiple servos as such to move
# to a certain position, with a start and end speed, using a sin function

servos = False
pie = 3.14159
sinsize = 1700.0
totalSteps = sinsize * 100.0

# how long to wait at each position before continuing to the next
# long wait -> slow movement. short wait -> fast movement
waitPerPos = False
# actual new Servo position command
newPos = False

# Move the servo to the new position with a sinus motion
def moveServos(goalPos, steps, goalSpeeds, startDelay):
    """
    Function which moves one or multiple servos to new positions using a
    sinus motion.
    To be specfic, the servo traverses from its current position to position @goalPos
    in @sinsize steps (@count keeps track of steps).
    It starts with speed @goalSpeeds[servo][0], and goes to speed @goalSpeeds[servo][1],
    where speed is simulated by holding every position for @waitPerPos ticks
    (@timeOnPos keeps track of time on position). After both servos complete
    their movement (@motionComplete), the function returns.

    @param goalPos (double list): Defines the goal positions for the servos
    @param steps (double): Number of steps into which to plan the movement
    @param goalSpeeds (int list): List with start, end speeds for each servo
    @param startDelay (int list): Delay in microseconds before start of movement
        for each servo
    """

    # init variables
    # 0 = servo has completed move. 1 = move to be completed
    motionComplete = [False] * len(servos)

    # Primary loop counter which goes from 0 to @sinsize
    count = [1] * len(servos)

    # Extended count for each servo to account for multiple cycles in one move function
    counts = [1] * len(servos) # NOTE: extra?

    # How many microseconds the servo is on one position
    timeOnPos = [1] * len(servos)

    # calc the amount of sinuses we traverse if we have to repeat the movement
    # sinsizes = [sinsize] * len(servos)

    # new Position for each servo
    newPos = [0.0] * len(servos)

    # a amplitude higher value taller wave shorter value shorter wave by magnitude:   a=(highest # - lowest #)/2
    a = [0.0] * len(servos)
    # b lower value = longer wave or higher value=shorter wave this is phase shift or stretch of function b=2pi/(period*2) where period is desired wave size
    b = [(2*pie/(sinsize*2))] * len(servos)
    # c is x frequency offset = what part of curve want to look at
    c = [0.0] * len(servos)
    # d is y offset  = 0.5*amplitude shifts the curve so it is wholey in 1st quadrant
    d = [0.0] * len(servos)


    waitPerPos = [0] * len(servos)
    for i, servo in enumerate(servos):

        # calc position dependent sine wave coefficients
        if goalPos[i] > servo.position:
            a[i] = (goalPos[i] - servo.position) / 2.0
            c[i] = 1.5 * pie
            d[i] = servo.position + a[i]
        else:
            a[i] = (servo.position - goalPos[i]) / 2.0
            c[i] = 0.5 * pie
            d[i] = servo.position - a[i]


    ######################################
    # Loop for setting the servo positions
    for step in range(int(steps)):

        # if all servos are done with their motion, stop the loop
        if all(motionComplete):
            print "Motion complete:", motionComplete
            break

        for i, servo in enumerate(servos):

            # Speed values start off at startspeed and end up at endspeed as the
            # In case of fast-to-slow: result is a sine curve that is compressed in
            # the x axis on one end (fast), and stretched on other end (slow).
            # Called every loop to smoothly change from startspeed to endspeed during movement.
            # NOTE: change to count?
            # startSpeed = goalSpeeds[i][0], endSpeed = goalSpeeds[i][1]
            if goalSpeeds[i][0] > goalSpeeds[i][1]:
                # start fast, end slow
                waitPerPos[i] = ((counts[i] + 1.0) / sinsize) * (goalSpeeds[i][0] - goalSpeeds[i][1]) + goalSpeeds[i][1]
            else:# start slow, end fast
                waitPerPos[i] = ((counts[i] + 1.0) / sinsize) * (goalSpeeds[i][1] - goalSpeeds[i][0]) + goalSpeeds[i][0]



            ## condition 1
            # We have to wait for startDelay to end before starting the movement
            if step < startDelay[i]:
                # NOTE: do sleep here?
                pass

            ## condition 2
            # motion is done and position held
            elif step > sinsize:
                print "Motion should be done, as step (%d) > sinsize (%d)" % (step, sinsize)
                servo.setPosition(goalPos[i])
                motionComplete[i] = True

            ## condition 3
            # move servo with sinus function to goal position
            else:
                # Send new position to servo
                if count[i] < sinsize and timeOnPos[i] == 1:
                    newPos[i] = int(a[i] * sin(count[i] * b[i] + c[i]) + d[i])
                    servo.setPosition(newPos[i])
                    # start of increment to count for possible pauses at this position to simulate slow
                    timeOnPos[i] += 1
                    # increments sine wave operator x in y=f(x)
                    count[i] += 1

                # keep the servo at a position for x ticks such as defined in waitPerPos
                elif timeOnPos[i] > 1 and timeOnPos[i] < waitPerPos[i]:
                    # servo.setPosition(newPos[i]) # NOTE: extra?
                    timeOnPos[i] += 1

                # If waited long enough on position, reset timeOnPos to enable
                # going to the next pos
                else:
                    count[i] += 1
                    timeOnPos[i] = 1

                    # alternately add and deduct 1 point
                    # 2->+1, 3->-1, 4->+1, 5->-1, etc
                    x = int(count[i] / sinsize)
                    multiplier = 1
                    if x != 1 and x % 2 != 0:
                        multiplier = -1
                    counts[i] += multiplier * 1 # NOTE: change to count?



# convert delay (ms) to python sleep (s) command
def delay(number):
    sleep(number / 1000.0)


def sin(val):
    return math.sin(val)



def main():
    # Set servo actively to position
    for servo in servos:
        servo.setPosition(servo.position)

    # set to max up, max right
    goalPos = [1750, 2400]
    # list with start, end speeds for each servo, 1=fast, 25=slow
    goalSpeeds = [[1, 1], [1, 1]]
    # delay in ms for each servo before starting movement
    startDelay = [100, 100]

    moveServos(goalPos, totalSteps, goalSpeeds, startDelay)
    print("Done")


# test class instead of using servo class connected to rpi GPIO servos
#class Servo:
#    def __init__(self, name, minPos, maxPos):
#        self.position = minPos
#        self.name = name
#        self.minPos = minPos
#        self.maxPos = maxPos

#    def setPosition(self, pos):
#        print("Set %s servo to position %d" % (self.name, pos) )


def setup():
    global servos
    # [verticalServo, horizontalServo]
    servos = servoControl.initialize_default_servos()

    # test
    # servos = [Servo("vertical", 600, 1750), Servo("horizontal", 600, 2400)]


def cleanup():
    servoControl.cleanup_servos(servos)


if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        print "interrupted by user"
    finally:
    	print "cleaning up"
    	cleanup()
