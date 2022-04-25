import RPi.GPIO as GPIO

class Coil():
    PIN = 21
    def __init__(self):
        GPIO.setup(self.PIN, GPIO.OUT)

    def engage():
        GPIO.output(self.PIN, 1)

    def disengage():
        GPIO.output(self.PIN, 0)