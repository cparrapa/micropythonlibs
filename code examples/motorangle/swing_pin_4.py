#motorized bumper sequence

import machine
from machine import Pin, PWM
import time

bumper = PWM(Pin(4), freq=50)

def angle(servo, angle):
    min_duty = 70
    max_duty = 100
    duty = int((angle/180) * (max_duty - min_duty) + min_duty)
    print(angle)
    servo.duty(duty)
    
while True:
    angle(bumper, 20)
    time.sleep(2)
    angle(bumper, 150)
    time.sleep(2)