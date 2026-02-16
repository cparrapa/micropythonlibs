from machine import Pin, I2C
import neopixel
from adxl345 import ADXL345
import math
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
accel = ADXL345(i2c)
np = neopixel.NeoPixel(Pin(16), 64)

# Simplified circular layout mapping (compass style ring around the edge)
ring = [
    3, 4, 5, 6, 7,      # top
    15, 23, 31,         # right
    39, 47, 55, 63,     # bottom
    62, 61, 60, 59,     # left
    51, 43, 35, 27, 19, 11,  # top-left to complete circle
    3                  # loop around
]

def angle_to_index(angle):
    # Convert angle to ring index
    segment = int((angle + 180) / 360 * len(ring)) % len(ring)
    return ring[segment]

while True:
    x, y, z = accel.read_axes()

    angle = math.atan2(y, x) * 180 / math.pi  # -180 to +180
    idx = angle_to_index(angle)

    np.fill((0, 0, 20))  # faint blue background
    np[idx] = (255, 0, 0)
    np.write()

    print("Angle:", int(angle))
    time.sleep(0.1)
