from time import sleep, sleep_ms
from machine import Pin, reset
from neopixel import NeoPixel

brightm = 0.5  # brightness
nm = 64        # total number of pixels in the matrix
matrix = NeoPixel(Pin(22), nm) # Connector 3
tempo= 0.01

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
            matrix[matrixixel] = (0, 50, 0)
            matrix.write()
            sleep_ms(100)
            matrix[matrixixel] = (0, 0, 0)
            matrix.write()
    except KeyboardInterrupt:
        print('Keyboard Interrupt') # ctrl+c
    finally:
        print('Exiting....')
        reset()