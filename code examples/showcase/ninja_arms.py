import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottomotor import OttoMotor
from ottomotor import Servo
from ottowalkroll import Arms

# arm servo motors
servo_leftarm=Servo()
servo_leftarm.attach(32)	# Connector 6
servo_rightarm=Servo()
servo_rightarm.attach(33)	# Connector 7

arms = Arms(32, 33)
 
delay = 0.3
while True:
    arms.move("both","center")
#    servo_leftarm.write(180)
#     servo_rightarm.write(90)
#     servo_leftarm.write(90)
#     time.sleep(delay)
#     servo_rightarm.write(150)
#     time.sleep(delay)
#     servo_leftarm.write(150)
#     time.sleep(delay)
#     servo_leftfoot.write(125)
#     time.sleep(delay)
#     servo_rightarm.write(90)
#     time.sleep(delay)
#     servo_leftarm.write(90)
#     time.sleep(delay)
#     servo_leftfoot.write(90)
#     time.sleep(delay)
#     servo_rightleg.write(90)
#     servo_leftleg.write(90)
#     time.sleep(delay)
#     servo_rightarm.write(50)
#     time.sleep(delay)
#     servo_leftarm.write(50)
#     time.sleep(delay)
#     servo_rightleg.write(60)
#     servo_leftleg.write(30)
#     time.sleep(delay)
#     servo_rightfoot.write(55)
#     time.sleep(delay)
#     servo_rightfoot.write(90)
#     time.sleep(delay)
#     servo_rightarm.write(20)
#     time.sleep(delay)
#     servo_leftarm.write(20)
#     time.sleep(delay)

