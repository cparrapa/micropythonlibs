from machine import Pin, I2C
import neopixel
from adxl345 import ADXL345
import time
import urandom

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
accel = ADXL345(i2c)
np = neopixel.NeoPixel(Pin(16), 64)



def sparkle():
    np.fill((0, 0, 0))
    for _ in range(10):
        idx = urandom.getrandbits(6)
        color = (
            urandom.getrandbits(6) * 4,
            urandom.getrandbits(6) * 4,
            urandom.getrandbits(6) * 4
        )
        np[idx] = color
        np.write()
        time.sleep(0.05)
        np[idx] = (0, 0, 0)
    np.write()


import math

def rainbow_color(i):
    # Simple HSV-to-RGB trick
    angle = i * math.pi * 2 / 64
    r = int((math.sin(angle) + 1) * 10)
    g = int((math.sin(angle + 2) + 1) * 10)
    b = int((math.sin(angle + 4) + 1) * 10)
    return (r, g, b)

def sparkle_rainbow():
    for _ in range(30):
        for i in range(64):
            np[i] = rainbow_color(i)
        np.write()
        time.sleep(0.03)
    np.fill((0, 0, 0))
    np.write()


while True:
    x, y, z = accel.read_axes()
    shake = abs(x) + abs(y) + abs(z)
    if shake > 300:  # Adjust threshold to suit your sensor
        sparkle() #sparkle_rainbow()
    time.sleep(0.1)
