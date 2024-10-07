from utime import sleep
from machine import Pin
from neopixel import NeoPixel

nm = 64 # total number of pixels in the matrix
matrix = NeoPixel(Pin(16), nm) # Connector 2

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
    global nm, matrix
    for j in range(255):
        for i in range(nm):
            rc_index = (i * 256 // nm) + j
            # print(rc_index)
            matrix[i] = wheel(rc_index & 255)
        matrix.write()
    sleep(wait)

counter = 0
offset = 0
while True:
    print('Running cycle', counter)
    rainbow_cycle(.5)
    counter += 1
