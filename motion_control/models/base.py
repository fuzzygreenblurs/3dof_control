from revolute import Revolute

class Base(Revolute):
    PIN                 = 18
    MIN_ANGLE           = 15
    MAX_ANGLE           = 180
    MIN_ANGLE_DC        = 500
    MAX_ANGLE_DC        = 2250
    ZERO_POSITION_ANGLE = 15
    ZERO_POSITION_DC    = 600