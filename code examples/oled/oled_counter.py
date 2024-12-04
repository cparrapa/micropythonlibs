import utime
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C

i2c = SoftI2C(sda=Pin(19), scl=Pin(18)) # Connector 1
oled = SSD1306_I2C(128, 64, i2c) # width, height using default address 0x3C

for i in range(1, 51): # count 1 to 50
    oled.fill(0) # clear to black
    oled.text('Otto Rocks!', 0, 0, 1) # at x=0, y=0, white on black
    oled.text(str(i), 40, 20, 1) # move 30 pixels horizontal and 20 down from the top
    oled.show() # update display
    utime.sleep(0.1) #wait 1/10th of a second

print('done')
oled.fill(0)
oled.text("Hello World!", 0, 0)
oled.show()

