# from time import sleep
from time import sleep
import RPi.GPIO as GPIO          
import pigpio

base  = 18
elbow = 19
pwm = pigpio.pi()
pwm.set_mode(base, pigpio.OUTPUT)
pwm.set_mode(elbow, pigpio.OUTPUT)

positions = [700, 1000, 1500, 2000, 2300, 2000, 1500, 1000, 700]

try:
    for i in positions:
        pwm.set_servo_pulsewidth(base, i)
        for j in positions:
            pwm.set_servo_pulsewidth(elbow, j)
            print(f'{i}, {j}')
            sleep(1)

except KeyboardInterrupt:
    # turning off servo
    pwm.set_PWM_dutycycle(base, 0)
    pwm.set_PWM_frequency(base, 0 )
    pwm.set_PWM_dutycycle(elbow, 0)
    pwm.set_PWM_frequency(elbow, 0 )
    GPIO.cleanup()
    print("GPIO cleanup complete.")
finally:
    pwm.set_PWM_dutycycle(base, 0)
    pwm.set_PWM_frequency(base, 0 )
    pwm.set_PWM_dutycycle(elbow, 0)
    pwm.set_PWM_frequency(elbow, 0 )
    GPIO.cleanup()
    print("GPIO cleanup complete.")

# GPIO.setmode(GPIO.BCM)

# BASE_SERVO  = 18
# # ELBOW_SERVO = 22

# GPIO.setup(BASE_SERVO, GPIO.OUT)
# # GPIO.setup(ELBOW_SERVO, GPIO.OUT)

# base_handler  = GPIO.PWM(BASE_SERVO, 1000)
# # elbow_handler = GPIO.PWM(ELBOW_SERVO, 1000)

# base_handler.start(0)

# try: 
#     while True:
#         for i in range(100):
#             print(i)
#             base_handler.ChangeDutyCycle(i)
#             sleep(0.2)

# except KeyboardInterrupt:
#     base_handler.stop()
#     # elbow_handler.stop()
#     GPIO.cleanup()
#     print("GPIO cleanup complete.")
