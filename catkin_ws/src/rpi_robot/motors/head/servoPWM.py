
import pigpio


pi = pigpio.pi()
pi.set_mode(18, pigpio.INPUT)
pi.set_mode(13, pigpio.INPUT)

pi.set_servo_pulsewidth(18, 0)    # off
pi.set_servo_pulsewidth(18, 600) # 90 degrees left
pi.set_servo_pulsewidth(18, 2400) # 90 degrees right
pi.set_servo_pulsewidth(18, 0)    # off

pi.set_servo_pulsewidth(13, 0) # off
pi.set_servo_pulsewidth(13, 1750) # 90 degrees up
pi.set_servo_pulsewidth(13, 600) # max down
pi.set_servo_pulsewidth(13, 0) # off
