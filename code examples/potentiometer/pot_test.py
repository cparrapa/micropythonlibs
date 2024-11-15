from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

led = Pin(2, Pin.OUT)                 # Built in LED
adc_33 = ADC(33)
adc_33.width(ADC.WIDTH_12BIT)
adc_33.atten(ADC.ATTN_11DB)
def map(value, in_min, in_max, out_min, out_max):
   map = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   return map

while True:
    print(int(map(adc_33.read(), 4095, 0, 0, 270)))
