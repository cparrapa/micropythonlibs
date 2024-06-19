from machine import Pin, I2C
import machine
from ssd1306 import SSD1306_I2C
import ssd1306
import utime

sda=machine.Pin(21)
scl=machine.Pin(22)

i2c=I2C(0,sda=sda, scl=scl, freq=400000)
display = SSD1306_I2C(128, 64, i2c)


display.fill(0) # clear to black
display.text('Otto Rocks', 0, 0, 1) # at x=0, y=0, white on black
# line under title
display.hline(0, 9, 127, 1)
# bottom of display
display.hline(0, 30, 127, 1)
# left edge
display.vline(0, 10, 32, 1)
# right edge
display.vline(127, 10, 32, 1)

for i in range(0, 118):
    # box x0, y0, width, height, on
    display.fill_rect(i,10, 10, 10, 1)
    # draw black behind number
    display.fill_rect(10, 21, 30, 8, 0)
    display.text(str(i), 10, 21, 1)
    display.show() # update display
    # utime.sleep(0.001)

print('done')
