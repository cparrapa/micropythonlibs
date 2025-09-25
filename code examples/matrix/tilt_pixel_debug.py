import machine
import neopixel
import time
from machine import I2C, Pin

# === ADXL345 Setup ===
class ADXL345:
    def __init__(self, i2c, addr=0x53):
        self.i2c = i2c
        self.addr = addr
        self.i2c.writeto_mem(self.addr, 0x2D, b'\x08')  # Power on
        self.i2c.writeto_mem(self.addr, 0x31, b'\x08')  # Full resolution, ±2g


    def read(self):
        data = self.i2c.readfrom_mem(self.addr, 0x32, 6)
        x = int.from_bytes(data[0:2], 'little', True)
        y = int.from_bytes(data[2:4], 'little', True)
        z = int.from_bytes(data[4:6], 'little', True)
        return x, y, z

# === NeoPixel Setup ===
MATRIX_WIDTH = 8
MATRIX_HEIGHT = 8
NUM_PIXELS = MATRIX_WIDTH * MATRIX_HEIGHT
NEOPIXEL_PIN = 16  # Use GPIO 16

np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

# === I2C Setup ===
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
accel = ADXL345(i2c)

# === Helper Functions ===
def clear():
    for i in range(NUM_PIXELS):
        np[i] = (0, 0, 0)
    np.write()

def xy_to_index(x, y):
    # Non-zigzag layout
    return y * MATRIX_WIDTH + x

# === Main Loop with Debugging ===
x_f = 3.0
y_f = 3.0

while True:
    print("Scanning I2C bus...")
    devices = i2c.scan()
    print("I2C devices found:", devices)

    x, y, z = accel.read()
    print("Raw Accel:", x, y, z)

    # Adjust axis mapping if needed
    x_f += x / 1000
    y_f -= y / 1000

    print("x_f:", x_f, "y_f:", y_f)

    x_pos = max(0, min(7, int(x_f)))
    y_pos = max(0, min(7, int(y_f)))

    print("x_pos:", x_pos, "y_pos:", y_pos)

    index = xy_to_index(x_pos, y_pos)
    print("Lighting index:", index)

    clear()
    np[index] = (0, 255, 0)
    np.write()

    time.sleep(0.2)
