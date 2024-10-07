import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
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

while True:
    servo_leftleg.write(90)
    servo_rightleg.write(90)
    time.sleep(1)
    servo_leftleg.write(0)
    servo_rightleg.write(180)
    time.sleep(1)
    servo_leftfoot.write(0)
    servo_rightfoot.write(180)
    time.sleep(3)
    servo_leftfoot.write(90)
    servo_rightfoot.write(90)
    time.sleep(2)
    servo_leftfoot.write(180)
    servo_rightfoot.write(0)
    time.sleep(1)