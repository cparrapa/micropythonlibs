import urandom
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C

i2c = SoftI2C(sda=Pin(19), scl=Pin(18)) # Connector 1
oled = SSD1306_I2C(128, 64, i2c) # width, height using default address 0x3C

HEART = [
    [ 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [ 0, 1, 1, 0, 0, 0, 1, 1, 0],
    [ 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [ 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [ 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [ 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

def draw_heart(xofs, yofs):
    for y, row in enumerate(HEART):
        for x, c in enumerate(row):
            oled.pixel(x + xofs, y + yofs, c)

def random_heart():
    xofs = urandom.getrandbits(7)
    yofs = urandom.getrandbits(6)
    print(xofs, yofs)
    draw_heart(xofs, yofs)

oled.fill(0)
for n in range(10):
    random_heart()

oled.show()
