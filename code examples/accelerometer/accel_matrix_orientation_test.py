from machine import Pin, I2C
from adxl345 import ADXL345
import time, math

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
accel = ADXL345(i2c)

prev_x, prev_y, prev_z = 0, 0, 0

def calc_angle(x, y):
    angle = math.atan2(y, x) * 180 / math.pi
    return angle

while True:
    x, y, z = accel.read_axes()
    angle = calc_angle(x, y)
    print("X:", x, "Y:", y, "Z:", z)

    dx = abs(x - prev_x)
    dy = abs(y - prev_y)
    dz = abs(z - prev_z)

    shake = dx > 100 or dy > 100 or dz > 100

    print("Angle XY: {:.1f}°  |  Shake: {}".format(angle, "YES" if shake else "no"))

    prev_x, prev_y, prev_z = x, y, z
    time.sleep(0.2)
