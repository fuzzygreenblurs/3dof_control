# ####### RACK POSITIONER ############
import RPi.GPIO as GPIO          
from time import sleep
import math
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
    # signal bounds to avoid damaging HW
    ABSOLUTE_MIN_DC = 500
    ABSOLUTE_MAX_DC = 2500

    @classmethod
    def converted_dc(cls, angle):
        if angle < cls.MIN_ANGLE or angle > cls.MAX_ANGLE:
            msg = f'{angle} is outside joint bounds: {cls.MIN_ANGLE} <= \u03B8 <= {cls.MAX_ANGLE}'
            warnings.warn(msg)
        
        slope = (cls.MAX_ANGLE_DC - cls.MIN_ANGLE_DC)/(cls.MAX_ANGLE - cls.MIN_ANGLE)
        dc = slope*(max(angle, cls.MIN_ANGLE)) + cls.MIN_ANGLE_DC
        
        return round(min(max(dc, cls.ABSOLUTE_MIN_DC), cls.ABSOLUTE_MAX_DC), 3)

    def __init__(self, pwm):
        self.angle = None
        self.pwm = pwm
        self.pwm.set_mode(self.PIN, pigpio.OUTPUT)

    def go_to(self, angle):
        self.pwm.set_servo_pulsewidth(self.PIN, self.converted_dc(angle))
        sleep(2)

class Base(Revolute):
    PIN                 = 18
    MIN_ANGLE           = 15
    MAX_ANGLE           = 180
    MIN_ANGLE_DC        = 500
    MAX_ANGLE_DC        = 2250
    ZERO_POSITION_ANGLE = 15
    ZERO_POSITION_DC    = 600

class Elbow(Revolute):
    PIN                 = 19
    MIN_ANGLE           = 0
    MAX_ANGLE           = 180
    MIN_ANGLE_DC        = 500
    MAX_ANGLE_DC        = 2250
    ZERO_POSITION_ANGLE = 90
    ZERO_POSITION_DC    = 1350

class Prismatic():
    ENCODER_A  = 2
    ENCODER_B  = 3
    CPR        = 193
    LENGTH     = 110
    MOTOR_CW   = 25          # upwards
    MOTOR_CCW  = 24          # downwards
    P_CONTROL_MIN_DC = 35
    P_CONTROL_MAX_DC = 45

    def __init__():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ENCODER_A, GPIO.IN)
        GPIO.setup(self.ENCODER_B, GPIO.IN)

        GPIO.setup(self.MOTOR_CW, GPIO.OUT)
        GPIO.setup(self.MOTOR_CCW, GPIO.OUT)
        self.up_handler = GPIO.PWM(MOTOR_CW, 1000)
        self.down_handler = GPIO.PWM(MOTOR_CCW, 1000)

        self.dir         = 0        # UP(CW) = -1, DOWN(CCW) = 1, STOPPED = 0
        self.count_A     = 0
        self.count_B     = 0
        self.rail_count  = 744
        self.K_p         = 1
        self.current_pos = 0

        self.ignore_calls = 0
        self.setup_encoder_isr()

        self.up_handler.start(0)
        self.down_handler.start(0)

    def setup_encoder_isr():
        GPIO.add_event_detect(self.ENCODER_A, GPIO.RISING, callback=self.pulse_A)
        GPIO.add_event_detect(self.ENCODER_B, GPIO.RISING, callback=self.pulse_B)

    def check_direction(self):
        if GPIO.input(self.ENCODER_B) == True:
            self.dir = -1 # moving upwards
            print(f'dir: {self.dir}, upward', end='\r')
        else:
            self.dir = 1  # moving downwards
            print(f'dir: {self.dir}, downward', end='\r')

    def pulse(fcn):
        if self.ignore_calls == 1: return 
        self.ignore_calls = 1
        return fcn()
        ignore_calls = 0

    @pulse
    def pulse_A():
        self.check_direction()
        self.count_A += self.dir

    @pulse
    def pulse_B():
        self.count_B += self.dir
    
    def gracefully_manipulate_gpio(fcn, **args):
        try:
            cleaned_up = False
            fcn(args)
        except KeyboardInterrupt:
            self.up_handler.stop()
            self.down_handler.stop()
            GPIO.cleanup()
            print("Keyboard interrupt triggered...GPIO cleanup complete.")
            cleaned_up = True
        finally:
            if not cleaned_up:
                self.up_handler.stop()
                self.down_handler.stop()
                GPIO.cleanup()
                print("GPIO cleanup complete.")

    def top(self):
        self.__up(40, 2)

    def middle(self):
        self.top()
        p_control(int(0.5 * self.rail_count))

    def bottom(self):
        self.__down(40, 2)

    def halt(self, duration=3):
        self.__up(0)
        self.__down(0)
        sleep(duration)

    def __up(self, dc, duration):
        self.up_handler.ChangeDutyCycle(dc)
        self.down_handler.ChangeDutyCycle(0)
        sleep(duration)

    def __down(self, dc, duration):
        self.down_handler.ChangeDutyCycle(dc)
        self.up_handler.ChangeDutyCycle(0)
        sleep(duration)

    def __measure_rail_pulse_count(self):
        initial_count_A, initial_count_B = self.count_A, self.count_B
        self.__up(80, 2)
        final_count_A, final_count_B = self.count_A, self.count_B

        retries = 0
        if not math.isclose(final_count_A, final_count_B, 10):
            if retries < 2:
                self.__measure_rail_pulse_count()
                retries += 1
            else:
                raise(Exception, 'rail measurement failing.')

        self.rail_count  = final_count_A
        self.current_pos = 0

    def __p_control(self, target_pos):
        error = target_pos - self.current_pos
        self.count_A = current_pos
        interval = 0.1

        while not math.isclose(abs(error), 10):
            dc = min(max(self.K_p * error, P_CONTROL_MIN_DC), P_CONTROL_MAX_DC)
            self.down(dc, interval) if error > 0 else self.up(dc, interval)
            
            error = target_pos - self.count_A        
            print(f'error: {error}, encoder_count: {self.count_A}')

