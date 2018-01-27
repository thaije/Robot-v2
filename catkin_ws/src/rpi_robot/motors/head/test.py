
import time
import pigpio 


import pigpio


#pi.set_servo_pulsewidth(18, 0) # off pi.set_servo_pulsewidth(18, 600) # 90 degrees left 
pi.set_servo_pulsewidth(18, 1200) # 90 degrees right
time.sleep(0.1)

pi.set_servo_pulsewidth(18, 0)    # off
