import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from ottobuzzer import Player
dfplayer = Player(16, 17)

led = Pin(2, Pin.OUT)                 # Built in LED
adc_32 = ADC(32)
adc_32.width(ADC.WIDTH_12BIT)
adc_32.atten(ADC.ATTN_11DB)
vol=10

def map(value, in_min, in_max, out_min, out_max):
   map = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   return map

while True:
    vol= round(map(adc_32.read(), 0, 4095, 0, 50))
    print(vol)
    dfplayer.volume(vol)
    dfplayer.play(1)
    sleep(1)
