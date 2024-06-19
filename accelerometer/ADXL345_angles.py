from machine import Pin, I2C
import time
import ustruct
import math
 
# Constants
ADXL345_ADDRESS = 0x53
ADXL345_POWER_CTL = 0x2D
ADXL345_DATA_FORMAT = 0x31
ADXL345_DATAX0 = 0x32
 
# Initialize I2C
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=400000)
 
# Initialize ADXL345
def init_adxl345():
    i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_POWER_CTL, bytearray([0x08]))  # Set bit 3 to 1 to enable measurement mode
    i2c.writeto_mem(ADXL345_ADDRESS, ADXL345_DATA_FORMAT, bytearray([0x0B]))  # Set data format to full resolution, +/- 16g
 
# Read acceleration data
def read_accel_data():
    data = i2c.readfrom_mem(ADXL345_ADDRESS, ADXL345_DATAX0, 6)
    x, y, z = ustruct.unpack('<3h', data)
    return x, y, z
 
# Calculate the magnitude of acceleration
def calc_accel_magnitude(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)
 
# Calculate roll angle in degrees
def calc_roll(x, y, z):
    return math.atan2(y, math.sqrt(x**2 + z**2)) * (180 / math.pi)
 
# Calculate pitch angle in degrees
def calc_pitch(x, y, z):
    return math.atan2(-x, math.sqrt(y**2 + z**2)) * (180 / math.pi)
 
# Main loop
init_adxl345()
while True:
    x, y, z = read_accel_data()
    magnitude = calc_accel_magnitude(x, y, z)
    roll = calc_roll(x, y, z)
    pitch = calc_pitch(x, y, z)
    print("X: {}, Y: {}, Z: {}, Magnitude: {:.2f}, Roll: {:.2f}, Pitch: {:.2f}".format(x, y, z, magnitude, roll, pitch))
    time.sleep(0.1)