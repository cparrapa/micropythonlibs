import urandom, machine, utime, ssd1306
import random # random direction for new ball
from machine import Pin, PWM, SPI
from utime import sleep
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64

scl=machine.Pin(18) # Connector 13
sda=machine.Pin(19)
i2c=machine.I2C(0,sda=sda, scl=scl)
# Screen size
width=128
height=64
oled = SSD1306_I2C(width, height, i2c)

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
