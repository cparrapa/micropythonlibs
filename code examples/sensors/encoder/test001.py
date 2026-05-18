import machine
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
from time import sleep
import utime
import rotary
from rotary import Rotary

#OLED setup
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

rotary = Rotary(18, 19, 26) # GPIO Pins for the encoder pins Connector 2. third is the button press switch Connector 4.

programs = 2
maxprog = 5
select = 0
        
def rotary_changed(change):
    global select
    if change == Rotary.ROT_CW:
        cw()
    elif change == Rotary.ROT_CCW:
        ccw()
    elif change == Rotary.SW_PRESS:
        press()
    elif change == Rotary.SW_RELEASE:
        unpress()

def cw():
    global select
    select = select + 1
    if select == maxprog:
        select = 0
    print("Selected: ", select, "Program: ", "N/A")
    
def ccw():
    global select
    if select == 0:
        select = maxprog - 1
    else:
        select = select - 1
    print("Selected: ", select, "Program: ", "N/A")
    
def press():
    print("Press")
    
def unpress():
    print("Unpress")

rotary.add_handler(rotary_changed)

print("Programs: ", programs, "Number of prg: ", maxprog, "Selected: ", select)

while True:
    oled.fill(0)
    oled.text("Program no. {}".format(select + 1), 0, 0)
    oled.fill_rect(0, 14, 128, 20, 1)
    oled.text("N/A", 0, 20, 0)
    oled.text("Feedback", 0, 40)
    oled.text("test.", 0, 50)
    oled.show()
    time.sleep(.05)

if __name__ == "__main__":
    main()
