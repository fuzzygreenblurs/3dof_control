# ####### RACK POSITIONER ############
import RPi.GPIO as GPIO          
from time import sleep

# GPIO.setmode(GPIO.BCM)

# ENCODER_A = 2
# ENCODER_B = 3
# GPIO.setup(ENCODER_A, GPIO.IN)
# GPIO.setup(ENCODER_B, GPIO.IN)

# COUNT_A = 0
# COUNT_B = 0
# DIR = 0          # CW = 1, CCW = -1, STOPPED = 0
# CPR = 193
# LEN = 110        # rack length = 110mm
# RACK_COUNT = 744

# ignore_calls = 0

# def check_direction():
#     global DIR
#     if GPIO.input(ENCODER_B) == True:
#         DIR = -1 # moving upward
#         print(f'dir: {DIR}, upward', end='\r')
#     else:
#         DIR = 1  # moving downward
#         print(f'dir: {DIR}, downward', end='\r')

# def pulse_A(_):
#     global ignore_calls
#     global COUNT_A, DIR

#     if ignore_calls == 1: 
#         return
#     ignore_calls = 1
    
#     check_direction()
#     COUNT_A += DIR

#     ignore_calls = 0

# def pulse_B(_):
#     global ignore_calls
#     global COUNT_B, DIR

#     if ignore_calls == 1: 
#         return
#     ignore_calls = 1

#     COUNT_B += DIR

#     ignore_calls = 0

# GPIO.add_event_detect(ENCODER_A, GPIO.RISING, callback=pulse_A)
# GPIO.add_event_detect(ENCODER_B, GPIO.RISING, callback=pulse_B)

# MOTOR_CW  = 25
# MOTOR_CCW = 24
# GPIO.setup(MOTOR_CW, GPIO.OUT)
# GPIO.setup(MOTOR_CCW, GPIO.OUT)

# up_handler = GPIO.PWM(MOTOR_CW, 1000) #f
# down_handler = GPIO.PWM(MOTOR_CCW, 1000) #b
# up_handler.start(0)
# down_handler.start(0)

# def set_rail_pulse_count():
#     global COUNT_A, COUNT_B
#     global f, b
#     try: 
#         initial_count_a = COUNT_A
#         initial_count_b = COUNT_B
        
#         up_handler.ChangeDutyCycle(80)
#         sleep(2)
#         up_handler.ChangeDutyCycle(0)

#         final_count_a = COUNT_A
#         final_count_b = COUNT_B

#         print(f'diff: {final_count_a - initial_count_a}, {final_count_b - initial_count_b}')
    
#     except KeyboardInterrupt:
#         up_handler.stop()
#         down_handler.stop()
#         GPIO.cleanup()
#         print("GPIO cleanup complete.")

# def set_to_middle():
#     global COUNT_A, COUNT_B
#     global f, b
#     # try: 
#     # start all the way at the top
#     # down_handler.ChangeDutyCycle(35)
#     # up_handler.ChangeDutyCycle(0)
#     # sleep(1)

#     try:
#         up_handler.ChangeDutyCycle(75)
#         down_handler.ChangeDutyCycle(0)
#         sleep(3)

#         middle_pos = int(0.5 * RACK_COUNT)
#         p_control(middle_pos, 0)
#     except KeyboardInterrupt:
#         up_handler.stop()
#         down_handler.stop()
#         GPIO.cleanup()

# def halt():
#     global f, b
#     try: 
#         up_handler.ChangeDutyCycle(0)
#         down_handler.ChangeDutyCycle(0)
#         sleep(2)
#     except KeyboardInterrupt:
#         up_handler.stop()
#         down_handler.stop()
#         GPIO.cleanup()
#         print("GPIO cleanup complete.")

# def bang_bang(pos):
#     global COUNT_A, COUNT_B
#     global f, b

#     try: 
#         while COUNT_A != pos:
#             up_handler.ChangeDutyCycle(35)
#             down_handler.ChangeDutyCycle(0)
#             sleep(0.1)

#             if COUNT_A > pos:
#                 up_handler.ChangeDutyCycle(0)
#                 down_handler.ChangeDutyCycle(35)
#                 sleep(0.1)

#     except KeyboardInterrupt:
#         up_handler.stop()
#         down_handler.stop()
#         GPIO.cleanup()
#         print("GPIO cleanup complete.")

# def p_control(target_pos, current_pos=0):
#     global COUNT_A
#     global f, b
#     K_p = 1

#     error = target_pos - current_pos
#     COUNT_A = current_pos
#     try: 
#         while abs(error) > 10:
#             dc = min(max(K_p * error, 35), 45)

