import time                       #importing machine and time libraries
from time import sleep, sleep_ms
from machine import Pin, reset
from ottoneopixel import OttoNeoPixel
from neopixel import NeoPixel


brightm = 0.3 # brightness variable for lights
nm = 64       # total number of pixels in the matrixo
matrixo = OttoNeoPixel(22, nm) # Connector 3
matrix = NeoPixel(Pin(22), nm) # Connector 3 using native librarhy instead
tempo= 0.01

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
           matrixo.pixels[i] = wheel(rc_index & 255)
       matrixo.pixels.write()
       time.sleep_ms(wait)

def bounce(r, g, b, wait):
   for i in range(2 * nm):
       for j in range(nm):
           matrixo.pixels[j] = (r,g,b)
       if (i // nm) % 2 == 0:
           matrixo.pixels[i % nm] = (0, 0, 0)
       else:
           matrixo.pixels[nm - 1 - (i % nm)] = (0, 0, 0)
       matrixo.pixels.write()
       time.sleep_ms(wait)

matrixo.fillAllRing(int(255 * brightm), 0, 0)
time.sleep(1)
matrixo.fillAllRing(0, int(255 * brightm), 0)
time.sleep(1)
matrixo.fillAllRing(0, 0, int(255 * brightm))
time.sleep(1)
bounce(int(255 * brightm), int(255 * brightm), int(255 * brightm),15)
rainbow_cycle(10)
time.sleep(1)
   
matrix.fill((0,255,255))

for i in range(nm):
    matrix[i] = (int(255 * brightm), int(255 * brightm), int(255 * brightm))
    matrix.write()
    sleep(tempo)

for i in range(nm):
    matrix[i] = (int(255 * brightm), int(0 * brightm), int(0 * brightm))
    matrix.write()
    sleep(tempo)
    
for i in range(nm):
    matrix[i] = (int(0 * brightm), int(255 * brightm), int(0 * brightm))
    matrix.write()
    sleep(tempo)
    
for i in range(nm):
    matrix[i] = (int(0 * brightm), int(0 * brightm), int(255 * brightm))
    matrix.write()
    sleep(tempo)
    
for i in range(nm):
    matrix[i] = (0, 0, 0)
    matrix.write()

while True:
    try:
        for matrixixel in range(nm):
            matrix[matrixixel] = (50, 50, 50)
            matrix.write()
            sleep_ms(30)
            matrix[matrixixel] = (0, 0, 0)
            matrix.write()
    except KeyboardInterrupt:
        print('Keyboard Interrupt') # ctrl+c
    finally:
        print('Exiting....')
        reset()
