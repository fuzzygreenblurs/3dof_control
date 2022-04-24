import RPi.GPIO as GPIO
from time import sleep

class TranslationalJoint():
    GPIO.setmode(GPIO.BCM)
    ENCODER_A = 2
    ENCODER_B = 3
    GPIO.setup(ENCODER_A, GPIO.IN)
    GPIO.setup(ENCODER_B, GPIO.IN)

    COUNT_A = 0
    COUNT_B = 0
    DIR = 0          # CW = 1, CCW = -1, STOPPED = 0
    CPR = 193
    LEN = 110        # rack length = 110mm
    RACK_COUNT = 744

    GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=pulse_A)
    GPIO.add_event_detect(ENCODER_B, GPIO.RISING, callback=pulse_B)

    MOTOR_CW  = 25
    MOTOR_CCW = 24
    GPIO.setup(MOTOR_CW, GPIO.OUT)
    GPIO.setup(MOTOR_CCW, GPIO.OUT)

    f = GPIO.PWM(MOTOR_CW, 1000)
    b = GPIO.PWM(MOTOR_CCW, 1000)
    f.start(0)
    b.start(0)

    @classmethod
    def _check_direction(cls):
        if GPIO.input(ENCODER_B) == True:
            cls.DIR = 1
            print('clockwise/upwards', end='\r')
        else:
            cls.DIR = -1
            print('counterclockwise/downward', end='\r')

    @classmethod
    def pulse_A(cls, _):
        check_direction()
        cls.COUNT_A += cls.DIR

    @classmethod
    def pulse_B(cls, _):
        cls.COUNT_B += cls.DIR

    @classmethod
    def set_rail_pulse_count(cls):
        try: 
            initial_count_a = cls.COUNT_A
            initial_count_b = cls.COUNT_B
            
            cls.f.ChangeDutyCycle(80)
            sleep(2)
            cls.f.ChangeDutyCycle(0)

            final_count_a = cls.COUNT_A
            final_count_b = cls.COUNT_B

            print(f'diff: {final_count_a - initial_count_a}, {final_count_b - initial_count_b}')

        finally:
            cls.cleanup()

    @classmethod
    def cleanup(cls):
        cls.f.stop()
        cls.b.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete.")

TranslationalJoint.set_rail_pulse_count()