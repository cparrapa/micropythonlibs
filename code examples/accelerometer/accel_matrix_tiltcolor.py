from machine import Pin, I2C
import neopixel
from adxl345 import ADXL345
import time
import math

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
accel = ADXL345(i2c)
np = neopixel.NeoPixel(Pin(16), 64)

def set_all(color):
    for i in range(64):
        np[i] = color
    np.write()

def normalize(x, y, z):
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    if magnitude == 0:
        return (0, 0, 0)
    scale = 5  # Lower = dimmer
    r = int((x / magnitude) * scale + scale)
    g = int((y / magnitude) * scale + scale)
    b = int((z / magnitude) * scale + scale)
    return (r, g, b)

while True:
    x, y, z = accel.read_axes()
    print("X:", x, "Y:", y, "Z:", z)

    color = normalize(x, y, z)
    set_all(color)
    time.sleep(0.1)
