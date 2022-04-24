import warnings

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