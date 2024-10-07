import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
digital = Pin(15, Pin.IN)

while True:
    print(digital.value())
    time.sleep(.01)