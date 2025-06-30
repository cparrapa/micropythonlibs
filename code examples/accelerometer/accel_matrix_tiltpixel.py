from machine import Pin, I2C
import neopixel
from adxl345 import ADXL345
import time

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
accel = ADXL345(i2c)
np = neopixel.NeoPixel(Pin(16), 64)

pos_x, pos_y = 3, 3

def xy_to_index(x, y):
    return y * 8 + x if y % 2 == 0 else y * 8 + (7 - x)

def draw_ball(x, y):
    np.fill((0, 0, 0))
    idx = xy_to_index(x, y)
    np[idx] = (0, 255, 0)
    np.write()

def clamp(val, min_val=0, max_val=7):
    return max(min_val, min(val, max_val))

cooldown = 0

while True:
    x, y, z = accel.read_axes()
    print("Tilt X:", x, "Y:", y)

    if cooldown == 0:
        moved = False
        if x > 200:
            pos_x = clamp(pos_x - 1)
            moved = True
        elif x < -200:
            pos_x = clamp(pos_x + 1)
            moved = True

        if y > 200:
            pos_y = clamp(pos_y - 1)
            moved = True
        elif y < -200:
            pos_y = clamp(pos_y + 1)
            moved = True

        if moved:
            cooldown = 3  # wait 3 frames before next move

    draw_ball(pos_x, pos_y)

    cooldown = max(0, cooldown - 1)
    time.sleep(0.1)
