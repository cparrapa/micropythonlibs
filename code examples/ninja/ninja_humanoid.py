import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
from ottomotor import Servo
from ottoninja import Ninja
from ottoneopixel import OttoUltrasonic
 
led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ultrasonic = OttoUltrasonic(18, 19)

ultrasonic.ultrasonicRGB2(0, 0, 255)

# arm servo motors
servo_leftarm=Servo()
servo_leftarm.attach(32)	# Connector 6
servo_rightarm=Servo()
servo_rightarm.attach(33)	# Connector 7
 
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

ninja = Ninja(27, 15, 14, 13)         # Connector 8 (Left leg), 9(Right leg), 10(Left foot), 11(Right foot)
 
delay = 0.5
while True:
    ultrasonic.ultrasonicRGB2(0, 255, 0)
    ninja.Walkset()
    sleep(0.3)
    servo_rightarm.write(90)
    servo_leftarm.write(40)
    sleep(delay)
    sleep(0.5)
    ninja.Walk(1, 3)
    sleep(0.2)
    servo_rightarm.write(50)
    sleep(0.3)
    servo_leftarm.write(60)
    sleep(0.3)
    ninja.Walk(-1,3) #backward, fast
    sleep(0.5)
    servo_rightarm.write(20)
    sleep(0.3)
    ninja.Walkset()
    servo_leftarm.write(90)
    sleep(0.3)
    ultrasonic.ultrasonicRGB2(255, 0, 0)
    ninja.Rollset()
    sleep(0.5)
    ninja.Roll(-1, 3)
    servo_rightarm.write(150)
    sleep(0.3)
    servo_leftarm.write(150)
    sleep(delay)
    sleep(0.5)
    ninja.Roll(1, 3)
    sleep(1)
    ninja.Rollstop()
    sleep(0.4)
    ninja.Rollrotate(1)
    ninja.Rollrotate(1)
    ninja.Rollrotate(-1)
    ninja.Rollrotate(-1)
    sleep(0.4)
    servo_rightarm.write(120)
    servo_leftarm.write(120)
    sleep(0.3)
    ninja.Rollset()
    sleep(0.4)
    ninja.Roll(1, 1)
    ninja.Roll(1, 2)
    ninja.Roll(1, 3)
    sleep(0.6)
    ninja.Rollstop()
    sleep(0.2)
    ultrasonic.ultrasonicRGB2(255, 0, 255)
    ninja.Walkset()
    sleep(0.3)
    servo_rightarm.write(90)
    servo_leftarm.write(90)
    sleep(0.4)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(delay)
    servo_rightleg.write(107)
    servo_leftleg.write(125)
    sleep(0.3)
    servo_rightarm.write(50)
    servo_leftarm.write(50)
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
    servo_leftfoot.write(90)
    time.sleep(delay)
    servo_leftarm.write(20)
    servo_rightarm.write(20)
    sleep(delay)

    

    
