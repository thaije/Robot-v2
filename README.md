# Robot-v2

## Usefull links
[Raspberry PI pinout](https://pinout.xyz/)
[Image processing with Opencv on RPI](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_table_of_contents_imgproc/py_table_of_contents_imgproc.html)


## Audio:
- Uses a USB speaker with mic
- Install sox library
- Play audio file: play file.mp3
- Record audio file: rec file.mp3 (or .wav etc)


## RPI setup:
Parts:
- 2 HItec HS-442 servos mounted on eachother to get 2 DOF
- pi camera v2
- external battery for servos

Pin setup:
- verticalServo BCM pin=13
- horizontalServo BCM pin=18
- external battery to breadboard
- servo power to breadboard
- RPI ground to breadboard (important!)


# settings:
Ubuntu login
User fedya
Login kutraspberry

ssh: `ssh fedya@192.168.178.68`
password: `kutraspberry`
