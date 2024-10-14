import ssd1306, utime, machine
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

scl=machine.Pin(18) # Connector 1
sda=machine.Pin(19)

i2c=I2C(0,sda=sda, scl=scl, freq=400000)
display = SSD1306_I2C(128, 64, i2c)

display.fill(0) # clear to black
display.text('HP Robots!', 0, 0, 1) # at x=0, y=0, white on black
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
