from machine import Pin, I2C, SoftI2C
import ssd1306
import time

# Initialize I2C interfaces
oled_i2c = SoftI2C(scl=Pin(18), sda=Pin(19)) #Connector 1
accel_i2c = I2C(1, scl=Pin(22), sda=Pin(21)) #Connector 3

# Define device address
ADXL345_ADDR = 0x53  # Alternatively, try 0x1D

# ADXL345 register addresses
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATAX0 = 0x32

# Initialize ADXL345
def init_adxl345():
    # Set device in measurement mode
    accel_i2c.writeto_mem(ADXL345_ADDR, POWER_CTL, bytes([0x08]))
    # Set data format
    accel_i2c.writeto_mem(ADXL345_ADDR, DATA_FORMAT, bytes([0x08]))

# Read accelerometer data
def read_accel():
    data = accel_i2c.readfrom_mem(ADXL345_ADDR, DATAX0, 6)
    x = int.from_bytes(data[0:2], 'little')
    y = int.from_bytes(data[2:4], 'little')
    z = int.from_bytes(data[4:6], 'little')
    
    # Convert data to signed numbers
    if x & (1 << 15): x -= (1 << 16)
    if y & (1 << 15): y -= (1 << 16)
    if z & (1 << 15): z -= (1 << 16)
    
    return x, y, z

# Initialize OLED display
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, oled_i2c)

# Initialize sensor
init_adxl345()

# Function to draw large text on OLED
def draw_large_text(oled, text, x, y):
    for i, c in enumerate(text):
        oled.text(c, x + i * 16, y)
        oled.text(c, x + i * 16 + 1, y)
        oled.text(c, x + i * 16, y + 1)
        oled.text(c, x + i * 16 + 1, y + 1)

while True:
    try:
        x, y, z = read_accel()
        # Clear the display
        oled.fill(0)
        # Display accelerometer data
        draw_large_text(oled, "X: {}".format(x), 0, 0)
        draw_large_text(oled, "Y: {}".format(y), 0, 16)
        draw_large_text(oled, "Z: {}".format(z), 0, 32)
        # Refresh the display
        oled.show()
        print("X:", x, "Y:", y, "Z:", z)  # Print debug information
        time.sleep(1)  # Increase time interval
    except KeyboardInterrupt:
        print("Program interrupted")
        break
