import machine, time, utime                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from ottomotor import OttoMotor
from ottomotor import Servo

offset = 0
motor = OttoMotor(13, 14)  # Connectors 10 & 11
servo_grip=Servo()
servo_grip.attach(27) # Connector 8
servo_bumper=Servo()
servo_bumper.attach(15) # Connector 9

def grip_close():
    for i in range(40, 80):
        servo_grip.write(i)
        sleep(0.01)
        
def grip_open():
    for i in range(80, 40, -1):
        servo_grip.write(i)
        sleep(0.01)
        
def bump_up():
    for i in range(70, 40, -1):
        servo_bumper.write(i)
        sleep(0.02)

def bump_down():
    for i in range(40, 70, 1):
        servo_bumper.write(i)
        sleep(0.02)

motor.Stop(1)
bump_down()
sleep(1)
grip_open()    
sleep(1)
grip_close()
sleep(1)
bump_up()
    
sleep(1)

motor.leftServo.freq(50)
motor.rightServo.freq(50)
motor.leftServo.duty(109- offset)
motor.rightServo.duty(43+ offset)
sleep(1)
motor.rightServo.duty(0)
motor.leftServo.duty(0)
