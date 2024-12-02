import machine
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import time
from time import sleep
import utime
import rotary
from rotary import Rotary

# OLED setup
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

rotary = Rotary(18, 19, 26) # GPIO Pins for the encoder pins Connector 2. third is the button press switch Connector 4.

def listprograms():
    return [f for f in os.listdir('/programs') if f.endswith('.py')]

def run_program(program):
    print(f"Running {program}...")
    with open(f'/programs/{program}') as f:
        exec(f.read())

programs = listprograms()
maxprog = len(listprograms())
select = 0

def rotary_changed(change):
    global select
    if change == Rotary.ROT_CW:
        select = select + 1
        if select == maxprog:
            select = 0
        print("Selected: ", select, "Program: ", programs[select])
    elif change == Rotary.ROT_CCW:
        if select == 0:
            select = maxprog - 1
        else:
            select = select - 1
        print("Selected: ", select, "Program: ", programs[select])
    elif change == Rotary.SW_PRESS:
        print("Press")
        run_program(programs[select])
    elif change == Rotary.SW_RELEASE:
        print("Unpress")

def run_program(program):
    print(f"Running {program}...")
    oled.fill(0)
    oled.text("Running", 0, 0)
    oled.text(f"{program}", 0, 10)
    oled.show()
    time.sleep(1)
    with open(f'/programs/{program}') as f:
        exec(f.read())

rotary.add_handler(rotary_changed)

print("Programs: ", programs, "Number of prg: ", maxprog, "Selected: ", select)

while True:
    oled.fill(0)
    oled.text("Program no. {}".format(select + 1), 0, 0)
    oled.fill_rect(0, 14, 128, 20, 1)
    oled.text(f"{programs[select]}", 0, 20, 0)
    oled.text("Press button", 0, 40)
    oled.text("to run program.", 0, 50)
    oled.show()
    time.sleep(.05)

if __name__ == "__main__":
    main()