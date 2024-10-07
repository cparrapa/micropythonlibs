import time, machine, neopixel
from time import sleep, sleep_ms
from machine import Pin, reset
from neopixel import NeoPixel

class RGB_Matrix:
    
    def __init__(self, gpio, width, height):
        self.width = width
        self.height = height
        self.neopixel = NeoPixel(Pin(gpio), width*height)
        
    def pixel_set(self, row, col, r=0, g=0, b=0, color=''):
        if color == '': 
            self.neopixel[col + (row*self.width)] = (r, g, b)
            self.neopixel.write()
        else:
            self.neopixel[col + (row*self.width)] = self.color
            self.neopixel.write()
            
    def pixel_clr(self, row, col):
        self.neopixel[col + (row*self.width)] = (0, 0, 0)
        self.neopixel.write()
        
    def clear_all(self):
        self.neopixel.fill((0,0,0))
        self.neopixel.write()

matrix = RGB_Matrix(16, 8, 8) # Connector 2, 8x8 =64

matrix.pixel_set(0,0,255,0,0) # draw a red pixel at the top left corner
matrix.pixel_set(7,0,0,255,0) # draw a green pixel at the lower left corner
matrix.pixel_set(0,7,0,0,255) # draw a blue pixel at the top right corner
#matrix.clear_all()
matrix.pixel_clr(7,7)
matrix.pixel_set(7,7,255,255,255) # draw a white pixel at the lower right corner
