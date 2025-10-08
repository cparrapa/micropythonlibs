import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

tilt = Pin(13, Pin.IN)

currenttime = 0
lasttime = 0

response = 10

def tilt_handler(pin):
    
    global currenttime
    global response
    
    currenttime = time.ticks_ms()
    if time.ticks_diff(currenttime, lasttime) > response:
        print("State: ", tilt.value())
        lasttime = currenttime
#Interrupt sequence (change registration)
tilt.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=tilt_handler)

while True:
    time.sleep(.1)
