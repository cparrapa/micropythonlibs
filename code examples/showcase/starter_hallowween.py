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
ring.rainbow_cycle(n, 1)
toccata ='Toccata:d=4,o=5,b=160:16a4,16g4,1a4,16g4,16f4,16d4,16e4,2c#4,16p,d.4,2p,16a4,16g4,1a4,8e.4,8f.4,8c#.4,2d4'
rtttl.play(toccata)
castle='Castle on a Cloud:d=4,o=5,b=90:8a,16b,16c6,8b,8a,8a,8g#,a,p,8a,16b,16c6,8b,8a,8g,8f,e,p,8d,16e,16f,8e,8a,8b,8c6,a,p,8d,16e,16f,8e,8d,8c,8b,a'
rtttl.play(castle)
ghost ='Ghostbusters:d=16,o=5,b=112:g,g,8b,8g,8a,4f.,g,g,g,g,8f,4g.,g,g,8b,8g,8a,4f.,g,g,g,g,8f,8a,8g,4d.,g,g,8b,8g,8a,4f.,g,g,g,g,8f,4g'
rtttl.play(ghost)
hallow = 'Halloween:d=4,o=5,b=180:8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#'
rtttl.play(hallow)
ring.fillAllRGBRing("ff6600")
ultrasonic.ultrasonicRGB1("ff6600", "ff6600")
zelda= 'Zelda1:d=4,o=5,b=125:a#,f.,8a#,16a#,16c6,16d6,16d#6,2f6,8p,8f6,16f.6,16f#6,16g#.6,2a#.6,16a#.6,16g#6,16f#.6,8g#.6,16f#.6,2f6,f6,8d#6,16d#6,16f6,2f#6,8f6,8d#6,8c#6,16c#6,16d#6,2f6,8d#6,8c#6,8c6,16c6,16d6,2e6,g6,8f6,16f,16f,8f,16f,16f,8f,16f,16f,8f,8f,a#,f.,8a#,16a#,16c6,16d6,16d#6,2f6,8p,8f6,16f.6,16f#6,16g#.6,2a#.6,c#7,c7,2a6,f6,2f#.6,a#6,a6,2f6,f6,2f#.6,a#6,a6,2f6,d6,2d#.6,f#6,f6,2c#6,a#,c6,16d6,2e6,g6,8f6,16f,16f,8f,16f,16f,8f,16f,16f,8f,8f'
rtttl.play(zelda)
song = 'Adams:d=4,o=5,b=160:8c,8d,8e,8f,1p,8d,8e,8f#,8g,1p,8d,8e,8f#,8g,p,8d,8e,8f#,8g,p,8c,8d,8e,8f'
rtttl.play(song)


while True:
    ring.fillAllRing(255, 130, 0)
    ultrasonic.ultrasonicRGB2(255, 100, 0)
    ring.bounce(n, int(255 * bright), int(153 * bright), int(0 * bright), 150)
    ring.fillAllRing(0, 255, 0)
    ultrasonic.ultrasonicRGB2(0, 255, 0)
    ring.cycle(n, int(51 * bright), int(204 * bright), int(0 * bright), 150)


