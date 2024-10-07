from machine import Pin, SoftI2C
from adxl345 import ADXL345
import time

# Define I2C pins
#i2c = SoftI2C(scl=Pin(18), sda=Pin(19)) #Connector 1
#i2c = SoftI2C(scl=Pin(16), sda=Pin(17)) #Connector 2
i2c = SoftI2C(scl=Pin(22), sda=Pin(21)) #Connector 3

# Initialize ADXL345
accel = ADXL345(i2c)

# Read accelerometer data
while True:
    x, y, z = accel.ReadXYZ()
    print("{}".format(x))
    time.sleep(0.5)