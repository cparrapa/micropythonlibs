import machine                       #importing machine libraries
from time import sleep               #importing sleep class
from machine import Pin, PWM         #importing Pin and PWM classes
from ottomotor import Servo

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

delay = 0.1
while True:
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(delay)
    
    servo_rightleg.write(150) #107
    servo_leftleg.write(120) #125
    sleep(delay)
    servo_leftfoot.write(180) #125
    sleep(0.5)
    servo_leftfoot.write(90)
    sleep(delay)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(delay)
    servo_rightleg.write(60) #46
    servo_leftleg.write(30) #54
    sleep(delay)
    servo_rightfoot.write(0) #55
    sleep(0.5)
    servo_rightfoot.write(90)
    sleep(delay)
