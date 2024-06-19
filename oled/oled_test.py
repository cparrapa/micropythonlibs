import machine, time                   #importing machine and time libraries
from time import sleep                     #importing sleep class
from ottooled import OttoOled
from ssd1306 import SSD1306_I2C 
from machine import Pin, I2C
import array # Needed for polygons

i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

# #1. To print a string:  
oled.text('Hello Otto world', 0, 0)
# #2. To display all the commands in queue:     
oled.show()
time.sleep(1)
# #3. Now to clear the oled display:  
oled.fill(0) 
oled.show()
time.sleep(0.5)
# #4. You may also use the invert function to invert the display.  
oled.invert(1)
time.sleep(0.5)
oled.invert(0)
# #5.To display a single pixel.
oled.pixel(5,5,1)
oled.show()
time.sleep(0.5)
# #6. To display a horizontal line  
oled.hline(5,5,50,1) 
oled.show()
time.sleep(0.5)
# #7. To display a vertical line  
oled.vline(5,5,50,1) 
oled.show()
time.sleep(0.5)
# #8. While hline and vline is quite useful, there is another function that is more flexible to use which is the line function.  
oled.line(5,5,50,50,1) 
oled.show()
time.sleep(0.5)
# #9.We may also be able to print a rectangle.  
oled.rect(5,5,50,50,1) 
oled.show()
time.sleep(0.5)
# #10. Or we may also print a filled rectangle:  
oled.fill_rect(5,5,50,25,1) 
oled.show()
time.sleep(1)
# oled.rect(x,y,w,h,c,[f])
oled.fill(0) 
oled.rect(0,10,50,20,1)       # Outine
#oled.rect(30,35,50,20,1,True) # Filled: True = 1 and False = 0
oled.show()
time.sleep(0.5)
# oled.ellipse(x,y,rx,ry,c,[f])
oled.fill(0) 
oled.ellipse(80,15,15,10,1)      # Outline
oled.ellipse(83,45,35,10,1,1)    # Filled
oled.ellipse(20,30,15,15,1,True) # Filled circle (rx = ry)
oled.ellipse(20,30,10,10,0)      # Outline circle (rx = ry)
oled.show()
time.sleep(0.5)
oled.fill(0) 
oled.ellipse(32,32,17,17,1,True) # Filled circle (rx = ry)
oled.ellipse(32,32,12,12,0,True) 
oled.ellipse(96,32,17,17,1,True) # Filled circle (rx = ry)
oled.ellipse(96,32,12,12,0,True)
oled.show()
time.sleep(0.5)
oled.fill(0) 
# oled.poly((x, y, coords, c,[f])
# First create an integer array of the coordinates
hexagon = array.array('I',[56,20, 72,20, 80,33, 72,47, 56,47, 48,33]) # 6 pairs
# Draw the polygon hexagon = array.array('I',[50,25, 64,18, 78,25, 78,42, 64,50, 50,42]) # 6 pairs
oled.poly(0,0, hexagon, 1, 1) # Filled hexagon
triangle = array.array('I', [64,22,74,39,54,39])
oled.poly(0,0, triangle, 0, True) # Filled
oled.show()
time.sleep(2)
oled.fill(0) 
triangle = array.array('I', [37,18,100,30,45,44])
oled.poly(0,0, triangle, 1, ) # Outline
oled.show()
time.sleep(1)

oled = OttoOled(21, 22)
oled.clearDisplay()
oled.writeTextDisplay("1234567890", 0, 20)
oled.showDisplay()
time.sleep(1)
oled.writeTextDisplay("|@$&¡!¿?()[]{}", 0, 30)
oled.showDisplay()
time.sleep(1)
oled.writeTextDisplay("¬°#_+-*/=~<>^%", 0, 40)
oled.showDisplay()
time.sleep(1)
oled.clearDisplay()
oled.pixelDisplay(1, 0, 1)
oled.showDisplay()
time.sleep(0.5)
oled.clearDisplay()
oled.lineDisplay(0, 0, 128, 64)
oled.showDisplay()
time.sleep(0.5)
oled.clearDisplay()
oled.squareDisplay(0, 0, 128, 64)
oled.showDisplay()
time.sleep(0.5)
oled.squareFillDisplay(0, 0, 128, 64,1)
oled.showDisplay()
time.sleep(0.5)
oled.clearDisplay()
oled.ringDisplay(64, 32, 32)
oled.showDisplay()
time.sleep(0.5)
oled.clearDisplay()
oled.circleDisplay(64, 32, 32)
oled.showDisplay()
time.sleep(0.5)

oled.clearDisplay()
oled.Eyes1Draw()
oled.Mouth1Draw()
oled.showDisplay()
time.sleep(1)

oled.clearDisplay()
oled.Eyes1Draw()
oled.Mouth1Draw()
oled.showDisplay()
time.sleep(1)

oled.clearDisplay()
oled.Eyes2Draw()
oled.Mouth2Draw()
oled.showDisplay()
time.sleep(1)

oled.clearDisplay()
oled.Eyes3Draw()
oled.Mouth3Draw()
oled.showDisplay()
time.sleep(1)

oled.clearDisplay()
oled.Eyes4Draw()
oled.Mouth4Draw()
oled.showDisplay()
time.sleep(1)

oled.clearDisplay()
oled.Eyes5Draw()
oled.Mouth5Draw()
oled.showDisplay()
time.sleep(1)

oled.clearDisplay()
oled.Eyes6Draw()
oled.Mouth6Draw()
oled.showDisplay()
time.sleep(1)
