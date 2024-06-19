from rotary import Rotary
import utime as time
from machine import Pin
from neopixel import NeoPixel

led = Pin(2, Pin.OUT)    # Built in LED
np = NeoPixel(Pin(22), 64)  # Connector 3
#from ottooled import OttoOled
#oled = OttoOled(21, 22)

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
    elif change == Rotary.SW_RELEASE:
        print('RELEASE')

rotary.add_handler(rotary_changed)

while True:
    time.sleep(0.1)
    #oled.clearDisplay()
    #oled.writeTextDisplay(val, 0, 0)
    #oled.showDisplay()
    np.fill((0,0,0))
    np[val] = (0, 255, 0)
    np.write()