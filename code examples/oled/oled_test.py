from time import sleep  #importing sleep class
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C
import array # Needed for polygons
from ottodisplay import OttoOled
i2c = SoftI2C(sda=Pin(19), scl=Pin(18)) # Connector 1
oled = SSD1306_I2C(128, 64, i2c) # width, height using default address 0x3C

# draw another FrameBuffer on top of the current one at the given coordinates
import framebuf
fbuf = framebuf.FrameBuffer(bytearray(8 * 8 * 1), 8, 8, framebuf.MONO_VLSB)
fbuf.line(0, 0, 7, 7, 1)
oled.blit(fbuf, 10, 10, 0)           # draw on top at x=10, y=10, key=0
oled.show()

oled.fill(0)
oled.fill_rect(0, 0, 32, 32, 1)
oled.fill_rect(2, 2, 28, 28, 0)
oled.vline(9, 8, 22, 1)
oled.vline(16, 2, 22, 1)
oled.vline(23, 8, 22, 1)
oled.fill_rect(26, 24, 2, 4, 1)
oled.text('MicroPython', 40, 0, 1)
oled.text('SSD1306', 40, 12, 1)
oled.text('OLED 128x64', 40, 24, 1)
oled.show()  # write the contents of the FrameBuffer to oled memory
sleep(1)

oled.fill(0) # fill entire screen with colour=0 "clear"

def oled_eyesclosed():
    oled.rect(16,0,96,33,0,True)
    oled.rect(16,16,32,6,1,True)
    oled.rect(80,16,32,6,1,True)
  
def oled_eyes():
    oled.rect(16,0,96,33,0,True)
    oled.ellipse(32,16,16,16,1,1)  #left eye
    oled.ellipse(32,16,10,10,0,1)  #left eye -
    oled.ellipse(96,16,16,16,1,1)  #right eye
    oled.ellipse(96,16,10,10,0,1)  #right eye -

def oled_eyesup():
    oled_eyes()
    oled.rect(0,16,128,17,0,True)
    
def oled_eyesup2():
    oled.rect(16,0,96,33,0,True)
    oled.ellipse(32,32,16,16,1,1)  
    oled.ellipse(32,32,10,10,0,1)  
    oled.ellipse(96,32,16,16,1,1) 
    oled.ellipse(96,32,10,10,0,1)  
    oled.rect(0,32,128,17,0,True)
    
def oled_eyesdown():
    oled_eyes()
    oled.rect(0,0,128,16,0,True)
    
def oled_eyesdown2():
    oled.rect(16,0,97,33,0,True)
    oled.ellipse(32,0,16,16,1,1) 
    oled.ellipse(32,0,10,10,0,1) 
    oled.ellipse(96,0,16,16,1,1)  
    oled.ellipse(96,0,10,10,0,1)  
    
def oled_eyeswinkleft():
    oled_eyes()
    oled.rect(64,0,128,16,0,True)
    
def oled_eyeswinkright():
    oled_eyes()
    oled.rect(0,0,64,16,0,True)
    
def oled_eyesangry():
    oled_eyes()
    triangle1 = array.array('I', [16,0,48,0,48,32])
    oled.poly(0,0, triangle1, 0, True)
    triangle2 = array.array('I', [80,0,112,0,80,32])
    oled.poly(0,0, triangle2, 0, True) 
    
def oled_eyesworry():
    oled_eyes()
    triangle1 = array.array('I', [16,0,48,0,16,32])
    oled.poly(0,0, triangle1, 0, True) 
    triangle2 = array.array('I', [80,0,112,0,112,32])
    oled.poly(0,0, triangle2, 0, True) 

def oled_mouthclosed():
    oled.rect(32,32,64,32,0,True)
    oled.rect(32,42,64,6,1,True)

def oled_mouth():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,48,16,16,1,1) 
    oled.ellipse(64,48,10,10,0,1)
    
def oled_mouthup():
    oled_mouth()
    oled.rect(48,32,33,16,0,True)
    
def oled_mouthup2():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,32,16,16,1,1) 
    oled.ellipse(64,32,10,10,0,1)
    oled.rect(48,16,33,16,0,True)
    
def oled_mouthdown():
    oled_mouth()
    oled.rect(48,48,33,16,0,True)

def oled_mouthdown2():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,64,16,16,1,1) 
    oled.ellipse(64,64,10,10,0,1)
    
def oled_mouthleft():
    oled_mouthclosed()
    oled.ellipse(80,53,15,11,1,1)
    oled.rect(64,48,32,5,1,True)
    
def oled_mouthright():
    oled_mouthclosed()
    oled.ellipse(48,53,15,11,1,1)
    oled.rect(32,48,32,5,1,True)
    
def oled_mouthhappy():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,48,15,15,1,1)
    oled.rect(48,32,32,16,1,True)
    
def oled_mouthworry():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,48,15,10,1,1)

oled.fill(0)
oled_eyesclosed()
oled_mouthclosed()
oled.show()    
sleep(1)
oled_eyes()
oled_mouth()
oled.show()    
sleep(1)
oled_eyesup()
oled_mouthup2()
oled.show()    
sleep(1)
oled_eyesdown()
oled_mouthdown()
oled.show()    
sleep(1)
oled_eyesdown2()
oled_mouthdown2()
oled.show()    
sleep(1)
oled_eyeswinkleft()
oled_mouthleft()
oled.show()    
sleep(1)
oled_eyeswinkright()
oled_mouthright()
oled.show()    
sleep(1)
oled_eyesangry()
oled_mouthhappy()
oled.show()    
sleep(1)
oled_eyesworry()
oled_mouthworry()
oled.show()    
sleep(1)

