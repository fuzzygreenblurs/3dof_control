import RPi.GPIO as GPIO          
import math
import pigpio

from time import sleep
from models.manipulator import Manipulator
from models.prismatic import Prismatic

GPIO.setmode(GPIO.BCM)

def cleanup(msg):
    manipulator.pwm.set_PWM_dutycycle(manipulator.base.PIN, 0)
    manipulator.pwm.set_PWM_frequency(manipulator.base.PIN, 0)
    manipulator.pwm.set_PWM_dutycycle(manipulator.elbow.PIN, 0)
    manipulator.pwm.set_PWM_frequency(manipulator.elbow.PIN, 0)
    manipulator.prismatic.up_handler.stop()
    manipulator.prismatic.down_handler.stop()
    GPIO.cleanup()
    print(f'\n{msg}')

if __name__ == '__main__':
    try:
        cleaned_up = False
        manipulator = Manipulator()
        
        # start on the other side of the camera harness with the rail down
        # manipulator.zero() # should position on top of the recepticle

        manipulator.go_to(-3, 5)
    except KeyboardInterrupt:
        cleanup('Keyboard interrupt triggered...GPIO cleanup complete.')
        cleaned_up = True
    finally:
        if not cleaned_up: cleanup('GPIO cleanup complete.')