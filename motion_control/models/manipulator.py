from base import Base
from elbow import Elbow
from prismatic import Prismatic
from coil import Coil

import RPi.GPIO as GPIO          
import pigpio

class Manipulator():
    BASE_PIN  = 18
    ELBOW_PIN = 19

    A_1 = 1
    A_2 = 1
    A_3 = 1
    A_4 = 1
    A_5 = 1

    def __init__(self):
        self.pwm = pigpio.pi()
        self.base = Base(self.pwm)
        self.elbow = Elbow(self.pwm)
        self.prismatic = Prismatic()
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