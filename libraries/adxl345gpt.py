# adxl345.py
from machine import I2C

class ADXL345:
    def __init__(self, i2c, addr=0x53):
        self.i2c = i2c
        self.addr = addr
        # Enable measurement mode
        self.i2c.writeto_mem(self.addr, 0x2D, b'\x08')

    def read_axes(self):
        data = self.i2c.readfrom_mem(self.addr, 0x32, 6)

        def to_signed(val):
            return val - 65536 if val > 32767 else val

        x = to_signed(data[0] | (data[1] << 8))
        y = to_signed(data[2] | (data[3] << 8))
        z = to_signed(data[4] | (data[5] << 8))

        return x, y, z


