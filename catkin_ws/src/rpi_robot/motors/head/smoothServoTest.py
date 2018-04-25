import servoPWM as servoControl
import math
from time import sleep

servo1 = False
servo2 = False
pie = 3.14159
sinsize = 1700.0
event = sinsize * 100.0

# servo 1 800-2200 decrease to open
svo1c   = 1750    # servo closed position
svo1o   = 600     # servo open position

# servo 2 800-2200 increase to open
svo2c   = 600     # servo closed position
svo2o   = 2400    # servo open position



count1 = 0.0      # sine wave x variable counts from 1 to 1700 (servo resolution) only starts counting after wait# reaches its activation value.
count1s = 0.0
speed1 = 0.0      # a value that consists of small increment values that change in magnitude depending on if the wave starts slow and ends fast or vise versa.
speedtick1 = 0.0  # ticks off how long the hold position for the servo is in very small ms increments giving the illusion of a slower or faster moving servo
sinsize1 = 0.0
                  # y= a*sin(bx+c)+d
                  # yvar# = a#(sin (b#*count#+c#)+d#
yvar1 = 0.0       # actual ms value thrown at servo ranged, paused, speed shifted etc.
a1 = 0.0          # a amplitude higher value taller wave shorter value shorter wave by magnitude:   a=(highest # - lowest #)/2
b1 = 0.0          # b lower value = longer wave or higher value=shorter wave this is phase shift or stretch of function b=2pi/(period*2) where period is desired wave size
c1 = 0.0          # c is x frequency offset = what part of curve want to look at
d1 = 0.0          # d is y offset  = 0.5*amplitude shifts the curve so it is wholey in 1st quadrant
per1 = 0          # trigger value either 0 or 1 to declare that that servo has reached its final position and so servo movement sequence of all servos (once all report per#=1)can end.

count2 = 0.0
count2s = 0.0
sinsize2 = 0.0
speed2 = 0.0
speedtick2 = 0.0
yvar2 = 0.0
a2 = 0.0
b2 = 0.0
c2 = 0.0
d2 = 0.0
per2 = 0


# convert delay (ms) to python sleep (s) command
def delay(number):
    sleep(number / 1000.0)


