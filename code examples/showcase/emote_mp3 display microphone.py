# This code requires MP3, microphone and OLED display, pending to update OLED to conenctor 1
# It makes Otto move his eyes randomly and react to sound by opening his mouth

import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor
from ottodisplay import OttoOled
import random
offset = 0

microphone = Pin(33, Pin.IN, Pin.OUT)
oled = OttoOled(21, 22)

n = 0
last = 0
debounce = 200
now = 0
is_talking = False

# Pupil variables
locationleftx = 30
locationlefty = 17
locationrightx = 98
locationrighty = 17
movementx = [0, 0]
movementy = [0, 0]

oled.Eyes1Draw()
oled.showDisplay()
oled.Mouth1Draw()
oled.showDisplay()

def talking():
    global is_talking
    is_talking = True
    microphone.irq(handler=None)
    
    # Talking sequence
    oled.clearDisplay()
    oled.Eyes1Draw()
    oled.Mouth2Draw()
    oled.showDisplay()
    
    time.sleep(.2)
    
    oled.clearDisplay()
    oled.Eyes1Draw()
    oled.Mouth1Draw()
    oled.showDisplay()
    
    microphone.irq(trigger=Pin.IRQ_RISING, handler=micrec)
    is_talking = False


def micrec(self):
    global n, last, now
    now = time.ticks_ms()
    if time.ticks_diff(now, last) > debounce and not is_talking:
        print("Sound recognized: ", n)
        n += 1
        talking()
        last = now

microphone.irq(trigger=Pin.IRQ_RISING, handler=micrec)

while True:
    time.sleep(1)
    randx = random.randint(-5, 5)
    randy = random.randint(-3, 3)
    oled.clearDisplay()
    oled.Mouth1Draw()
    oled.circleDisplay(30, 17, 17)
    oled.circleBlackDisplay(locationleftx + randx, locationlefty + randy, 10)
    oled.circleDisplay(98, 17, 17)
    oled.circleBlackDisplay(locationrightx + randx, locationrighty + randy, 10)
    oled.showDisplay()
    