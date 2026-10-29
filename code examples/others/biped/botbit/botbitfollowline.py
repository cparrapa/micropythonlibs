 # -*- coding: utf-8 -*-
from microbit import *
import music
import math
import radio

motor_pwm = bytearray([8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
servo_pos = bytearray([0, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC])

# motion functions
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


# servo functions
def setServo(servo, angle):
    "set the servo angel"
    a = (1.5 + angle/90) * 1000
    servo_pos[servo*2 + 1] = int(a / 256)
    servo_pos[servo*2 + 2] = int(a % 256)


def updatePosition():
    servo_pos[0] = 0
    try:
        i2c.write(0x2A, servo_pos)
    except:
        print("i2c error")

def BatteryLevel():
    return i2c.read(0x2A, 1)[0]
	
def distance():
    i2c.write(0x0b, bytearray([1]))
    sleep(2)
    temp=i2c.read(0x0b,2)
    distanceCM=(temp[0]+temp[1]*256)/10
    return distanceCM   
	
def setRGB(cmd,r,g,b): #cmd: 2 leftLed 3: rightLed r,g,b range:0-255
    i2c.write(0x0b,bytearray([cmd,r,g,b]))
    sleep(1)
    
def setHSV(cmd,h,s,v): #cmd: 4 leftLed 5: rightLed h range:0-360 s v range:0-1 
    _h1 = h%256
    _h2 = h//256
    _s = int(s*100)
    _v = int(v*100)
    i2c.write(0x0b,bytearray([cmd,_h1,_h2,_s,_v]))
    sleep(1)
		
sensor_min = [1024, 1024, 1024, 1024, 1024]
sensor_max = [0, 0, 0, 0, 0]
sensor = [0, 0, 0, 0, 0]
sensor_pin = (pin3, pin1, pin10, pin2, pin4)
# calibration
def Calibrate():
    global sensor_min, sensor_max, sensor,sensor_pin
    motion(-1000, 1000)
    t = running_time()
    while (running_time() - t) < 5000:
        for i in range(5):
            sensor[i] = sensor_pin[i].read_analog() 
            sensor_min[i] = min(sensor[i], sensor_min[i])
            sensor_max[i] = max(sensor[i], sensor_max[i])
    motion(0, 0)
    print("sensors min value:%d,%d,%d,%d,%d" % \
         (sensor_min[0], sensor_min[1], sensor_min[2], sensor_min[3], sensor_min[4]))
    print("sensors max value:%d,%d,%d,%d,%d" % \
         (sensor_max[0], sensor_max[1], sensor_max[2], sensor_max[3], sensor_max[4]))
  
def ReadLineSensor():
    global sensor_min, sensor_max, sensor,sensor_pin
    for i in range(5):
        sensor[i] = sensor_pin[i].read_analog()
        sensor[i] = round((sensor[i] - sensor_min[i]) / (sensor_max[i] - sensor_min[i]) * 1000)
    
    sum = sensor[0] + sensor[1] + sensor[2] + sensor[3] + sensor[4]
    if sum <= 0:
        return 0
    else:
        return (sensor[0] + sensor[1] * 1000 + sensor[2] * 2000 + sensor[3] * 3000 + sensor[4]*4000) / sum
        
def PIDtracking(kp,kd,trackSpeed):
    global pre_line_pos
    line_pos = ReadLineSensor() - 2000  
    correction = kp * line_pos + kd * (line_pos - pre_line_pos)
    pre_line_pos = line_pos
    print('correction:',correction)
    if correction > 0:
        motion(trackSpeed - correction, trackSpeed)
    else:
        motion(trackSpeed, trackSpeed + correction)
        
# application
t=0
display.off()
motion(0, 0)
pin3.read_digital()
pin4.read_digital()
pin10.read_digital()
pin3.set_pull(pin3.NO_PULL)
pin4.set_pull(pin4.NO_PULL)
pin10.set_pull(pin10.NO_PULL)
setServo(0,-45)
setServo(2,-45)
setServo(1,45)
setServo(3,45)
updatePosition()
Calibrate()
#kp = float(input('kp=:'))
#kd = float(input('kd=:'))
pre_line_pos = ReadLineSensor() - 2000
while True: 
    for i in range(360):
        setHSV(4,i,1.0,1.0)
        setHSV(5,i,1.0,1.0)
        PIDtracking(1.8,5,1200)
        sleep(10)
    