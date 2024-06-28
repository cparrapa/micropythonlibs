from machine import Pin, SoftI2C
from adxl345 import ADXL345
import time

# Define I2C pins
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))

# Initialize ADXL345
accel = ADXL345(i2c)

# Read accelerometer data
while True:
    x, y, z = accel.ReadXYZ()
    print("x = {}, y = {}, z = {}".format(x, y, z))
    roll,pitch = accel.RollPitch()
    print("roll = {0:.2f}, pitch = {1:.2f}".format(roll,pitch))    
    time.sleep(0.5)