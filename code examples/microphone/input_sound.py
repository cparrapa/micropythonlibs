from machine import Pin, ADC          #importing Pin and ADC classes
from time import sleep                #importing sleep class

led = Pin(2, Pin.OUT)  # Built in LED
mic=ADC(Pin(32))       # Connector 6

while True:   
 print(mic.read())  #reading analog pin
 sleep(0.05)
 if (mic.read()) > (2000):
    led.off()
    sleep(0.2)
 else:
    led.on()
