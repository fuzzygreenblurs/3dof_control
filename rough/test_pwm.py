import RPi.GPIO as GPIO          
from time import sleep

GPIO.setmode(GPIO.BCM)

ENCODER_A = 2
ENCODER_B = 3
GPIO.setup(ENCODER_A, GPIO.IN)
GPIO.setup(ENCODER_B, GPIO.IN)

COUNT_A = 0
COUNT_B = 0
DIR = 0          # CW = 1, CCW = -1, STOPPED = 0
CPR = 193

def check_direction():
    global DIR
    if GPIO.input(ENCODER_B) == True:
        DIR = 1
        print('clockwise', end='\r')
    else:
        DIR = -1
        print('counterclockwise', end='\r')

def pulse_A(_):
    global COUNT_A, DIR
    check_direction()
    COUNT_A += DIR

def pulse_B(_):
    global COUNT_B, DIR
    COUNT_B += DIR

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

if __name__ == '__main__':
    try: 
        while True:
            for i in range(0, 101):
                f.ChangeDutyCycle(i)
                sleep(0.1)

            for i in range(100, 0, -1):
                f.ChangeDutyCycle(i)
                sleep(0.1)

            for i in range(0, 101):
                b.ChangeDutyCycle(i)
                sleep(0.1)

            for i in range(100, 0, -1):
                b.ChangeDutyCycle(i)
                sleep(0.1)
            
            sleep(1)


        # while True:
        #     print(COUNT_A, COUNT_B, end='\r')

    except KeyboardInterrupt:
        f.stop()
        b.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete.")