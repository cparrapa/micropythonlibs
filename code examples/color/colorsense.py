from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoNeoPixel
from machine import Pin
from machine import I2C
from ottosensors import TCS34725
from time import sleep

i = None

buzzer_25 = OttoBuzzer(25)

neopixel = OttoNeoPixel(4, 13)

i2c_bus = I2C(0, sda=Pin(21), scl=Pin(22))
tcs = TCS34725(i2c_bus)


buzzer_25.playEmoji("S_connection")
neopixel.setBrightness(((100)/100))
while True:
    tcsred,tcsgreen,tcsblue=tcs.html_rgb(tcs.read(True))
    tcs_h,tcs_s,tcs_b=tcs.rgb_to_hsv(tcsred,tcsgreen,tcsblue)
    for i in range(13):
        neopixel.setRGBLed(tcsred, tcsgreen, tcsblue, i)
        print('hue' + str(tcs_h))
        print('red' + str(tcsred))


    if (tcsred) > 60 and (tcsred) <= 70:
        buzzer_25.playNote(466, 125)
    elif (tcs_h) > 2 and (tcs_h) <= 40:
        buzzer_25.playNote(523, 125)
    elif (tcs_h) > 40 and (tcs_h) <= 80:
        buzzer_25.playNote(587, 125)
    elif (tcs_h) > 80 and (tcs_h) <= 120:
        buzzer_25.playNote(622, 125)
    elif (tcs_h) > 120 and (tcs_h) <= 160:
        buzzer_25.playNote(698, 125)
    elif (tcs_h) > 160 and (tcs_h) <= 220:
        buzzer_25.playNote(784, 125)
    elif (tcs_h) > 220 and (tcs_h) <= 260:
        buzzer_25.playNote(880, 125)
    elif (tcs_h) > 260 and (tcs_h) <= 270:
        buzzer_25.playNote(932, 125)
    else:
        buzzer_25.playNote(0, 500)
    sleep(0.5)
