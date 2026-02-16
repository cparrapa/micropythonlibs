from time import sleep
from machine import Pin
from neopixel import NeoPixel

nm = 64 # total number of pixels in the matrix
matrix = NeoPixel(Pin(22), nm) # Connector 3

color = 25 # we use the same brightness for each color
delay = .05
# here we define variables for each color
red = (color, 0, 0)
green = (0, color, 0)
blue = (0, 0, color)

# draw red up the matrix
for i in range(0, nm):
    matrix[i] = red
    matrix.write()
    sleep(delay)
    matrix[i] = (0,0,0)
# draw blue up the matrix
for i in range(0, nm):
    matrix[i] =  green
    matrix.write()
    sleep(delay)
    matrix[i] = (0,0,0)
# draw green up the matrix
for i in range(0, nm):
    matrix[i] =  blue
    matrix.write()
    sleep(delay)
    matrix[i] = (0,0,0)
