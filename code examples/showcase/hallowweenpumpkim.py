import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from ottoneopixel import OttoUltrasonic
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
import rtttl

ultrasonic = OttoUltrasonic(18, 19)
bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
buzzer = OttoBuzzer(25)               # Built in Buzzer
motor = OttoMotor(13, 14)             # Connectors 10 & 11

ultrasonic.ultrasonicRGB1("33ff33", "33ff33")
ring.rainbow_cycle(n, 5)

hallow = 'Halloween:d=4,o=5,b=180:8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#'
rtttl.play(hallow)
ring.fillAllRGBRing("ff6600")
ultrasonic.ultrasonicRGB1("ff6600", "ff6600")
song = 'Adams:d=4,o=5,b=160:8c,8d,8e,8f,1p,8d,8e,8f#,8g,1p,8d,8e,8f#,8g,p,8d,8e,8f#,8g,p,8c,8d,8e,8f'
rtttl.play(song)
while True:
    ring.fillAllRing(255, 130, 0)
    ultrasonic.ultrasonicRGB2(255, 100, 0)
    ring.bounce(n, int(255 * bright), int(153 * bright), int(0 * bright), 150)
    ring.fillAllRing(0, 255, 0)
    ultrasonic.ultrasonicRGB2(0, 255, 0)
    ring.cycle(n, int(51 * bright), int(204 * bright), int(0 * bright), 150)
