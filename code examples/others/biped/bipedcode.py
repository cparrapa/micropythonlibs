"""
  Program Otto DIY robot for basic movements with CircuitPython
  https://youtu.be/yhI3i0DSZoo
  
  Board:
  - Maker Nano RP2040
    https://my.cytron.io/maker-nano-rp2040-simplifying-projects-with-raspberry-pi-rp2040
  - IO Expansion Shield for Arduino Nano
    https://my.cytron.io/p-io-expansion-shield-for-arduino-nano
  - SG90 Micro Servo
    https://my.cytron.io/p-sg90-micro-servo
  - 5VDC HC-SR04 Ultrasonic Sensor
    https://my.cytron.io/p-5v-hc-sr04-ultrasonic-sensor
  - 3D printing products
    https://my.cytron.io/c-3d-modeling
  
  Connections:
  - Servo left leg = GP2
  - Servo right leg = GP3
  - Servo left foot = GP4
  - Servo right foot = GP5
  - Ultrasonic trig = GP7
  - Ultrasonic echo = GP6
  
  Libraries required from bundle (https://circuitpython.org/libraries):
  - adafruit_motor
  - adafruit_hcsr04.mpy
  - simpleio.mpy
  
  Otto DIY
  - https://www.ottodiy.com/
  
  Last Modified: 28 Mar 2022
"""

import time
import board
import digitalio
import simpleio
import pwmio
from adafruit_motor import servo
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP7, echo_pin=board.GP6)

SERVO_LL = board.GP2 # Servo for left leg
SERVO_LR = board.GP3 # Servo for right leg
SERVO_FL = board.GP4 # Servo for left foot
SERVO_FR = board.GP5 # Servo for right foot

pwm_ll = pwmio.PWMOut(SERVO_LL, duty_cycle=2 ** 15, frequency=50)
pwm_lr = pwmio.PWMOut(SERVO_LR, duty_cycle=2 ** 15, frequency=50)
pwm_fl = pwmio.PWMOut(SERVO_FL, duty_cycle=2 ** 15, frequency=50)
pwm_fr = pwmio.PWMOut(SERVO_FR, duty_cycle=2 ** 15, frequency=50)

servo_ll = servo.Servo(pwm_ll)
servo_lr = servo.Servo(pwm_lr)
servo_fl = servo.Servo(pwm_fl)
servo_fr = servo.Servo(pwm_fr)

offset_ll = 8
offset_lr = 0
offset_fl = 10
offset_fr = 0

defaultpos_ll = 90 - offset_ll
defaultpos_lr = 90 - offset_lr
defaultpos_fl = 90 - offset_fl
defaultpos_fr = 90 - offset_fr

def stand():
    servo_ll.angle = defaultpos_ll
    servo_lr.angle = defaultpos_lr
    servo_fl.angle = defaultpos_fl
    servo_fr.angle = defaultpos_fr
    time.sleep(1)

def dance_1():
    for count in range(5):
        servo_fl.angle = defaultpos_fl - (count*10)
        time.sleep(0.02)
    for count in range(4, -1, -1):
        servo_fl.angle = defaultpos_fl - (count*10)
        time.sleep(0.02)

def dance_2():
    for count in range(5):
        servo_fr.angle = defaultpos_fr + (count*10)
        time.sleep(0.02)
    for count in range(4, -1, -1):
        servo_fr.angle = defaultpos_fr + (count*10)
        time.sleep(0.02)

def dance_3():
    for count in range(6):
        servo_fl.angle = defaultpos_fl + (count*10)
        time.sleep(0.02)
    for count in range(6):
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)
    time.sleep(0.2)
    for count in range(5, -1, -1):
        servo_fl.angle = defaultpos_fl + (count*10)
        time.sleep(0.02)
    for count in range(5, -1, -1):
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)

def dance_4():
    for count in range(6):
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)
    for count in range(6):
        servo_fl.angle = defaultpos_fl + (count*10)
        time.sleep(0.02)
    time.sleep(0.2)
    for count in range(5, -1, -1):
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)
    for count in range(5, -1, -1):
        servo_fl.angle = defaultpos_fl + (count*10)
        time.sleep(0.02)

def dance_5():
    for count in range(6):
        servo_fr.angle = defaultpos_fr - (count*10)
        servo_fl.angle = defaultpos_fl + (count*10)
        time.sleep(0.02)
    time.sleep(0.5)
    for count in range(5, -1, -1):
        servo_fr.angle = defaultpos_fr - (count*10)
        servo_fl.angle = defaultpos_fl + (count*10)
        time.sleep(0.02)
    time.sleep(0.3)

def dance_6():
    for count in range(3):
        servo_ll.angle = defaultpos_ll - (count*10)
        servo_lr.angle = defaultpos_lr - (count*10)
        time.sleep(0.02)
    time.sleep(0.3)
    for count in range(3):
        for count in range(5):
            servo_ll.angle = defaultpos_ll + (count*10) - 20
            servo_lr.angle = defaultpos_lr + (count*10) - 20
            time.sleep(0.02)
        time.sleep(0.3)
        for count in range(5):
            servo_ll.angle = defaultpos_ll - (count*10) + 20
            servo_lr.angle = defaultpos_lr - (count*10) + 20
            time.sleep(0.02)
        time.sleep(0.3)

