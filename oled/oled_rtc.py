from machine import Pin, I2C, RTC
from time import sleep_ms 
from ssd1306 import SSD1306_I2C

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

rtc = RTC() 
rtc.datetime((2024, 5, 20, 6, 15, 00, 0, 0)) 
# rtc.datetime((YYYY, MM, DD, WD, HH, MM, SS, MS)) 
# WD 1 = Monday 
# WD 7 = Sunday 
isPoint = True

while True: 
    t = rtc.datetime() 
    oled.fill(0) 
    oled.text('** RTC Time **', 4, 0) 
    oled.text('Date: {}-{:02d}/{:02d}' .format(t[1],t[2],t[0]), 0, 25)  
    if isPoint: 
        colon = ':' 
    else: 
        colon = ' ' 
    oled.text('Time: {:02d}{}{:02d}:{:02d}' .format(t[4], colon, t[5], t[6]), 0, 40) 
    oled.show() 
    sleep_ms(500) 
    isPoint = not isPoint