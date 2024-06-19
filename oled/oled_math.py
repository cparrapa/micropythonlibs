import machine
import ssd1306
from utime import sleep, time
import utime
from ssd1306 import SSD1306_I2C

WIDTH = 128
HEIGHT = 64
sda=machine.Pin(21)
scl=machine.Pin(22)
i2c=machine.I2C(0,sda=sda, scl=scl)
# Screen size
width=128
height=64
oled = SSD1306_I2C(width, height, i2c)

equations = ['(x * y) & 24', '(x * y) & 47', '(x * y) & 64', 'x & y', 'x % y', '(x % y) % 4', '40 % (x % y+1)']

for eqn in range(0, len(equations)):
    start = time()

    oled.fill(0) # clear display
    oled.text('calculating', 0, 0, 1)
    oled.text(equations[eqn], 0, 10, 1)
    oled.show()
    for x in range(WIDTH):
        for y in range(1, HEIGHT):
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
