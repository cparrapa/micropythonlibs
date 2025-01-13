from ottoencoder import Rotary
import utime as time
from machine import Pin
from neopixel import NeoPixel
from ottooled import OttoOled

led = Pin(2, Pin.OUT)    # Built in LED
ring = NeoPixel(Pin(4), 13)  # Connector 5
oled = OttoOled(19, 18) # Connector 1

rotary = Rotary(16, 17, 26) # GPIO Pins for the encoder pins Connector 2. third is the button press switch Connector 4.
val = 0

def rotary_changed(change):
    global val
    if change == Rotary.ROT_CW:
        val = val + 1
        print(val)
    elif change == Rotary.ROT_CCW:
        val = val - 1
        print(val)
    elif change == Rotary.SW_PRESS:
        print('PRESS')
        led.on()
    elif change == Rotary.SW_RELEASE:
        print('RELEASE')
        led.off()

rotary.add_handler(rotary_changed)

while True:
    time.sleep(0.05)
    if val >= (13):
        val = 0
    ring.fill((0,0,0))
    ring[val] = (0, 255, 0)
    ring.write()
    oled.clearDisplay()
    oled.writeTextDisplay(val, 0, 0)
    oled.showDisplay()
    