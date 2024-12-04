from utime import sleep, time
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C

i2c = SoftI2C(sda=Pin(19), scl=Pin(18)) # Connector 1
oled = SSD1306_I2C(128, 64, i2c) # width, height using default address 0x3C
width=128
height=64

equations = ['(x * y) & 24', '(x * y) & 47', '(x * y) & 64', 'x & y', 'x % y', '(x % y) % 4', '40 % (x % y+1)']

for eqn in range(0, len(equations)):
    start = time()

    oled.fill(0) # clear display
    oled.text('calculating', 0, 0, 1)
    oled.text(equations[eqn], 0, 10, 1)
    oled.show()
    for x in range(width):
        for y in range(1, height):
            if eval(equations[eqn]):
               oled.pixel(x,y,0)
            else:
                oled.pixel(x,y,1)
    oled.show()
    sleep(5)

    end = time()
    duration = str(end - start)
    print(equations[eqn])
    print(duration, ' seconds')

oled.text('done', 0, 0, 1)
oled.show()
print('done')
