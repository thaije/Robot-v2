## How to ROS
- Topic: node publishes messages, node subscribed to a topic can receive these messages
- Services: A client node sends a request (what is 2+1?) to a Service node, the service node sends a response(2+1=3) back to the client
- Parameters: rosparam can be used to set, get, load, dump, delete and list parameters (e.g. intialization paramters).

### Topic publisher / Subscriber
- copy listener and talker from beginner_tutorials/scripts
- chmod +x file_name.py (for both files)
- roscore
- rosrun package_name listener.py/talker.py or listener/talker(for cpp)

# Hardware
## Parts:
- Raspberry pi 2b
- 2 V-tec 6v 177 RPM DC motors with double hall encoders (https://eckstein-shop.de/V-TEC-6V-Mini-25D-DC-Motor-Getriebe-Motor-Stirnradgetriebe-mit-Encoder-177-RPM-EN)
- 2 Pololu Wheel 90×10mm Pair - Black
- SN754410 H-bridge for DC motor control
- Castor/ ball wheel
- 2 Hitec HS-422 180 degree servo's with pan-tilt set
- Raspberry pi v2 camera mounted on pan-tilt set
- 3 HC-SR04 sonars, 1 mounted on pan-tilt set, 2 mounted at front at a 20°.
- Xiaomi 10000 mAh powerbank for rpi
- 3300 mAh NiMh battery for servos / dc motors
- 2 Pinout boards
- Pinout cables
 Wiring GPIO

## Wiring

### DC motors
- sn75 flipped to right, pins mentioned are BCM pin numbers
- BCM pin 23 - sn75 left 7
- BCM pin 24 - sn75 left 1
- BCM pin 10 - sn75 right 7
- BCM pin 9 - sn75 right 8
- BCM pin 25 - sn75 left 2
- BCM pin 11 - sn75 right 2
- Pin 2 (5v) - sn75 right 1
- Connect 6v external power to pinout board
- Connect pinout board + (6v) to sn75 left 8
- Pinout board ground to RPI ground
- Pinout board ground to: sn75 left 4 / 5 / sn75 right 4 / 5 (all 4)
- DC motor 1 red (m1) sn75 right 3
- DC motor 1 white(m2) to sn75 right 6
- DC motor 2 red(m1) to sn75 left 3
- DC motor 2 white(m2) to sn75 left 6

### DC motors encoder wiring
- 3v3 from rpi (pin 1) to pinout board (not same side as 6v)
- ground from rpi to pinout board
- 3v3 input pins from encoders to pinout board +
- ground pins from encoders to pinout board ground
- Right motor encoder output 1 green (cm2) to BCM pin 17
- Right motor encoder output 2 yellow (cm1) to BCM pin 27
- Left motor encoder ouput 1 green (cm2) to BCM pin 14
- Left motor encoder ouput 2 yellow(cm1) to BCM pin 15
