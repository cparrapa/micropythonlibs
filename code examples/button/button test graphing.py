from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

button = Pin(26, Pin.IN) # Connector 4

while True:
    print(button.value())
    sleep(.01)