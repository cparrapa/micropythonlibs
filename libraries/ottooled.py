# ottooled v2.0 10.07.2024
import math, framebuf
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

class OttoOled:
    
    def __init__(self, sda, scl):
        self.i2c = I2C(sda=Pin(sda), scl=Pin(scl))
        self.display = SSD1306_I2C(128, 64, self.i2c)
            
    def writeTextDisplay(self, writeValue, xPos,  yPos):
        self.display.text("{}".format(writeValue), xPos, yPos, 1)
        
    def pixelDisplay(self, xPos,  yPos, value):
        self.display.pixel(xPos,  yPos, value)
    
    def lineDisplay(self, xPos1, yPos1, xPos2, yPos2):
        self.display.line(xPos1, yPos1, xPos2, yPos2, 1)
        
    def squareDisplay(self, xPos , yPos , width, height):
        self.display.rect(xPos , yPos , width, height, 1)
        
    def squareBlackDisplay(self, xPos , yPos , width, height):
        self.display.rect(xPos , yPos , width, height, 0)
        
    def squareFillDisplay(self, xPos , yPos , width, height,value):
        self.display.fill_rect(xPos , yPos , width, height, value)

    def drawCircle(self, x, y, r, color):
        self.display.ellipse(x,y,r,r,color,1)
    
    def circleDisplay(self, x, y, r):
        self.drawCircle(x, y, r, 1)
    
    def circleBlackDisplay(self, x, y, r):
        self.drawCircle(x, y, r, 0)
        
    def ringDisplay(self, x, y, r):
        self.display.ellipse(x,y,r,r,1,0)

    def Draw2Eyes(self):
        self.circleDisplay(30, 17, 17)
        self.circleBlackDisplay(30, 14, 10)
        self.circleDisplay(98, 17, 17)
        self.circleBlackDisplay(98, 14, 10)
    
    def Eyes1Draw(self):
        self.circleDisplay(30, 17, 17)
        self.circleBlackDisplay(30, 14, 10)
        self.circleDisplay(98, 17, 17)
        self.circleBlackDisplay(98, 14, 10)
        
    def Eyes2Draw(self):
        self.Draw2Eyes()
        self.display.fill_rect(0, 17, 128, 17, 0)
    
    def Eyes3Draw(self):
        self.Draw2Eyes()
        self.display.fill_rect(0, 0, 128, 17, 0)
        
    def Eyes4Draw(self):
        self.Draw2Eyes()
        self.display.fill_rect(0, 0, 64, 17, 0)
        
    def Eyes5Draw(self):
        self.Draw2Eyes()
        self.display.fill_rect(0, 0, 36, 17, 0)
        self.display.fill_rect(92, 0, 36, 20, 0)
    
    def Eyes6Draw(self):
        self.Draw2Eyes()
        self.display.fill_rect(24, 0, 74, 20, 0)
        
    def Mouth1Draw(self):
        self.circleDisplay(64, 50, 14)
        self.circleBlackDisplay(64, 50, 10)
        self.display.fill_rect(0, 36, 128, 14, 0)
    
    def Mouth2Draw(self):
        self.circleDisplay(64, 50, 14)
        
    def Mouth3Draw(self):
        self.circleDisplay(64, 60, 20)
    
    def Mouth4Draw(self):
        self.display.fill_rect(39, 54, 50, 7, 1)
   
    def Mouth5Draw(self):
        self.display.fill_rect(44, 44, 50, 7, 1)
        self.circleDisplay(84, 54, 10)

    def Mouth6Draw(self):
        self.display.fill_rect(44, 44, 50, 7, 1)
        self.circleDisplay(53, 54, 10)
        
    def showDisplay(self):
        self.display.show()
        
    def clearDisplay(self):
        self.display.fill(0)
        self.display.show()
        
    def ShowIcon(self,icono,x,y,w,h):
        fb = framebuf.FrameBuffer(icono,w,h, framebuf.MONO_HLSB)
        self.display.blit(fb, x, y)