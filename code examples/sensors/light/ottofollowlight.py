import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor
offset = 0

analogL=ADC(Pin(27))                  # Connector 6
analogR=ADC(Pin(15))                  # Connector 7
ultrasonic = OttoUltrasonic(18, 19)
motor = OttoMotor(13, 14)             # Connectors 10 & 11

while True:
    print(str("l") + str(analogL.read()))
    print(str("R") + str(analogR.read()))
    if (analogL.read()) < (2000):
        ultrasonic.ultrasonicRGB1("fe0000", "00ff00")
        motor.leftServo.duty(60- offset)
        motor.rightServo.duty(60+ offset)
    elif (analogR.read()) < (2000):
        ultrasonic.ultrasonicRGB1("00ff00", "fe0000")
        motor.leftServo.duty(95- offset)
        motor.rightServo.duty(95+ offset)
    else:
        ultrasonic.ultrasonicRGB1("00ff00", "00ff00")
        motor.leftServo.duty(95- offset)
        motor.rightServo.duty(60+ offset)
