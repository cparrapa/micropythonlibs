import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
from ottoninja import Ninja

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ninja = Ninja(27, 15, 14, 13)         # Connector 8 (Left leg), 9(Right leg), 10(Left foot), 11(Right foot)

while True:
    ninja.Walkset()
    time.sleep(1)
    ninja.Rollset()
    time.sleep(1)
    ninja.Roll(-1, 2)
    time.sleep(2)
    ninja.Roll(1, 2)
    time.sleep(2)
    ninja.Rollstop()
    time.sleep(0.5)
    ninja.Rollrotate(1)
    ninja.Rollrotate(-1)
    time.sleep(1)

