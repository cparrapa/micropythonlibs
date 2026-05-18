import machine
from machine import Pin, PWM
import time
from ottomotor import OttoMotor

wheell = PWM(Pin(14), freq=50)
wheelr = PWM(Pin(13), freq=50)
anglel = PWM(Pin(27), freq=50)
angler = PWM(Pin(15), freq=50)

steplength = .25

def wheel(servo, speed):
    min_duty = 20
    max_duty = 130
    duty = int((speed/10)*(max_duty - min_duty) + min_duty)
    servo.duty(duty)
    
def angle(servo, angle):
    min_duty = 70
    max_duty = 100
    duty = int((angle/180) * (max_duty - min_duty) + min_duty)
    print(angle)
    servo.duty(duty)

var = 0

angle(angler, 90)

while True:
    angle(anglel, var)
    time.sleep(.01)
    var += 2
    if var > 180:
        var = 0
    print(var)