#             if error > 0:
#                 down_handler.ChangeDutyCycle(dc)
#                 up_handler.ChangeDutyCycle(0)
#             elif error < 0:
#                 up_handler.ChangeDutyCycle(dc)
#                 down_handler.ChangeDutyCycle(0)
            
#             sleep(0.1)
#             error = target_pos - COUNT_A
#             print(f'error: {error}, count_a: {COUNT_A}')

#     except KeyboardInterrupt:
#         up_handler.stop()
#         down_handler.stop()
#         GPIO.cleanup()
#         print('GPIO cleanup complete.')

# # if __name__ == '__main__':
# #     # set_rail_pulse_count()

# #     # bang_bang(-372)
# #     set_to_middle()
# #     # halt()
# #     # p_control(372)

# #     up_handler.stop()
# #     down_handler.stop()
# #     GPIO.cleanup()
# #     print("GPIO cleanup complete.")

####### RACK POSITIONER ############

##### REVOLUTE SERVO POSITIONS #####
# from time import sleep
# import RPi.GPIO as GPIO          
import pigpio
import warnings

base  = 18
elbow = 19
pwm = pigpio.pi()
pwm.set_mode(base, pigpio.OUTPUT)
pwm.set_mode(elbow, pigpio.OUTPUT)

class Revolute():
    ABSOLUTE_MIN_DC = 501
    ABSOLUTE_MAX_DC = 2499

    @classmethod
    def converted_dc(cls, angle):
        if angle < cls.MIN_ANGLE or angle > cls.MAX_ANGLE:
            msg = f'{angle} is outside joint bounds: {cls.MIN_ANGLE} <= \u03B8 <= {cls.MAX_ANGLE}'
            warnings.warn(msg)
        
        slope = (cls.MAX_ANGLE_DC - cls.MIN_ANGLE_DC)/(cls.MAX_ANGLE - cls.MIN_ANGLE)
        dc = slope*(max(angle, cls.MIN_ANGLE)) + cls.MIN_ANGLE_DC
        
        return round(min(max(dc, cls.ABSOLUTE_MIN_DC), cls.ABSOLUTE_MAX_DC), 3)

class Base(Revolute):
    MIN_ANGLE           = 15
    MAX_ANGLE           = 180
    MIN_ANGLE_DC        = 500
    MAX_ANGLE_DC        = 2250
    ZERO_POSITION_ANGLE = 15
    ZERO_POSITION_DC    = 600

class Elbow(Revolute):
    MIN_ANGLE           = 0
    MAX_ANGLE           = 180
    MIN_ANGLE_DC        = 500
    MAX_ANGLE_DC        = 2250
    ZERO_POSITION_ANGLE = 90
    ZERO_POSITION_DC    = 1350

# positions = [700, 1000, 1500, 2000, 2300, 2000, 1500, 1000, 700]

# try:
#     for i in positions:
#         print(f'{i}')
#         pwm.set_servo_pulsewidth(elbow, i)
#         # for j in positions:
#         #     pwm.set_servo_pulsewidth(elbow, j)
#         #     print(f'{i}, {j}')
#         sleep(1)

try:
    # pass
    # start at zero position - 
    print('base ~15deg - 600, ~180deg - 2400')
    print('elbow - 90deg - 1350, 0deg - 500, 180deg - 2400' )
    # pwm.set_servo_pulsewidth(elbow, 2400)
    # sleep(1)

    # pwm.set_servo_pulsewidth(elbow, 2400)    
    # sleep(2)

    print(Base.converted_dc(200))

    # pwm.set_servo_pulsewidth(elbow, 1350)    
    # sleep(2)

    # for dc in range(2400, 600, -200):
    #     pwm.set_servo_pulsewidth(base, dc)
    #     sleep(1)

    # for dc in range(2400, 1350, -50):
    #     pwm.set_servo_pulsewidth(elbow, dc)
    #     sleep(1)


    # pwm.set_servo_pulsewidth(elbow, )
    # sleep(1)

    # ingest camera coordinates - transform into physical coordinates
    # calculate inverse kinematics values
    # base go to base_position
    # elbow go to elbow_position
    # activate coil
    # end effector to z = 0
    # end effector to height = 50%
    # 

except KeyboardInterrupt:
    # turning off servo
    pwm.set_PWM_dutycycle(base, 0)
    pwm.set_PWM_frequency(base, 0 )
    # pwm.set_PWM_dutycycle(elbow, 0)
    # pwm.set_PWM_frequency(elbow, 0 )
    GPIO.cleanup()
    print("GPIO cleanup complete.")
finally:
    pwm.set_PWM_dutycycle(base, 0)
    pwm.set_PWM_frequency(base, 0)
    pwm.set_PWM_dutycycle(elbow, 0)
    pwm.set_PWM_frequency(elbow, 0)
    GPIO.cleanup()
    print("GPIO cleanup complete.")