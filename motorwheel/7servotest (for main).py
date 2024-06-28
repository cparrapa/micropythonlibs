import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
from ottomotor import Servo

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ultrasonic = NeoPixel(Pin(18), 6)     # Connector 1
io = 19                               # echo input and trigger out signal
bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
digitalL = Pin(32, Pin.IN)            # Connector 8
digitalR = Pin(15, Pin.IN)            # Connector 9
motor = OttoMotor(13, 14)             # Connectors 10 & 11
offsetL = 0                           # Calibration for left servo motor
offsetR = 0                           # Calibration for right servo motor
digital_pin_32 = Pin(32, Pin.IN, Pin.PULL_UP)

servo_13=Servo()
servo_13.attach(13)

previous_value = 1
previous_time = 0

servo_13.write(180)

print("Seconds per revolution:")

while True:
    
    current_value = digital_pin_32.value()
    
    if previous_value == 1 and current_value == 0:
        current_time = time.ticks_us()
        time_diff = time.ticks_diff(current_time, previous_time)
        print(time_diff/100000)
        previous_time = current_time
        
    previous_value = current_value
    
    
    time.sleep((0.01))