def walk_forward():
    for count in range(4):
        servo_fl.angle = defaultpos_fl + (count*10)
        servo_fr.angle = defaultpos_fr + (count*2)
        time.sleep(0.02)
    for count in range(3):
        servo_ll.angle = defaultpos_ll - (count*10)
        servo_lr.angle = defaultpos_lr - (count*10)
        time.sleep(0.02)
    for count in range(3):
        for count in range(3, -1, -1):
            servo_fl.angle = defaultpos_fl + (count*10)
            servo_fr.angle = defaultpos_fr + (count*2)
            time.sleep(0.02)
        for count in range(4):
            servo_fl.angle = defaultpos_fl - (count*2)
            servo_fr.angle = defaultpos_fr - (count*10)
            time.sleep(0.02)
        for count in range(5):
            servo_ll.angle = defaultpos_ll + (count*10) - 20
            servo_lr.angle = defaultpos_lr + (count*10) - 20
            time.sleep(0.02)
        for count in range(3, -1, -1):
            servo_fl.angle = defaultpos_fl - (count*2)
            servo_fr.angle = defaultpos_fr - (count*10)
            time.sleep(0.02)
        for count in range(4):
            servo_fl.angle = defaultpos_fl + (count*10)
            servo_fr.angle = defaultpos_fr + (count*2)
            time.sleep(0.02)
        for count in range(5):
            servo_ll.angle = defaultpos_ll - (count*10) + 20
            servo_lr.angle = defaultpos_lr - (count*10) + 20
            time.sleep(0.02)
    for count in range(3, -1, -1):
        servo_fl.angle = defaultpos_fl + (count*10)
        servo_fr.angle = defaultpos_fr + (count*2)
        time.sleep(0.02)
    for count in range(4):
        servo_fl.angle = defaultpos_fl - (count*2)
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)
    for count in range(3):
        servo_ll.angle = defaultpos_ll + (count*10) - 20
        servo_lr.angle = defaultpos_lr + (count*10) - 20
        time.sleep(0.02)
    for count in range(3, -1, -1):
        servo_fl.angle = defaultpos_fl - (count*2)
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)

def walk_backward():
    for count in range(4):
        servo_fl.angle = defaultpos_fl - (count*2)
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)
    for count in range(3):
        servo_ll.angle = defaultpos_ll - (count*10)
        servo_lr.angle = defaultpos_lr - (count*10)
        time.sleep(0.02)
    for count in range(3):
        for count in range(3, -1, -1):
            servo_fl.angle = defaultpos_fl - (count*2)
            servo_fr.angle = defaultpos_fr - (count*10)
            time.sleep(0.02)
        for count in range(4):
            servo_fl.angle = defaultpos_fl + (count*10)
            servo_fr.angle = defaultpos_fr + (count*2)
            time.sleep(0.02)
        for count in range(5):
            servo_ll.angle = defaultpos_ll + (count*10) - 20
            servo_lr.angle = defaultpos_lr + (count*10) - 20
            time.sleep(0.02)
        for count in range(3, -1, -1):
            servo_fl.angle = defaultpos_fl + (count*10)
            servo_fr.angle = defaultpos_fr + (count*2)
            time.sleep(0.02)
        for count in range(4):
            servo_fl.angle = defaultpos_fl - (count*2)
            servo_fr.angle = defaultpos_fr - (count*10)
            time.sleep(0.02)
        for count in range(5):
            servo_ll.angle = defaultpos_ll - (count*10) + 20
            servo_lr.angle = defaultpos_lr - (count*10) + 20
            time.sleep(0.02)
    for count in range(3, -1, -1):
        servo_fl.angle = defaultpos_fl - (count*2)
        servo_fr.angle = defaultpos_fr - (count*10)
        time.sleep(0.02)
    for count in range(4):
        servo_fl.angle = defaultpos_fl + (count*10)
        servo_fr.angle = defaultpos_fr + (count*2)
        time.sleep(0.02)
    for count in range(3):
        servo_ll.angle = defaultpos_ll + (count*10) - 20
        servo_lr.angle = defaultpos_lr + (count*10) - 20
        time.sleep(0.02)
    for count in range(3, -1, -1):
        servo_fl.angle = defaultpos_fl + (count*10)
        servo_fr.angle = defaultpos_fr + (count*2)
        time.sleep(0.02)

time.sleep(1)

stand()
object_distance = 0
mode = 0
run = False

while True:
    try:
        object_distance = sonar.distance
        print("Object distance: {}cm".format(object_distance))

        if object_distance < 15:
            mode += 1
            run = True
            time.sleep(2)

    except RuntimeError:
        print("Retrying!")
    
    time.sleep(0.1)
    
    if mode == 1 and run == True:
        run = False
        for count in range(3):
            dance_1()
            time.sleep(0.2)
        stand()
    
    elif mode == 2 and run == True:
        run = False
        for count in range(3):
            dance_2()
            time.sleep(0.2)
        stand()
    
    elif mode == 3 and run == True:
        run = False
        dance_3()
        time.sleep(0.5)
        dance_4()
        time.sleep(0.5)
        dance_5()
        stand()
    
    elif mode == 4 and run == True:
        run = False
        dance_6()
        stand()
    
    elif mode == 5 and run == True:
        run = False
        walk_forward()
        stand()
    
    elif mode == 6 and run == True:
        mode = 0
        run = False
        walk_backward()
        stand()
    