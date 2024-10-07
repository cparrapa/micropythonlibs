import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottomotor import Servo

led = Pin(2, Pin.OUT)                 # Built in LED
digital_pin_32 = Pin(32, Pin.IN, Pin.PULL_UP)
servo=Servo()
servo.attach(33)
previous_value = 1
previous_time = 0

servo.write(180)

print("Seconds per revolution:")

while True:
    
    current_value = digital_pin_32.value()
    
    if previous_value == 1 and current_value == 0:
        current_time = time.ticks_us()
        time_diff = time.ticks_diff(current_time, previous_time)
        print(time_diff/100000)
        previous_time = current_time
        
    previous_value = current_value
    time.sleep(0.01)