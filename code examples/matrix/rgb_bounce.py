from utime import sleep
from machine import Pin
from neopixel import NeoPixel

ROWS = 8
COLS = 8
nm = ROWS * COLS # number of pixels in the matrix
matrix = NeoPixel(Pin(16), nm) #Connector 2
# Bounce a ball around a NeoPixel Matrix
# matrix = [[0 for _ in range(cols)] for _ in range(rows)]

def clear():
    for i in range(0, nm):
        matrix[i] = (0,0,0)
    matrix.write()

def write_pixel(x, y, value):
    if y >= 0 and y < ROWS and x >=0 and x < COLS:
        # odd count rows 1, 3, 5 the wire goes from bottup
        #if x % 2: 
            #matrix[(x+1)*ROWS - y - 1] = value             
        #else: # even count rows, 0, 2, 4 the wire goes from the top down up
            matrix[x*ROWS + y] = value
            
def show():
    matrix.write()

# draw four colors at each corner of the matrix
write_pixel(0, 0, (255, 0, 0)) # draw a red pixel at the top left corner
write_pixel(7, 0, (0, 255, 0)) # draw a green pixel at the lower left corner
write_pixel(0, 7, (0, 0, 255)) # draw a blue pixel at the top right corner
write_pixel(7, 7, (255, 255, 255)) # draw a white pixel at the lower right corner

brightness=50
x=0
y=0
dx = 1
dy = 1
counter = 0
while True:
    if x <= 0:
        dx = 1
    if y <= 0:
        dy = 1
    if x >= COLS-1:
        dx = -1
    if y >= ROWS-1:
        dy = -1
    print(x,y)
    if counter < 100:
        write_pixel(x, y, (brightness,0,0)) # blue
    elif counter < 200:
        write_pixel(x, y, (0,brightness,0)) # blue
    elif counter < 300:
        write_pixel(x, y, (0,0,brightness)) # blue
    show()
    x += dx
    y += dy
    counter += 1
    if counter > 300:
        counter = 0
    if not counter % 150:
        x += 1
    sleep(.1)
