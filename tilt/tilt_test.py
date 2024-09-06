import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, I2C         #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
#OLED stuff
from ottooled import OttoOled
from ssd1306 import SSD1306_I2C 

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
digital = Pin(33, Pin.IN)

#OLED connections
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

currenttime = time.ticks_ms()
lasttime = currenttime
responsetime = 50

def tilt_change(pin):
    
    global currenttime
    global lasttime
    
    currenttime = time.ticks_ms()
    
    if time.ticks_diff(currenttime, lasttime) > responsetime:
        time.sleep(.1)
        if digital.value() == 1:
            print("L ", digital.value())
            oled.fill(0)
            oled.text('Left', 0, 0)
            oled.show()
            
        else:
            print("R ", digital.value())
            oled.fill(0)
            oled.text('Right', 0, 0)
            oled.show()
    else:
        ()
    
    lasttime = currenttime
    
digital.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=tilt_change)

while True:
    print(digital.value())
    time.sleep(.1)