# start of primary move function that includes all servos and is called up and activated per each event
def movef(ecycle, s1, w81, spa1, spb1, yprev1, ynext1, s2,  w82, spa2, spb2, yprev2, ynext2):
    # counter master list:
    # count = count ticker for primary loop to check to see if each servo needs to move
    # count# = count for each servo that starts up once wait period for that servo is reached
    # count#s =extended count for each servo to account for multiple cycles in one move function
    # speedtick# =a tiny microsecond pause from 1 to a value between spa# to spb# where servo is held momentary at one value
    # per# = either 1 or 0 marks end of all movement from that servo for the movef function.

    delay(1)   # master delay
    # resets and values established
    per1=0
    per2=0
    count1 = 1
    count1s =1
    speedtick1 = 1
    b1=(2*pie/(sinsize*2))  # coefficient of sine math function

    sinsize1=((s1*2)-1)*sinsize  # ranges from s1=1,2,3,4,5 sinsize#= 1*1700,3*1700,5*1700,7*1700

    count2 = 1
    count2s =1
    speedtick2 = 1
    b2=(2*pie/(sinsize*2))
    sinsize2=((s2*2)-1)*sinsize

    # position dependent sine wave coeficients
    if(ynext1 > yprev1):
        a1= (ynext1-yprev1)/2.0
        c1= (1.5)*pie
        d1= yprev1+a1
    else:  # (ynext# < yprev#)
        a1= (yprev1-ynext1)/2.0
        c1= (0.5)*pie
        d1= yprev1-a1

    if(ynext2 > yprev2):
        a2= (ynext2-yprev2)/2.0
        c2= (1.5)*pie
        d2= yprev2+a2
    else:  # (ynext# < yprev#)
        a2= (yprev2-ynext2)/2.0
        c2= (0.5)*pie
        d2= yprev2-a2




    # ##########   GLOBAL LOOP FOR ALL SERVOS #######################
    for count in range(0, ecycle):
        # traditional speed values start off as spa# and end up as spb# as count# ticks away on the fly as curve is being drawn.
        #  result is a sine curve that is compressed in the x axis on one end (spa#=large number) and stretched on other end (spb#=small number).

        if spa1 > spb1:
            speed1=((count1s+1.0)/sinsize)*(spa1-spb1) + spb1 # start fast end slow
        else:
            speed1= ((count1s+1.0)/sinsize)*(spb1-spa1)+ spa1 #  start slow end fast

        if spa2 > spb2:
            speed2=((count2s+1.0)/sinsize)*(spa2-spb2) + spb2 # start fast end slow
        else:
            speed2= ((count2s+1.0)/sinsize)*(spb2-spa2)+ spa2 #  start slow end fast



        #  servo #1   3 states or cases

         # condition 1 servo not ready to move yet, sleep for start duration (w81)
        if count < w81:
            servo1.setPosition(yprev1)

        # condition 3 motion is done and position is held
        elif count > w81 and count1 > sinsize1:
            servo1.setPosition(ynext1)
            per1=1 # declares this servo is finished with its movement

        # condition 2 sin wave function active with optional hold position while big loop asks other servos for their turn
        elif count > w81:

            # new position of servo is written
            if count1 < sinsize1 and speedtick1 == 1:
                yvar1= a1*sin((count1)*b1+c1)+d1  # the math function
                servo1.setPosition(yvar1)   # throws a command at the servo
                speedtick1 += 1 #  start of increment to count for possible pauses at this position to simulate slow
                count1 += 1 # increments sine wave operator x in y=f(x)

            # sine wave is sustained at old value for 1 to speed# as counted by speedtick#
            elif speedtick1 > 1 and speedtick1 < speed1:
                servo1.setPosition(yvar1)
                speedtick1 += 1  # increments speedtick1 to delay the servo at one position along its travel to simulate a speed

            # sine wave is now permitted to continue drawing and moving to points by having speedtick# reset
            else:
                count1+=1 # locks out the sine function from going past sinsize by ever increasing count#
                speedtick1 = 1 # reset for next sin wave increment  through of sine fun

                if count1/sinsize <= 1:    # count#s is given a positive or negative counter to follow sin wave so speed can be adjusted
                    count1s +=1
                elif count1/sinsize > 1 and count1/sinsize < 2:
                    count1s -=1
                elif count1/sinsize >= 2 and count1/sinsize < 3:
                    count1s +=1
                elif count1/sinsize >= 3 and count1/sinsize < 4:
                    count1s -=1
                elif count1/sinsize >= 4 and count1/sinsize < 5:
                    count1s +=1
                elif count1/sinsize >= 5 and count1/sinsize < 6:
                    count1s -=1
                elif count1/sinsize >= 6 and count1/sinsize < 7:
                    count1s +=1

        # end if statement for case 2



        # servo #2
        if count < w82:     # notes same as servo #1 above
            servo2.setPosition(yprev2)

        elif count > w82 and count2 > sinsize2:
            servo2.setPosition(ynext2)
            per2=1

        elif count > w82:

            if count2 < sinsize2 and speedtick2 == 1:
                yvar2= a2*sin((count2)*b2+c2)+d2
                servo2.setPosition(yvar2)
                speedtick2 += 1
                count2 += 1

            elif speedtick2 > 1 and speedtick2 < speed2:
                servo2.setPosition(yvar2)
                speedtick2 += 1

            else:
                count2+=1
                speedtick2 = 1

                if count2/sinsize <= 1:
                    count2s +=1
                elif count2/sinsize > 1 and count2/sinsize < 2:
                    count2s -=1
                elif count2/sinsize >= 2 and count2/sinsize < 3:
                    count2s +=1
                elif count2/sinsize >= 3 and count2/sinsize < 4:
                    count2s -=1
                elif count2/sinsize >= 4 and count2/sinsize < 5:
                    count2s +=1
                elif count2/sinsize >= 5 and count2/sinsize < 6:
                    count2s -=1
                elif count2/sinsize >= 6 and count2/sinsize < 7:
                    count2s +=1

            # breaks FOR loop out of further un necessary cycles as all servos report their movement complete
            if per1 == 1 and per2 == 1:
                break

    # ############# END OF GLOBAL LOOP FOR ALL SERVOS ############
# end of void subroutine function for entire move function


#  start of program meat
def setup():
    global servo1, servo2
    [servo1, servo2] = servoControl.initialize_default_servos()


def loop():
    # servo lockdown when power is on
    servo1.setPosition(svo1c)
    servo2.setPosition(svo2c)


    # key:
    #  ecycle = time acts as the cut off when all servos have completed their one way motion
    #  s# = number of times sine wave repeats
    #  w8#= 1000=1sec approx. each servo wait time
    #  spa# = start speed, range: 1-25 or 1 fast, 25 slow
    #  spb# = end speed, range: 1-25 or 1 fast, 25 slow
    #  yprev# = previous servo position
    #  ynext# = next position

    # key:ecycle, s1,w81, spa1,spb1,yprev1,ynext1,s2,w82,spa2, spb2,yprev2,ynext2)
    movef(event , 3, 100, 10  ,25  ,svo1c ,svo1o ,3 ,5000,15  ,5   ,svo2c ,svo2o)
    print "Done with first loop"
    delay(2000)
    movef(event , 1, 5000,25  ,5   ,svo1o ,svo1c ,1 ,1100,1   ,15  ,svo2o ,svo2c)
    delay(4000)





# def setup():
#     global servo1, servo2
#     [servo1, servo2] = servoControl.initialize_default_servos()

def cleanup():
    servoControl.cleanup_servos([servo1, servo2])

# def main():
#     servo1.setPosition(1500)
#     servo2.setPosition(2000)
#
#

if __name__ == '__main__':
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        print "interrupted by user"
    finally:
    	print "cleaning up"
    	cleanup([servo1, servo2])
