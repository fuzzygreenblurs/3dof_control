from models.revolute import Revolute

class Elbow(Revolute):
    PIN                 = 19
    MIN_ANGLE           = 0
    MAX_ANGLE           = 130
    MIN_ANGLE_DC        = 1900
    MAX_ANGLE_DC        = 513.33
    ZERO_POSITION_ANGLE = 0
    ZERO_POSITION_DC    = 1900