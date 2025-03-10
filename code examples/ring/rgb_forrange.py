import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel

bright = 0.5                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5


while True:
    for i in range(1, 13):
        ring.setRGBring(i, "00ffff")
        sleep(0.1)

    ring.clearRGB()
