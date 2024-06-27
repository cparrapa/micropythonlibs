from time import sleep
from machine import Pin
from neopixel import NeoPixel

bright = 0.5  			   # brightness variable for lights
n = 13 					   # Number of LEDs in the ring
ring = NeoPixel(Pin(4), n) # Connector 5

for i in range(13):
    ring[i] = (int(255 * bright), int(255 * bright), int(255 * bright))
    ring.write()
    sleep(0.06)

for i in range(13):
    ring[i] = (int(255 * bright), 0, 0)
    ring.write()
    sleep(0.06)
    
for i in range(13):
    ring[i] = (0, int(255 * bright), 0)
    ring.write()
    sleep(0.06)
    
for i in range(13):
    ring[i] = (0, 0, int(255 * bright))
    ring.write()
    sleep(0.06)
    
for i in range(13):
    ring[i] = (0, 0, 0)
    ring.write()
    
ring[1] = (255, 0, 0) # set to red, full brightness
ring[2] = (255, 0, 0)
ring[3] = (255, 0, 0)
ring[4] = (255, 0, 0) 
ring[5] = (0, 128, 0) # set to green, half brightness
ring[6] = (0, 128, 0)
ring[7] = (0, 128, 0)
ring[8] = (0, 128, 0)
ring[9] = (0, 0, 64)  # set to blue, quarter brightness
ring[10] = (0, 0, 64)
ring[11] = (0, 0, 64)
ring[12] = (0, 0, 64)  
ring.write()
sleep(1)
    
def demo(ring):
    n = ring.n

    # cycle
    for i in range(2 * n):
        for j in range(n):
            ring[j] = (0, 0, 0)
        ring[i % n] = (255, 255, 255)
        ring.write()
        sleep(0.025)

    # bounce
    for i in range(2 * n):
        for j in range(n):
            ring[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            ring[i % n] = (0, 0, 0)
        else:
            ring[n - 1 - (i % n)] = (0, 0, 0)
        ring.write()
        sleep(0.06)

    # fade in/out
    for i in range(0, 5 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            ring[j] = (val, 0, 0)
        ring.write()

    # clear
    for i in range(n):
        ring[i] = (0, 0, 0)
    ring.write()
    
demo(ring)

ring.fill((255,255,0))
ring.write()

sleep(1)
luz = 0
for count in range(13):
    ring[luz] = (int(255 * bright), 0, int(255 * bright))
    ring.write()
    luz += 1
    sleep(0.1)
    for count in range(13):
        ring[count] = (0, 0, 0)
    ring.write()
    print(luz)
luz = 0
