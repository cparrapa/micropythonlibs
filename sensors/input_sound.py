from machine import Pin, ADC          #importing Pin and ADC classes
from time import sleep                   #importing sleep class
import machine

led = machine.Pin(2, machine.Pin.OUT)
potentiometer=ADC(Pin(26))             #Connector 4

while True:
 potentiometer_value=potentiometer.read()           #reading analog pin
 print(potentiometer_value)
 if (potentiometer_value) > (600):
    led.off()
    sleep(0.2)
 else:
    led.on()
