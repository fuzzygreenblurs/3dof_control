import RPi.GPIO as GPIO          
import time

GPIO.setmode(GPIO.BCM)

COIL = 21
GPIO.setup(COIL, GPIO.OUT)

try:
    GPIO.output(COIL, 1)
    print('on...')
    time.sleep(10)

    GPIO.output(COIL, 0)
    print('off')
    time.sleep(3)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO cleanup complete.")
finally:
    GPIO.cleanup()
    print("GPIO cleanup complete.")