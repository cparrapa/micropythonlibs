from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer

buzzer = OttoBuzzer(25)               # Built in Buzzer
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5

import math
adc_26 = ADC(32)                      # Connector 6
adc_26.width(ADC.WIDTH_10BIT)         # resolution range 0 to 1023

def map(value, in_min, in_max, out_min, out_max):
   map = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   return map

ring.setBrightness(1)
buzzer.playEmoji("S_connection")
while True:
    buzzer.playNote(round(map(adc_26.read(), 0, 1024, 261, 523)), 100)
    ring.setRGBLed(0, 255, 100, round(map(adc_26.read(), 1024, 0, 0, 12)))
    ring.clearRGB()
