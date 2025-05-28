from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
import machine, time                       #importing machine and time libraries
from time import sleep
from ottomotor import OttoMotor
from ottomotor import Servo

offset = 0

motor = OttoMotor(13, 14)             # Connectors 10 & 11
motor.leftServo.freq(50)
motor.rightServo.freq(50)
motor.leftServo.duty(95- offset)
motor.rightServo.duty(60+ offset)
sleep(1)
motor.rightServo.duty(0)
motor.leftServo.duty(0)
motor.leftServo.duty(109- offset)
motor.rightServo.duty(43+ offset)
sleep((1))
motor.leftServo.duty(127- offset)
motor.rightServo.duty(29+ offset)
sleep((1))
motor.rightServo.duty(45+ offset)
motor.leftServo.duty(45- offset)
sleep(0.4)
motor.rightServo.duty(0)
motor.leftServo.duty(0)
motor.Stop(1)
sleep((1))
motor.Moveleft(1, 1, 2)
motor.leftServo.duty(109- offset)
sleep((1))
motor.Stop(2)
motor.Moveright(1, 1, 2)
motor.rightServo.duty(43+ offset)
sleep((1))
motor.Stop(3)

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
servo_leftfoot.write(90)
servo_rightfoot.write(90)

"""
from ottoangle import Servo
motor=Servo(pin=15)
motor.move(0) 
time.sleep(1)
motor.move(90) 
time.sleep(1)
motor.move(180) 
time.sleep(1)
motor.move(90) 
time.sleep(1)
"""