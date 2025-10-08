from time import sleep
from machine import Pin, I2C
from ht16k33 import HT16K33MatrixFeatherWing
from ottoledmatrix import OttoLedMatrix
import math

i2c = I2C(scl=Pin(16), sda=Pin(17))
display = HT16K33MatrixFeatherWing(i2c)
display.set_brightness(2)
ledmatrix = OttoLedMatrix(16,17)

def OttoDotMatrix(value):
    for i in range(128):
        x = math.floor(i / 16)
        y = i % 16
        if(y >= 8):
            y -= 8
            x += 8
        if(value[i] == '1'):
            display.plot(x, y).draw()

display.plot(0,0).draw()
sleep(1)
display.plot(15,0).draw()
sleep(1)
display.plot(7,0).draw()
sleep(1)
display.plot(15,7).draw()
sleep(1)
display.plot(7,7).draw()
sleep(1)
display.plot(8,7).draw()
sleep(1)

for i in range(8):
    ledmatrix.OttoEyes(i)
    ledmatrix.OttoMouth(i)
    sleep(1)
    ledmatrix.MatrixClear()
for i in range(12):
    ledmatrix.OttoMouth(i)
    sleep(1)
    ledmatrix.MatrixClear()
OttoDotMatrix("11100000000001111111100000011111011111000011111001111100001111100011100000011100000000000000000000000000000000000000000000000000")