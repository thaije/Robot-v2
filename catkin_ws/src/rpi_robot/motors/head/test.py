
import pigpio
import time

pi = pigpio.pi()
pi.set_mode(18, pigpio.INPUT)
pi.set_mode(13, pigpio.INPUT)

#pi.set_servo_pulsewidth(18, 0)    # off
#pi.set_servo_pulsewidth(18, 600) # 90 degrees left
#time.sleep(0.5)
#pi.set_servo_pulsewidth(18, 2400) # 90 degrees right
#time.sleep(0.5)
#pi.set_servo_pulsewidth(18,1500)
#time.sleep(0.5)
pi.set_servo_pulsewidth(18, 0)    # off

pi.set_servo_pulsewidth(13, 0) # off
pi.set_servo_pulsewidth(13, 1750) # 90 degrees up
time.sleep(0.5)
pi.set_servo_pulsewidth(13, 600) # max down
time.sleep(0.5)
pi.set_servo_pulsewidth(13, 800) #middle
time.sleep(0.5)
pi.set_servo_pulsewidth(13, 0) # off
