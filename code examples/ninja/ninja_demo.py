import machine                       #importing machine libraries
from time import sleep               #importing sleep class
from machine import Pin, PWM         #importing Pin and PWM classes
from ottomotor import Servo
from ottowalkroll import Ninja
from ottoneopixel import OttoUltrasonic

led = Pin(2, Pin.OUT)                 # Built in LED
ultrasonic = OttoUltrasonic(18, 19)

ultrasonic.ultrasonicRGB2(0, 0, 255)

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

delay = 0.2
ninja = Ninja(27, 15, 14, 13)         # Connector 8 (Left leg), 9(Right leg), 10(Left foot), 11(Right foot)

while True:
    ultrasonic.ultrasonicRGB2(0, 255, 0)
    ninja.walkset()
    sleep(0.5)
    ninja.walk(1,3) #forward, fast
    ninja.walk(-1,3) #backward, fast
    sleep(0.5)
    ninja.walkset()
    ultrasonic.ultrasonicRGB2(255, 0, 0)
    ninja.rollset()
    sleep(0.5)
    ninja.roll(-1, 3)
    sleep(0.5)
    ninja.roll(1, 3)
    sleep(1)
    ninja.rollstop()
    sleep(0.4)
    ninja.rollrotate(1)  #right
    ninja.rollrotate(1)
    ninja.rollrotate(-1)  #left
    ninja.rollrotate(-1)
    sleep(0.4)
    ninja.rollset()
    sleep(0.4)
    ninja.roll(1, 1)
    ninja.roll(1, 2)
    ninja.roll(1, 3)
    sleep(0.6)
    ninja.rollstop()
    sleep(0.2)
    ultrasonic.ultrasonicRGB2(255, 0, 255)
    ninja.walkset()
    sleep(0.4)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(delay)
    servo_rightleg.write(107)
    servo_leftleg.write(125)
    sleep(delay)
    servo_rightfoot.write(55)
    sleep(delay)
    servo_rightfoot.write(90)
    sleep(delay)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(delay)
    servo_rightleg.write(46)
    servo_leftleg.write(54)
    sleep(delay)
    servo_leftfoot.write(125)
    sleep(delay)
    servo_leftfoot.write(90)
    sleep(delay)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(delay)
    servo_rightleg.write(140) #107
    servo_leftleg.write(120) #125
    sleep(delay)
    servo_rightleg.write(120)
    servo_leftleg.write(100) 
    sleep(delay)
    servo_rightleg.write(90) 
    servo_leftleg.write(90) 
    sleep(delay)
    servo_rightleg.write(120)
    servo_leftleg.write(140)
    sleep(delay)
    servo_rightleg.write(100) 
    servo_leftleg.write(120) 
    sleep(delay)
    servo_rightleg.write(90) 
    servo_leftleg.write(90) 
    sleep(delay)
    
    #fastest walk
    ultrasonic.ultrasonicRGB2(255, 255, 0)
    for count in range(5):
        servo_rightleg.write(90)
        servo_leftleg.write(90)
        sleep(0.1)
        
        servo_rightleg.write(150) #107
        servo_leftleg.write(120) #125
        sleep(0.1)
        servo_leftfoot.write(180) #125
        sleep(0.5)
        servo_leftfoot.write(90)
        sleep(0.1)
        servo_rightleg.write(90)
        servo_leftleg.write(90)
        sleep(0.1)
        servo_rightleg.write(60) #46
        servo_leftleg.write(30) #54
        sleep(0.1)
        servo_rightfoot.write(0) #55
        sleep(0.5)
        servo_rightfoot.write(90)
        sleep(delay)

