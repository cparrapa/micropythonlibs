from machine import Pin, ADC          #importing Pin and ADC classes
from time import sleep                #importing sleep class

led = Pin(2, Pin.OUT)    # Built in LED
pot=ADC(Pin(33))         # creating potentiometer object Connector 7

while True:
 potentiometer_value=pot.read()           #reading analog pin
 print(potentiometer_value)
 td= 0.1 + potentiometer_value/4095
 led.on()
 sleep(td)
 led.off()
 sleep(td)

