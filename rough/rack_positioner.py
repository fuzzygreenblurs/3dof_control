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
LEN = 110        # rack length = 110mm
RACK_COUNT = 744

ignore_calls = 0

def check_direction():
    global DIR
    if GPIO.input(ENCODER_B) == True:
        DIR = -1 # moving upward
        print(f'dir: {DIR}, upward', end='\r')
    else:
        DIR = 1  # moving downward
        print(f'dir: {DIR}, downward', end='\r')

def pulse_A(_):
    global ignore_calls
    global COUNT_A, DIR

    if ignore_calls == 1: 
        return
    ignore_calls = 1
    
    check_direction()
    COUNT_A += DIR

    ignore_calls = 0

def pulse_B(_):
    global ignore_calls
    global COUNT_B, DIR

    if ignore_calls == 1: 
        return
    ignore_calls = 1

    COUNT_B += DIR

    ignore_calls = 0

GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=pulse_A)
GPIO.add_event_detect(ENCODER_B, GPIO.RISING, callback=pulse_B)

MOTOR_CW  = 25
MOTOR_CCW = 24
GPIO.setup(MOTOR_CW, GPIO.OUT)
GPIO.setup(MOTOR_CCW, GPIO.OUT)

up_handler = GPIO.PWM(MOTOR_CW, 1000) #f
down_handler = GPIO.PWM(MOTOR_CCW, 1000) #b
up_handler.start(0)
down_handler.start(0)

def set_rail_pulse_count():
    global COUNT_A, COUNT_B
    global f, b
    try: 
        initial_count_a = COUNT_A
        initial_count_b = COUNT_B
        
        up_handler.ChangeDutyCycle(80)
        sleep(2)
        up_handler.ChangeDutyCycle(0)

        final_count_a = COUNT_A
        final_count_b = COUNT_B

        print(f'diff: {final_count_a - initial_count_a}, {final_count_b - initial_count_b}')
    
    except KeyboardInterrupt:
        up_handler.stop()
        down_handler.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete.")

def set_to_middle():
    global COUNT_A, COUNT_B
    global f, b
    # try: 
    # start all the way at the top
    # down_handler.ChangeDutyCycle(35)
    # up_handler.ChangeDutyCycle(0)
    # sleep(1)

    try:
        up_handler.ChangeDutyCycle(75)
        down_handler.ChangeDutyCycle(0)
        sleep(3)

        middle_pos = int(0.5 * RACK_COUNT)
        p_control(middle_pos, 0)
    except KeyboardInterrupt:
        up_handler.stop()
        down_handler.stop()
        GPIO.cleanup()

def halt():
    global f, b
    try: 
        up_handler.ChangeDutyCycle(0)
        down_handler.ChangeDutyCycle(0)
        sleep(2)
    except KeyboardInterrupt:
        up_handler.stop()
        down_handler.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete.")

def bang_bang(pos):
    global COUNT_A, COUNT_B
    global f, b

    try: 
        while COUNT_A != pos:
            up_handler.ChangeDutyCycle(35)
            down_handler.ChangeDutyCycle(0)
            sleep(0.1)

            if COUNT_A > pos:
                up_handler.ChangeDutyCycle(0)
                down_handler.ChangeDutyCycle(35)
                sleep(0.1)

    except KeyboardInterrupt:
        up_handler.stop()
        down_handler.stop()
        GPIO.cleanup()
        print("GPIO cleanup complete.")

def p_control(target_pos, current_pos=0):
    global COUNT_A
    global f, b
    K_p = 1

    error = target_pos - current_pos
    COUNT_A = current_pos
    try: 
        while abs(error) > 10:
            dc = min(max(K_p * error, 35), 45)

            if error > 0:
                down_handler.ChangeDutyCycle(dc)
                up_handler.ChangeDutyCycle(0)
            elif error < 0:
                up_handler.ChangeDutyCycle(dc)
                down_handler.ChangeDutyCycle(0)
            
            sleep(0.1)
            error = target_pos - COUNT_A
            print(f'error: {error}, count_a: {COUNT_A}')

    except KeyboardInterrupt:
        up_handler.stop()
        down_handler.stop()
        GPIO.cleanup()
        print('GPIO cleanup complete.')

if __name__ == '__main__':
    # set_rail_pulse_count()

    # bang_bang(-372)
    set_to_middle()
    # halt()
    # p_control(372)

    up_handler.stop()
    down_handler.stop()
    GPIO.cleanup()
    print("GPIO cleanup complete.")

