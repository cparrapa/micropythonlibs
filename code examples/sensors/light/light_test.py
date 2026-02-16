from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

led = Pin(2, Pin.OUT)             # Built in LED
light=ADC(Pin(33))                # Connector 7 analog
light.atten(ADC.ATTN_0DB)

def map(value, in_min, in_max, out_min, out_max):
   map = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   return map

while True:
    print("Analog:", light.read(),"Light:",int(map(light.read(), 4095, 0, 0, 100)), "%")
    sleep(0.1)
 