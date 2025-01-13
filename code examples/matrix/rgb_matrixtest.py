import time                       #importing machine and time libraries
from machine import Pin, ADC, PWM #importing Pin, ADC and PWM classes
from ottoneopixel import OttoNeoPixel

brightm = 0.1 # brightness variable for lights
nm = 64       # total number of pixels in the matrix
matrix = OttoNeoPixel(22, nm) # Connector 3

def wheel(pos):
   if pos < 0 or pos > 255:
      return (0, 0, 0)
   if pos < 85:
      return (int((255 - pos * 3)*brightm), int(pos * 3*brightm), 0)
   if pos < 170:
       pos -= 85
       return (0, int((255 - pos * 3)*brightm), int(pos * 3*brightm))
   pos -= 170
   return (int(pos * 3*brightm), 0, int((255 - pos * 3)*brightm))

def rainbow_cycle(wait):
   for j in range(255):
       for i in range(nm):
           rc_index = (i * int(256 * brightm) // nm) + j
           matrix.pixels[i] = wheel(rc_index & 255)
       matrix.pixels.write()
       time.sleep_ms(wait)

def bounce(r, g, b, wait):
   for i in range(2 * nm):
       for j in range(nm):
           matrix.pixels[j] = (r,g,b)
       if (i // nm) % 2 == 0:
           matrix.pixels[i % nm] = (0, 0, 0)
       else:
           matrix.pixels[nm - 1 - (i % nm)] = (0, 0, 0)
       matrix.pixels.write()
       time.sleep_ms(wait)

matrix.fillAllRing(int(255 * brightm), 0, 0)
time.sleep(1)
matrix.fillAllRing(0, int(255 * brightm), 0)
time.sleep(1)
matrix.fillAllRing(0, 0, int(255 * brightm))
time.sleep(1)
bounce(int(255 * brightm), int(255 * brightm), int(255 * brightm),15)
rainbow_cycle(10)
time.sleep(1)
   

