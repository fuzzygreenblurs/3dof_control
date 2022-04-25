import RPi.GPIO as GPIO
from time import sleep
from math import isclose

class Prismatic():
    ENCODER_A  = 2
    ENCODER_B  = 3
    CPR        = 193
    LENGTH     = 110
    MOTOR_CW   = 25          # upwards
    MOTOR_CCW  = 24          # downwards
    P_CONTROL_MIN_DC = 35
    P_CONTROL_MAX_DC = 45

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ENCODER_A, GPIO.IN)
        GPIO.setup(self.ENCODER_B, GPIO.IN)

        GPIO.setup(self.MOTOR_CW, GPIO.OUT)
        GPIO.setup(self.MOTOR_CCW, GPIO.OUT)
        self.up_handler = GPIO.PWM(self.MOTOR_CW, 1000)
        self.down_handler = GPIO.PWM(self.MOTOR_CCW, 1000)

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

    def setup_encoder_isr(self):
        GPIO.add_event_detect(self.ENCODER_A, GPIO.RISING, callback=self.pulse_A)
        GPIO.add_event_detect(self.ENCODER_B, GPIO.RISING, callback=self.pulse_B)

    def check_direction(self):
        if GPIO.input(self.ENCODER_B) == True:
            self.dir = -1 # moving upwards
            print(f'dir: {self.dir}, upward', end='\r')
        else:
            self.dir = 1  # moving downwards
            print(f'dir: {self.dir}, downward', end='\r')

    # def pulse(self, fcn):
    #     if self.ignore_calls == 1: return 
    #     self.ignore_calls = 1
    #     return fcn()
    #     ignore_calls = 0

    # @pulse
    def pulse_A(self, _):
        if self.ignore_calls == 1: return 
        self.ignore_calls = 1

        self.check_direction()
        self.count_A += self.dir

        ignore_calls = 0

    # @pulse
    def pulse_B(self, _):
        if self.ignore_calls == 1: return 
        self.ignore_calls = 1
        
        self.count_B += self.dir

        ignore_calls = 0
    
    # def gracefully_manipulate_gpio(fcn, **args):
    #     try:
    #         cleaned_up = False
    #         fcn(args)
    #     except KeyboardInterrupt:
    #         self.up_handler.stop()
    #         self.down_handler.stop()
    #         GPIO.cleanup()
    #         print("Keyboard interrupt triggered...GPIO cleanup complete.")
    #         cleaned_up = True
    #     finally:
    #         if not cleaned_up:
    #             self.up_handler.stop()
    #             self.down_handler.stop()
    #             GPIO.cleanup()
    #             print("GPIO cleanup complete.")

    def top(self):
        self.__up(40, 2)

    def middle(self):
        self.top()
        self.__p_control(int(0.5 * self.rail_count))

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
        if not isclose(final_count_A, final_count_B, 10):
            if retries < 2:
                self.__measure_rail_pulse_count()
                retries += 1
            else:
                raise(Exception, 'rail measurement failing.')

        self.rail_count  = final_count_A
        self.current_pos = 0

    def __p_control(self, target_pos):
        error = target_pos - self.current_pos
        self.count_A = self.current_pos
        interval = 0.1

        while not isclose(abs(error), 10):
            dc = min(max(self.K_p * error, self.P_CONTROL_MIN_DC), self.P_CONTROL_MAX_DC)
            self.__down(dc, interval) if error > 0 else self.up(dc, interval)
            
            error = target_pos - self.count_A        
            print(f'error: {error}, encoder_count: {self.count_A}')