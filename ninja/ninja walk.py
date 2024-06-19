import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
from ottomotor import Servo

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer

# angle servo motors
servo_leftleg=Servo()
servo_leftleg.attach(27)	# Connector 8
servo_rightleg=Servo()
servo_rightleg.attach(15)	# Connector 9

# wheel servo motors
servo_leftfoot=Servo()
servo_leftfoot.attach(14)	# Connector 10
servo_rightfoot=Servo()
servo_rightfoot.attach(13)	# Connector 11

delay = 0.5
while True:
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    time.sleep(delay)
    servo_rightleg.write(107)
    servo_leftleg.write(125)
    time.sleep(delay)
    servo_rightfoot.write(125)
    time.sleep(delay)
    servo_rightfoot.write(90)
    time.sleep(delay)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    time.sleep(delay)
    servo_rightleg.write(46)
    servo_leftleg.write(54)
    time.sleep(delay)
    servo_leftfoot.write(55)
    time.sleep(delay)
    servo_leftfoot.write(90)
    time.sleep(delay)
