import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
offset = 0

buzzer = OttoBuzzer(25)               # Built in Buzzer
motor = OttoMotor(13, 14)             # Connectors 10 & 11

buzzer.playEmoji("S_happy")
motor.leftServo.freq(50)
motor.rightServo.freq(50)
motor.leftServo.duty(127- offset)
motor.rightServo.duty(29+ offset)
sleep(1)
motor.rightServo.duty(0)
motor.leftServo.duty(0)
