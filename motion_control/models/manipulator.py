from models.elbow import Elbow
from models.prismatic import Prismatic
from models.coil import Coil
from models.base import Base
from time import sleep
import math

import RPi.GPIO as GPIO          
import pigpio

class Manipulator():
    BASE_PIN  = 18
    ELBOW_PIN = 19

    # cm
    A_2 = 5.70
    A_4 = 5.70

    def __init__(self):
        self.pwm = pigpio.pi()
        self.base = Base(self.pwm)
        self.elbow = Elbow(self.pwm)
        self.prismatic = Prismatic()
        self.coil = Coil()

    def zero(self):
        self.base.go_to(45)
        self.elbow.go_to(self.elbow.ZERO_POSITION_ANGLE)
        self.prismatic.top()
        self.base.go_to(self.base.ZERO_POSITION_ANGLE)


    def go_to(self, X=0, Y=0):
        if X == 0 and Y == 0:
            return self.zero()

        R_1 = math.sqrt((X**2) + (Y**2))

        # self.prismatic.middle()
        self.base.go_to(self.__base_angle(X, Y, R_1))
        self.elbow.go_to(self.__elbow_angle(X, Y, R_1))

    def pick_and_place(self, X, Y):
        self.go_to(X, Y)
        
        self.coil.engage()
        self.prismatic.down()

        self.zero()
        self.coil.disengage()

    # inverse kinematics
    def __base_angle(self, X, Y, R_1):
        phi_3 = math.atan(X/Y) * 180/math.pi
        
        num = (self.A_2 ** 2) + (R_1 ** 2) - (self.A_4 ** 2)
        den = 2 * self.A_2 * R_1

        phi_1 = math.acos(num/den) * 180/math.pi

        # 2nd quadrant --> add 90
        result = phi_3 + phi_1 + 90 
        # print(f'phi1: {phi_1}, phi3: {phi_3}, result: {result}')
        print(f'result: {result}')
        return result 

    def __elbow_angle(self, X, Y, R_1):
        num = (self.A_2 ** 2) + (self.A_4 ** 2) - (R_1 ** 2)
        den = 2 * self.A_2 * self.A_4

        result = abs((math.acos(num/den) * 180/math.pi) - 180)
        print(result)
        return result

