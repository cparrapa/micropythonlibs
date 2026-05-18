import machine
from machine import Pin, PWM
import time
from ottomotor import OttoMotor

wheell = PWM(Pin(14), freq=50)
wheelr = PWM(Pin(13), freq=50)
anglel = PWM(Pin(27), freq=50)
angler = PWM(Pin(15), freq=50)

steplength = .25
fadedelay = .05

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
    
def gap():
    time.sleep(.5)
    
def stand():
    angle(anglel, 15)
    angle(angler, 165)
    
def left():
    angle(angler, 220)
    angle(anglel, 40)
    gap()
    g = 40
    while g != 90:
        print(g)
        angle(anglel, g)
        g += 5
        time.sleep(fadedelay)
    print("Transition successfull.")
    wheel(wheell, 6)
    time.sleep(.5)
    wheel(wheell, 5)
    gap()
    while g != 30:
        print(g)
        angle(anglel, g)
        g -= 5
        time.sleep(fadedelay)
    stand()
    gap()

def right():
    angle(anglel, -100)
    angle(angler, 140)
    gap()
    g = 140
    while g != 85:
        print(g)
        angle(angler, g)
        g -= 5
        time.sleep(fadedelay)
    wheel(wheelr, 4)
    time.sleep(.5)
    wheel(wheelr, 5)
    gap()
    while g != 165:
        print(g)
        angle(angler, g)
        g += 5
        time.sleep(fadedelay)
    stand()
    gap()

stand()
gap()

while True:
    left()
    right()
