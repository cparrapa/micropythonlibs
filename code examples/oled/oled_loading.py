from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C

i2c = SoftI2C(sda=Pin(19), scl=Pin(18)) # Connector 1
oled = SSD1306_I2C(128, 64, i2c) # width, height using default address 0x3C

oled.fill(0) # clear to black
oled.text('HP Robots!', 0, 0, 1) # at x=0, y=0, white on black
# line under title
oled.hline(0, 9, 127, 1)
# bottom of oled
oled.hline(0, 30, 127, 1)
# left edge
oled.vline(0, 10, 32, 1)
# right edge
oled.vline(127, 10, 32, 1)

for i in range(0, 118):
    # box x0, y0, width, height, on
    oled.fill_rect(i,10, 10, 10, 1)
    # draw black behind number
    oled.fill_rect(10, 21, 30, 8, 0)
    oled.text(str(i), 10, 21, 1)
    oled.show() # update oled
    # utime.sleep(0.001)

print('done')
