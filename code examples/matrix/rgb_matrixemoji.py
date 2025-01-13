from time import sleep
from machine import Pin
from neopixel import NeoPixel

brightm = 0.3 # brightness variable for lights
nm = 64       # total number of pixels in the matrix
matrix = NeoPixel(Pin(22), nm) # Connector 3

matrix.fill((255,255,0))
matrix.write()
sleep(1)

def yellow():
    global i, nm, delay
    for i in range(nm):
        matrix[i] = (int(255 * brightm), int(255 * brightm), int(0 * brightm))
        matrix.write()

yellow()

# face negative
matrix[0] = (0,0,0)
matrix[1] = (0,0,0)
matrix[8] = (0,0,0)
matrix[6] = (0,0,0)
matrix[7] = (0,0,0)
matrix[15] = (0,0,0)
matrix[48] = (0,0,0)
matrix[55] = (0,0,0)
matrix[56] = (0,0,0)
matrix[57] = (0,0,0)
matrix[62] = (0,0,0)
matrix[63] = (0,0,0)

# eyes
matrix[18] = (100, 200, 0) 
matrix[21] = (100, 200, 0)

# mouth
matrix[42] = (100, 100, 100) 
matrix[51] = (100, 100, 100)   
matrix[52] = (100, 100, 100)  
matrix[45] = (100, 100, 100)  

matrix.write()
