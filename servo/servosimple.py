# Load the machine module for GPIO and PWM
# Control servo motor with MicroPython
# Author: George Bantique, TechToTinker
# Date: September 15, 2020

import machine
from machine import Pin, ADC, PWM 
# Load the time module for the delays
import time

adc_32 = ADC(26)
adc_32.width(ADC.WIDTH_10BIT)

# Create a regular p23 GPIO object
p23 = machine.Pin(32, machine.Pin.OUT)

# Create another object named pwm by
# attaching the pwm driver to the pin
pwm = machine.PWM(p23)

# Set the pulse every 20ms
pwm.freq(50)

# Set initial duty to 0
# to turn off the pulse
pwm.duty(0)

# Creates a function for mapping the 0 to 180 degrees
# to 20 to 120 pwm duty values
def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

# Creates another function for turning 
# the servo according to input angle
def servo(pin, angle):
    pin.duty(map(angle, 0, 180, 20, 120))


# To rotate the servo motor to 0 degrees
servo(pwm, 0)

# To rotate the servo motor to 90 degrees
servo(pwm, 90)

# To rotate the servo motor to 180 degrees
servo(pwm, 180)

# To rotate the servo from 0 to 180 degrees
# by 10 degrees increment
for i in range(0, 181, 10):
    servo(pwm, i)
    time.sleep(0.5)
    
# To rotate the servo from 180 to 0 degrees
# by 10 degrees decrement
for i in range(180, -1, -10):
    servo(pwm, i)
    time.sleep(0.5)
    
while True:
    print(adc_32.read())
    

