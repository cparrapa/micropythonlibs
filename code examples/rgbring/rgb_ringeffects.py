import time
from machine import Pin
from neopixel import NeoPixel

n = 13 					   # Number of LEDs in the ring
ring = NeoPixel(Pin(4), n) # Connector 5

def set_color(r, g, b):
  for i in range(n):
    ring[i] = (r, g, b)
  ring.write()
set_color(255, 255, 0)
time.sleep_ms(200)

def wipe(r, g, b, wait):
    for i in range(n):
        ring[i] = (r, g, b)
        ring.write()
        time.sleep_ms(wait)
wipe(0, 255, 0, 50)

def cycle(r, g, b, wait):
    for i in range(1 * n):
        for j in range(n):
            ring[j] = (0, 0, 0)
        ring[i % n] = (r, g, b)
        ring.write()
        time.sleep_ms(wait)
cycle(0, 255, 255, 100)    
  
def bounce(r, g, b, wait):
    for i in range(1 * n):
        for j in range(n):
            ring[j] = (r, g, b)
        if (i // n) % 2 == 0:
            ring[i % n] = (0, 0, 0)
        else:
            ring[n - 1 - (i % n)] = (0, 0, 0)
        ring.write()
        time.sleep_ms(wait)
bounce(0, 0, 255, 100)

def wheel(pos): # function to go through all colors 
  # Iringut a value 0 to 255 to get a color value.
  # The colours are a transition r - g - b - back to r.
  if pos < 0 or pos > 255:
    return (0, 0, 0)
  if pos < 85:
    return (255 - pos * 3, pos * 3, 0)
  if pos < 170:
    pos -= 85
    return (0, 255 - pos * 3, pos * 3)
  pos -= 170
  return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
  for j in range(255):
    for i in range(n):
      rc_index = (i * 256 // n) + j
      ring[i] = wheel(rc_index & 255)
    ring.write()
    time.sleep_ms(wait)
rainbow_cycle(8)

def fade():
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            ring[j] = (val, 0, 0)
        ring.write()
fade()

for i in range(n):
    ring[i] = (0, 0, 0)
ring.write()