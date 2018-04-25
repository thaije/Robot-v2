import servoPWM as servoControl
import math
from time import sleep


servos = False
pie = 3.14159
sinsizeDef = 1700.0
totalSteps = sinsizeDef * 100.0

servoSpeeds = False
# actual ms value thrown at servo ranged, paused, speed shifted etc.
newPos = False

# Move the servo to the new position with a sinus motion
def moveServos(goalPos, steps, goalSpeeds, startDelay):
    """
    Function which moves one or multiple servos to new positions along a
    sinus motion
    @param goalPos (double list): Defines the goal positions for the servos
    @param steps (double): Number of steps into which to plan the movement
    @param goalSpeeds (int list): List with start, end speeds for each servo
    @param startDelay (int list): Delay in microseconds before start of movement
        for each servo
    """

    # init variables
    # 0 = servo has completed move. 1 = move to be completed
    motionComplete = [False] * len(servos)

    # Count ticker for primary loop to check if each servo needs to move
    count = [1] * len(servos)

    # Extended count for each servo to account for multiple cycles in one move function
    counts = [1] * len(servos)

    # How many microseconds to hold each new servo position
    speedTick = [1] * len(servos)

    #coefficient of sine math function
    b = [(2*pie/(sinsize*2))] * len(servos)

    # calc the amount of sinuses we traverse if we have to repeat the movement
    sinsizes = [sinsize] * len(servos)

    # current position of each servo
    newPos = [0.0] * len(servos)

    # a amplitude higher value taller wave shorter value shorter wave by magnitude:   a=(highest # - lowest #)/2
    a = [0.0] * len(servos)
    # b lower value = longer wave or higher value=shorter wave this is phase shift or stretch of function b=2pi/(period*2) where period is desired wave size
    b = [0.0] * len(servos)
    # c is x frequency offset = what part of curve want to look at
    c = [0.0] * len(servos)
    # d is y offset  = 0.5*amplitude shifts the curve so it is wholey in 1st quadrant
    d = [0.0] * len(servos)

    servoSpeeds = [0] * len(servos)
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


        # Speed values start off at startspeed and end up at endspeed as the
        # In case of fast-to-slow: result is a sine curve that is compressed in
        # the x axis on one end (fast), and stretched on other end (slow).
        startSpeed = goalSpeeds[i][0]
        endSpeed = goalSpeeds[i][1]

        if startSpeed > endSpeed:
            # start fast, end slow
            servoSpeeds[i] = ((counts[i] + 1.0) / sinsizeDef) * (startSpeed - endSpeed) + endSpeed
        else:# start slow, end fast
            servoSpeeds[i] = ((counts[i] + 1.0) / sinsizeDef) * (endSpeed - startSpeed) + startSpeed


    ######################################
    # Loop for setting the servo positions
    for step in range(steps):

        # if all servos are done with their motion, stop the loop
        if all(motionComplete):
            break

        for i, servo in enumerate(servos):

            ## condition 1
            # We have to wait for startDelay to end before starting the movement
            if count[i] < startDelay[i]:
                # sleep(?)
                pass

            ## condition 2
            # motion is done and position held
            elif count[i] > sinsize[i]:
                servo.setPosition(goalPos[i])
                motionComplete[i] = True

            ## condition 3
            # move servo with sinus function to goal position
            else:

                # new position of servo is written
                if count[i] < sinsize[i] and speedtick[i] == 1:
                    newPos[i] = a[i] * math.sin(count[i] * b[i] + c[i]) + d[i]
                    servo.setPosition(newPos[i])
                    # start of increment to count for possible pauses at this position to simulate slow
                    speedtick[i] += 1
                    # increments sine wave operator x in y=f(x)
                    count[i] += 1

                # sine wave is sustained at old value for 1 speedtick to servoSpeed
                elif speedtick[i] > 1 and speedtick[i] < servoSpeeds[i]:
                    servo.setPosition(newPos[i])
                    # increase speedtick to delay the servo at one position
                    # along its travel to simulate a certain speed
                    speedtick[i] += 1

                # sine wave is now permitted to continue drawing and moving to
                # points by having speedtick reset
                else:
                    count[i] += 1
                    speedtick[i] += 1

                    # alternately add and deduct 1 point
                    # 2->+1, 3->-1, 4->+1, 5->-1, etc
                    x = int(count[i] / sinsize)
                    multiplier = 1
                    if x != 1 and x % 2 != 0:
                        multiplier = -1
                    counts[i] += multiplier * 1


def main():
    # Set servo actively to position
    for servo in servos:
        servo.setPosition(servo.position)

    # repeat the motion 1 time for each servo
    goalPos = [1750, 2400] # set to max up, max right
    goalSpeeds = [[25, 5], [5, 25]] # list with start, end speeds for each servo
    startDelay = [100, 100] # delay (micros) for each servo before starting movement

    moveServos(goalPos, totalSteps, goalSpeeds, startDelay)
    print("Done")

def setup():
    global servos
    # [verticalServo, horizontalServo]
    servos = servoControl.initialize_default_servos()


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
