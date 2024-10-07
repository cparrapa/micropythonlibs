# -*- coding: utf-8 -*-
from microbit import *
import radio
import math

motor_pwm = bytearray([8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
servo_pos = bytearray([0, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC])

'''
motor_pwm.ch1 = M1.A
motor_pwm.ch2 = M1.B
motor_pwm.ch3 = M2.A
motor_pwm.ch4 = M2.B
'''


def motion(leftSpeed, rightSpeed):
    if leftSpeed > 2000:
        leftSpeed = 2000
    if leftSpeed < -2000:
        leftSpeed = -2000
    if leftSpeed == 0:
        motor_pwm[1] = 0
        motor_pwm[2] = 0
        motor_pwm[3] = 0
        motor_pwm[4] = 0
    if leftSpeed > 0:
        motor_pwm[1] = int(leftSpeed / 256)
        motor_pwm[2] = int(leftSpeed % 256)
        motor_pwm[3] = 0
        motor_pwm[4] = 0
    if leftSpeed < 0:
        leftSpeed = -leftSpeed
        motor_pwm[1] = 0
        motor_pwm[2] = 0
        motor_pwm[3] = int(leftSpeed / 256)
        motor_pwm[4] = int(leftSpeed % 256)
    if rightSpeed > 2000:
        rightSpeed = 2000
    if rightSpeed < -2000:
        rightSpeed = -2000
    if rightSpeed == 0:
        motor_pwm[5] = 0
        motor_pwm[6] = 0
        motor_pwm[7] = 0
        motor_pwm[8] = 0
    if rightSpeed > 0:
        motor_pwm[5] = 0
        motor_pwm[6] = 0
        motor_pwm[7] = int(rightSpeed / 256)
        motor_pwm[8] = int(rightSpeed % 256)
    if rightSpeed < 0:
        rightSpeed = -rightSpeed
        motor_pwm[5] = int(rightSpeed / 256)
        motor_pwm[6] = int(rightSpeed % 256)
        motor_pwm[7] = 0
        motor_pwm[8] = 0
    i2c.write(0x2A, motor_pwm)


def setServo(servo, angle):
    "set the servo angel"
    a = (1.5 + angle/90) * 1000
    servo_pos[servo*2 + 1] = int(a / 256)
    servo_pos[servo*2 + 2] = int(a % 256)


def updatePosition():
    servo_pos[0] = 0
    i2c.write(0x2A, servo_pos)


def getDistance():
    i2c.write(0x0b, bytearray([1]))
    temp = i2c.read(0x0B, 2)
    dis = (temp[0]+temp[1]*256)/10
    return dis


# application
display.off()
motion(0, 0)

radio.on()
radio.config(length=8, queue=20, channel=79, power=7,
             address=0x44773311, group=0x1B, data_rate=radio.RATE_250KBIT)
x = 0
y = 0
z = 0
a = 0
left = 0
right = 0
while True:
    # print("running")
    msg = bytes(8)
    msg = radio.receive_bytes()
    if msg is not None:
        x = msg[0]*256 + msg[1]
        x = x - 10000
        y = msg[2]*256 + msg[3]
        y = y - 10000
        z = msg[4]*256 + msg[5]
        z = z - 10000
        a = msg[6]*256 + msg[7]
        if a == 0:
            left = int((y + x) )
            right = int((y - x))
            #print('left = ', left)
            #print('right = ', right)
            motion(-right, -left)
        if (a & 0x03) != 0:
            motion(0, 0)
            y = min(max(-1000, y), 1000)
            x = min(max(-1000, x), 1000)
            sv = math.asin(y/1000)*180/math.pi
            sh = math.asin(x/1000)*180/math.pi
            sv = min(max(-45, sv), 45)
            sh = min(max(-45, sh), 45)
            if (a & 0x01) != 0:
                setServo(0, -sv)
                setServo(2, -sh)
            if (a & 0x02) != 0:
                setServo(1, sv)
                setServo(3, sh)
            updatePosition()