oled.poweroff()     # power off the oled, pixels persist in memory
oled.poweron()      # power on the oled, pixels redrawn
oled.contrast(0)    # dim
oled.contrast(100)  # bright
#oled.rotate(True)  # rotate 180 degrees
#oled.rotate(False) # rotate 0 degrees
oled.fill(0)
#1. To print a string:
oled.text('Hello Otto ', 0, 0)
oled.text('World', 0, 20, 1)    # draw some text at x=0, y=20, colour=1
variable=5
oled.text("variable: {}".format(variable), 0, 30)
oled.scroll(20, 0)  # scroll 20 pixels to the right
#2. To display all the commands in queue:     
oled.show()         # write the contents of the FrameBuffer to oled memory
sleep(0.5)
#3. Now to clear the oled display:  
oled.fill(0)        # fill entire screen with colour=0
sleep(0.5)
#4. You may also use the invert function to invert the display.  
oled.invert(1) # oled inverted
sleep(0.5)
oled.invert(0) # oled normal
#5.To display a single pixel.
oled.pixel(0, 0)     # get pixel at x=0, y=0
oled.pixel(0, 10, 1) # set pixel at x=0, y=10 to color=1 "blue"
oled.show()
sleep(0.5)
#6. To display a horizontal line  
oled.hline(0, 5, 10, 1) # draw horizontal line x=0, y=5, width=10, colour=1
oled.show()
sleep(0.5)
#7. To display a vertical line  
oled.vline(0, 5, 10, 1) # draw vertical line x=0, y=5, height=10, colour=1
oled.show()
sleep(0.5)
#8. While hline and vline is quite useful, there is another function that is more flexible to use which is the line function.  
oled.line(0, 0, 128, 64, 1)          # draw a line from 0,0 to 128,64
oled.show()
sleep(0.5)
#9.We may also be able to print a rectangle.  
oled.rect(10, 10, 107, 43, 1)        # draw a rectangle outline 10,10 to 117,53, colour=1
# oled.rect(x,y,w,h,c,[f])
oled.rect(0,10,50,20,1)       # Outine
oled.rect(30,35,50,20,1,True) # Filled: True = 1 and False = 0
oled.show()
sleep(0.5)
#10. Or we may also print a filled rectangle:  
oled.fill_rect(0, 0, 128, 64, 1)   # draw a solid rectangle 10,10 to 128,64, colour=1
oled.show()
sleep(1)
# oled.ellipse(x,y,rx,ry,c,[f])
oled.fill(0) 
oled.ellipse(80,15,15,10,1)      # Outline
oled.ellipse(83,45,35,10,1,1)    # Filled
oled.ellipse(20,30,15,15,1,True) # Filled circle (rx = ry)
oled.ellipse(20,30,10,10,0)      # Outline circle (rx = ry)
oled.show()
sleep(0.5)
oled.fill(0) 
oled.ellipse(32,32,17,17,1,True) # Filled circle (rx = ry)
oled.ellipse(32,32,12,12,0,True) 
oled.ellipse(96,32,17,17,1,True) # Filled circle (rx = ry)
oled.ellipse(96,32,12,12,0,True)
oled.show()
sleep(0.5)
oled.fill(0) 
# oled.poly((x, y, coords, c,[f])
# First create an integer array of the coordinates
hexagon = array.array('I',[56,20, 72,20, 80,33, 72,47, 56,47, 48,33]) # 6 pairs
# Draw the polygon hexagon = array.array('I',[50,25, 64,18, 78,25, 78,42, 64,50, 50,42]) # 6 pairs
oled.poly(0,0, hexagon, 1, 1) # Filled hexagon
triangle = array.array('I', [64,22,74,39,54,39])
oled.poly(0,0, triangle, 0, True) # Filled
oled.show()
sleep(0.5)
oled.fill(0) 
triangle = array.array('I', [37,18,100,30,45,44])
oled.poly(0,0, triangle, 1, ) # Outline
oled.show()
sleep(0.5)
oled.fill(0) 
oled.text('1234567890', 0, 20) #oled.writeTextDisplay(" ", 0, 0)
oled.text("|@$&¡!¿?()[]{}", 0, 30)
oled.text("¬°#_+-*/=~<>^%", 0, 40)
oled.show()
sleep(3)

oled = OttoOled(19, 18) # Connector 1
#oled.pixelDisplay(1, 0, 1)
#oled.lineDisplay(0, 0, 128, 64)
#oled.squareDisplay(0, 0, 128, 64)
#oled.squareFillDisplay(0, 0, 128, 64,1)
#oled.ringDisplay(64, 32, 32)
#oled.circleDisplay(64, 32, 32)

oled.clearDisplay()
oled.Eyes1Draw()
oled.Mouth1Draw()
oled.showDisplay()
sleep(2)

oled.clearDisplay()
oled.Eyes2Draw()
oled.Mouth2Draw()
oled.showDisplay()
sleep(2)

oled.clearDisplay()
oled.Eyes3Draw()
oled.Mouth3Draw()
oled.showDisplay()
sleep(2)

oled.clearDisplay()
oled.Eyes4Draw()
oled.Mouth4Draw()
oled.showDisplay()
sleep(2)

oled.clearDisplay()
oled.Eyes5Draw()
oled.Mouth5Draw()
oled.showDisplay()
sleep(2)

oled.clearDisplay()
oled.Eyes6Draw()
oled.Mouth6Draw()
oled.showDisplay()
