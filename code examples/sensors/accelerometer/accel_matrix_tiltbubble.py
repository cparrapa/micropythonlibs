from machine import Pin, I2C
import neopixel
from adxl345 import ADXL345
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
accel = ADXL345(i2c)
np = neopixel.NeoPixel(Pin(16), 64)

def xy_to_index(x, y):
    return y * 8 + x if y % 2 == 0 else y * 8 + (7 - x)

def clamp(val, min_val=0, max_val=7):
    return max(min_val, min(val, max_val))

while True:
    x, y, z = accel.read_axes()

    # Map x/y tilt to bubble position (invert for spirit level logic)
    px = clamp(4 - int(x / 150))
    py = clamp(4 - int(y / 150))

    np.fill((0, 0, 0))
    np[xy_to_index(px, py)] = (0, 255, 0)
    np.write()

    print("Bubble at:", px, py)
    time.sleep(0.1)