class Coil():
    def __init__(self):
        self.pin = 21
        GPIO.setup(21, GPIO.OUT)

    def engage():
        GPIO.output(self.pin, 1)

    def disengage():
        GPIO.output(self.pin, 0)

class Manipulator():
    BASE_PIN  = 18
    ELBOW_PIN = 19

    A_1 = 1
    A_2 = 1
    A_3 = 1
    A_4 = 1
    A_5 = 1

    def __init__(self):
        pwm = pigpio.pi()

        self.base = Base(pwm)
        self.elbow = Elbow(pwm)
        self.prismatic = PrismaticJoint()
        self.coil = Coil()

    def zero():
        self.prismatic.middle()
        self.base.go_to(30)
        self.elbow.go_to(self.elbow.ZERO_POSITION_ANGLE)
        self.prismatic.top()
        self.base.go_to(self.base.ZERO_POSITION_ANGLE)

    def go_to(X=0, Y=0):
        if X == 0 and Y == 0:
            return self.zero()

        R_1 = math.sqrt((X**2) + (Y**2))

        self.prismatic.middle()
        self.base.go_to(base_angle(X, Y, R_1))
        self.elbow.go_to(elbow_angle(X, Y, R_1))

    def pick_and_place(X, Y):
        self.go_to(X, Y)
        
        self.coil.engage()
        self.prismatic.down()

        self.zero()
        self.coil.disengage()

    # inverse kinematics
    def __base_angle(X, Y, R_1):
        p = math.atan(Y/X)
        q = ((self.A_4**2) - (self.A_2**2) - (R_1**2))/(2*(self.A_2)*R_1)
        return math.atan(p) - math.acos(q)

    def __elbow_angle(X, Y, R_1):
        n = ((self.A_2**2) + (self.A_4**2) - (R_1**2))
        d = (2 * (A_2) * (A_4))
        return 180 - acos(n/d)

if __name__ == '__main__':
    try:
        cleaned_up = False
        manipulator = Manipulator()

        # read coordinates



    except KeyboardInterrupt:
        self.up_handler.stop()
        self.down_handler.stop()
        GPIO.cleanup()
        print("Keyboard interrupt triggered...GPIO cleanup complete.")
        cleaned_up = True
    finally:
        if not cleaned_up:
            self.up_handler.stop()
            self.down_handler.stop()
            GPIO.cleanup()
            print("GPIO cleanup complete.")



# try:
#     # pass
#     # start at zero position - 
#     print('base ~15deg - 600, ~180deg - 2400')
#     print('elbow - 90deg - 1350, 0deg - 500, 180deg - 2400' )
#     # pwm.set_servo_pulsewidth(elbow, 2400)
#     # sleep(1)

#     # pwm.set_servo_pulsewidth(elbow, 2400)    
#     # sleep(2)

#     print(Base.converted_dc(200))

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