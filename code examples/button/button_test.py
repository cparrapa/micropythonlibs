import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer

led = Pin(2, Pin.OUT)       # Built in LED
buzzer = OttoBuzzer(25)     # Built in Buzzer
button = Pin(4, Pin.IN)    # Connector 4

while True:
    print(button.value())
    sleep(.01)
    if (button.value()) == (1):
        led.on()
        buzzer.playEmoji("S_happy")
    else:
        led.off()
