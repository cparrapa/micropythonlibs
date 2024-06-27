from time import sleep
from machine import Pin
from neopixel import NeoPixel

n = 13 					   # Number of LEDs in the ring
ring = NeoPixel(Pin(4), n) # Connector 5
WheelPos = 0

def Wheel():
    global WheelPos, n, L, i
    WheelPos = (255) - WheelPos
    if WheelPos < (85):
        for L in range(n):
            ring[L] = (255 - WheelPos * 3, 0, WheelPos * 3 )
        ring.write()


    elif WheelPos < (170):
        WheelPos -= 85
        for L in range(n):
            ring[L] = (0, WheelPos * 3, 255 - WheelPos * 3)
        ring.write()

    else:
        WheelPos -= 170
        for L in range(n):
            ring[L] = (WheelPos * 3, 255 - WheelPos * 3, 0)
        ring.write()

while True:
    for i in range((255)):
        WheelPos = i
        Wheel()
        sleep(0.02)
