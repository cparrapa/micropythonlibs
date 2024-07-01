from machine import Pin, ADC          #importing Pin and ADC classes
from time import sleep                #importing sleep class

led = Pin(2, Pin.OUT)  # Built in LED
pot=ADC(Pin(33))       # Connector 7

while True:   
 print(pot.read())  #reading analog pin
 sleep(0.05)
 if (pot.read()) > (2000):
    led.off()
    sleep(0.2)
 else:
    led.on()
