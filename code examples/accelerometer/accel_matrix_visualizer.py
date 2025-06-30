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

def draw_axes(x, y, z):
    # Normalize to bar lengths
    bx = clamp(int(abs(x) / 64))  # 0 to 7
    by = clamp(int(abs(y) / 64))
    bz = clamp(int((z + 1024) / 8))  # For blue background

    np.fill((0, 0, clamp(int(bz))))

    for i in range(bx):
        col = clamp(3 + i) if x > 0 else clamp(3 - i)
        idx = xy_to_index(col, 3)
        np[idx] = (0, 255, 0)  # green bar

    for i in range(by):
        row = clamp(3 + i) if y > 0 else clamp(3 - i)
        idx = xy_to_index(3, row)
        np[idx] = (255, 0, 0)  # red bar

    np.write()

while True:
    x, y, z = accel.read_axes()
    print("X:", x, "Y:", y, "Z:", z)
    draw_axes(x, y, z)
    time.sleep(0.1)
