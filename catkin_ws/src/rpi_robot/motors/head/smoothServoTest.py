import servoPWM as servoControl

servos = False

def setup():
    global servos
    servos = servoControl.initialize_default_servos()

def cleanup():
    servoControl.cleanup_servos(servos)

def main():
    servos[0].setPosition(1500)
    servos[1].setPosition(2000)


if __name__ == '__main__':
    setup()
    try:
        main()
    except KeyboardInterrupt:
        print "interrupted by user"
    finally:
    	print "cleaning up"
    	cleanup()
