import machine
from machine import Pin, PWM, I2C, SoftI2C
from ssd1306 import SSD1306_I2C
import time

#OLED setup
i2c = SoftI2C(scl=Pin(18), sda=Pin(19), freq=400000) 
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

ir = Pin(27)

n = 0

timenow = 0
timelast = 0
timediff = 0

def irchange(pin):
    global n, timenow, timelast, timediff
    timelast = timenow
    timenow = time.ticks_ms()
    timediff = time.ticks_diff(timelast, timenow)
    print("n =", n, "| timediff = ", timediff)
    n += 1
    if pin.value() == 1:
        oled.fill(0)
        oled.text("1, n = {}".format(n), 0, 0)
        oled.text("Time diff: {}".format(timediff), 0, 10)
        oled.show()
    else:
        time.sleep(.01)
# Setup IRQ on the IR pin
ir.irq(trigger=Pin.IRQ_RISING, handler=irchange)

oled.fill(0)
oled.text("Tap IR to start.", 0, 0)
oled.show()

while True:
    time.sleep(10)
