from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from time import sleep                   #importing sleep class

led = Pin(2, Pin.OUT)
pot=ADC(Pin(26))              #creating potentiometer object

while True:
 potentiometer_value=pot.read()           #reading analog pin
 print(potentiometer_value)
 td= 0.1 + potentiometer_value/4095
 led.on()
 sleep(td)
 led.off()
 sleep(td)

