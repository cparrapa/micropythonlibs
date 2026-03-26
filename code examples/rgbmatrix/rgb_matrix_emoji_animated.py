# v0 02/09/2024   Alex Etchells
# A class for drawing icons on the 8x8 RGB matrix
#Current Icons:
#0       smile
#1       heart
#2       beer
#3       poop
#4       skull
#5       halloween
#6       otto_diy
#7       hp_otto
#8       bender
#9       dog
#11      cat

import time                       #importing machine and time libraries
from machine import Pin, ADC, PWM #importing Pin, ADC and PWM classes
from ottoneopixel import OttoRGBMatrix

class OttoRGBMatrixIcon:
    def __init__(self, connector = 0):
        connectorPin = [None,18,16,22] #GPIO pins for the 4pin connectors (1 to 3)
        brightm = 0.5 # brightness variable for lights
        nm = 64       # total number of pixels in the self.matrix
   
        self.matrix = OttoRGBMatrix(connectorPin[connector], nm)        # Connector 3
        self.matrix.setBrightness(brightm)
        self.blankScreen()
        self.matrix.pixels.write()
        #self.icons = ["smile","heart","beer","poop","skull","halloween","otto_diy","hp_otto","bender","dog,"cat"]
        icoList = "smile,heart,beer,poop,skull,halloween,otto_diy,hp_otto,bender,dog,cat"
        self.icons = [icoName for icoName in icoList.split(',')]
   
   
    def showIconByNumber(self, iconNo):
        if iconNo < 0 or iconNo > len(self.icons) - 1:
            return
        self.showIcon(self.icons[iconNo])
    
    def showIcon(self, iconName):
        if iconName == 'smile':
            self.icon_smile()
        elif iconName == 'heart':
            self.icon_heart()
        elif iconName == 'beer':
            self.icon_beer()
        elif iconName == 'poop':
            self.icon_poop()
        elif iconName == 'skull':
            self.icon_skull()
        elif iconName == 'halloween':
            self.icon_halloween()
        elif iconName == 'otto_diy':
            self.icon_ottodiy()
        elif iconName == 'hp_otto':
            self.icon_hpotto()
        elif iconName == 'bender':
            self.icon_bender()
        elif iconName == 'dog':
            self.icon_dog()
        elif iconName == 'cat':
            self.icon_cat()

    def blankScreen(self):
        bk= (0,0,0)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(3,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(4,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(7,row)



    def icon_smile(self):
        bk = (0,0,0)
        wt = (255,255,255)
        yl = ( 255, 255, 0)
        #1
        row = [bk,bk,yl,yl,yl,yl,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,yl,yl,yl,yl,yl,yl,bk]
        self.matrix.setMatrixRow(1,row)
        row = [yl,yl,bk,wt,yl,bk,wt,yl]
        self.matrix.setMatrixRow(2,row)
        row = [yl,yl,wt,wt,yl,wt,wt,yl]
        self.matrix.setMatrixRow(3,row)
        row = [yl,yl,yl,yl,yl,yl,yl,yl]
        self.matrix.setMatrixRow(4,row)
        row = [yl,yl,yl,yl,yl,yl,yl,yl]
        self.matrix.setMatrixRow(5,row)
        row = [bk,yl,yl,bk,bk,yl,yl,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,yl,yl,yl,yl,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #2
        row = [bk,yl,bk,bk,bk,bk,yl,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #3
        row = [yl,bk,yl,yl,yl,yl,bk,yl]
        self.matrix.setMatrixRow(5,row,True)
        time.sleep(0.5)
        #4
        row = [yl,yl,bk,wt,yl,yl,yl,yl]
        self.matrix.setMatrixRow(2,row)
        row = [yl,yl,wt,wt,yl,yl,yl,yl]
        self.matrix.setMatrixRow(3,row,True)
        time.sleep(0.2)
        #5
        row = [yl,yl,bk,wt,yl,bk,wt,yl]
        self.matrix.setMatrixRow(2,row)
        row = [yl,yl,wt,wt,yl,wt,wt,yl]
        self.matrix.setMatrixRow(3,row,True)
        time.sleep(0.5)
        
    def icon_heart(self):    
        self.blankScreen()
        bk = (0,0,0)
        r1 = (80,0,0)
        r2 = (160,0,0)
        r3 = (180,0,0)
        r4 = [230,0,0]
        r5 = [255,0,0]
        #1
        row = [bk,bk,bk,r1,r1,bk,bk,bk]
        self.matrix.setMatrixRow(3,row)
        self.matrix.setMatrixRow(4,row,True)
        time.sleep(0.1)
        #2
        row = [bk,bk,bk,r1,r1,bk,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,r1,r2,r2,r1,bk,bk]
        self.matrix.setMatrixRow(3,row)
        self.matrix.setMatrixRow(4,row)
        row = [bk,bk,bk,r1,r1,bk,bk,bk]
        self.matrix.setMatrixRow(5,row,True)
        time.sleep(0.1)
        #3
        row = [bk,r1,r1,r1,r1,r1,r1,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,r1,r1,r2,r2,r1,r1,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,r1,r2,r3,r3,r2,r1,bk]
        self.matrix.setMatrixRow(3,row)
        row = [bk,r1,r1,r2,r2,r1,r1,bk]
        self.matrix.setMatrixRow(4,row)
        row = [bk,bk,r1,r1,r1,r1,bk,bk]
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,bk,r1,r1,bk,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #4
        row = [bk,r1,r1,bk,bk,r1,r1,bk]
        self.matrix.setMatrixRow(0,row)
        row = [r1,r1,r1,r1,r1,r1,r1,r1]
        self.matrix.setMatrixRow(1,row)
        row = [r1,r2,r3,r2,r2,r3,r2,r1]
        self.matrix.setMatrixRow(2,row)
        row = [r1,r2,r4,r4,r4,r4,r2,r1]
        self.matrix.setMatrixRow(3,row)
        row = [r1,r1,r2,r4,r4,r2,r1,r1]
        self.matrix.setMatrixRow(4,row)
        row = [bk,r1,r1,r2,r2,r1,r1,bk]
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,r1,r1,r1,r1,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,r1,r1,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.1)
        #5
        row = [r1,r3,r3,r1,r1,r3,r3,r1]
        self.matrix.setMatrixRow(1,row)        
        row = [r1,r4,r5,r5,r5,r5,r4,r1]
        self.matrix.setMatrixRow(2,row)     
        row = [r1,r4,r5,r5,r5,r5,r4,r1]
        self.matrix.setMatrixRow(3,row)
        row = [r1,r3,r4,r5,r5,r4,r3,r1]
        self.matrix.setMatrixRow(4,row)
        row = [bk,r1,r3,r4,r4,r3,r1,bk]
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,r1,r3,r3,r1,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #6
        row = [bk,r3,r3,bk,bk,r3,r3,bk]
        self.matrix.setMatrixRow(0,row)
        row = [r3,r4,r4,r3,r3,r4,r4,r3]
        self.matrix.setMatrixRow(1,row)     
        row = [r3,r5,r5,r5,r5,r5,r5,r3]
        self.matrix.setMatrixRow(2,row)      
        row = [r3,r5,r5,r5,r5,r5,r5,r3]
        self.matrix.setMatrixRow(3,row)         
        row = [r3,r4,r5,r5,r5,r5,r4,r3]
        self.matrix.setMatrixRow(4,row)               
        row = [bk,r3,r4,r5,r5,r4,r3,bk]
        self.matrix.setMatrixRow(5,row)   
        row = [bk,bk,r3,r4,r4,r3,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,r3,r3,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.2)
        #7
        row = [bk,r5,r5,bk,bk,r5,r5,bk]
        self.matrix.setMatrixRow(0,row)
        row = [r5,r5,r5,r5,r5,r5,r5,r5]
        self.matrix.setMatrixRow(1,row)     
        row = [r5,r5,r5,r5,r5,r5,r5,r5]
        self.matrix.setMatrixRow(2,row)      
        row = [r5,r5,r5,r5,r5,r5,r5,r5]
        self.matrix.setMatrixRow(3,row)         
        row = [r5,r5,r5,r5,r5,r5,r5,r5]
        self.matrix.setMatrixRow(4,row)               
        row = [bk,r5,r5,r5,r5,r5,r5,bk]
        self.matrix.setMatrixRow(5,row)   
        row = [bk,bk,r5,r5,r5,r5,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,r5,r5,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)

    def icon_beer(self):
        bk = (0,0,0)
        wt = (255,255,255)
        y1 = (248,243,192)
        t1 = (255,198,56)
        y2 = (249,255,27)
        b1 = (176,126,0)
        t2 = (246,176,0)
        g1 = (214,255,221)
        b2= (147,105,0)
        y3 = (255,238,32)
        y4 = (255,220,32)
        b3 = (211,151,0)
        y5 = (234,198,0)


        row = [bk,bk,y1,wt,y1,y1,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,wt,wt,wt,y1,wt,wt,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,y1,t1,y2,wt,b1,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,t1,y2,t2,b1,g1,g1]
        self.matrix.setMatrixRow(3,row)
        row = [bk,bk,t1,y3,t2,b1,bk,wt]
        self.matrix.setMatrixRow(4,row)
        row = [bk,bk,t1,y4,t2,b2,bk,wt]
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,b3,y5,b3,b2,g1,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,wt,wt,g1,g1,bk,bk]
        self.matrix.setMatrixRow(7,row,True)

    def icon_poop(self):
        bk = (0,0,0)
        wt = (255,255,255)
        br = (95,55,5)
        #1
        row = [bk,bk,br,br,bk,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,br,br,br,br,br,bk,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,br,wt,br,wt,br,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row = [br,br,bk,br,bk,br,br,bk]
        self.matrix.setMatrixRow(3,row)
        row = [br,br,br,br,br,br,br,bk]
        self.matrix.setMatrixRow(4,row)
        row = [br,br,br,bk,br,br,br,br]
        self.matrix.setMatrixRow(5,row)
        row = [br,br,br,br,br,br,br,br]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #2
        row = [bk,bk,bk,br,br,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,bk,br,br,br,br,br,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,bk,br,wt,br,wt,br,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,br,br,bk,br,bk,br,br]
        self.matrix.setMatrixRow(3,row)
        row = [bk,br,br,br,br,br,br,br]
        self.matrix.setMatrixRow(4,row)
        row = [br,br,br,br,bk,br,br,br]
        self.matrix.setMatrixRow(5,row,True)
        time.sleep(0.5)
        #3
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,bk,bk,br,br,bk,bk,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,bk,br,br,br,br,br,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,br,wt,br,wt,br,bk]
        self.matrix.setMatrixRow(3,row)
        row = [bk,br,br,bk,br,bk,br,br]
        self.matrix.setMatrixRow(4,row)
        row = [bk,br,br,br,br,br,br,br]
        self.matrix.setMatrixRow(5,row)
        row = [br,br,br,bk,bk,bk,br,br]
        self.matrix.setMatrixRow(6,row)
        row = [br,br,br,br,br,br,br,br]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #4
        row = [bk,bk,br,br,bk,bk,bk,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,br,br,br,br,br,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,br,wt,br,wt,br,bk,bk]
        self.matrix.setMatrixRow(3,row)
        row = [br,br,bk,br,bk,br,bk,bk]
        self.matrix.setMatrixRow(4,row)
        row = [br,br,br,br,br,br,br,bk]
        self.matrix.setMatrixRow(5,row)
        row = [br,br,bk,bk,bk,br,br,br]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.5)        
    
    def icon_skull(self):
        bk = (0,0,0)
        wt = (255,255,255)
        rd = (255,0,0)
        #1
        row = [bk,wt,wt,wt,wt,wt,wt,bk]
        self.matrix.setMatrixRow(0,row)
        row = [wt,bk,bk,wt,wt,bk,bk,wt]
        self.matrix.setMatrixRow(1,row)
        row = [wt,bk,bk,wt,wt,bk,bk,wt]
        self.matrix.setMatrixRow(2,row)
        row = [wt,bk,rd,wt,wt,bk,rd,wt]
        self.matrix.setMatrixRow(3,row)
        row = [bk,wt,wt,bk,bk,wt,wt,bk]
        self.matrix.setMatrixRow(4,row)
        row = [bk,bk,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #2
        row = [wt,rd,bk,wt,wt,rd,bk,wt]
        self.matrix.setMatrixRow(3,row)
        row = [bk,bk,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #3
        row = [wt,rd,bk,wt,wt,rd,bk,wt]
        self.matrix.setMatrixRow(2,row)
        row = [wt,bk,bk,wt,wt,bk,bk,wt]
        self.matrix.setMatrixRow(3,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #4
        row = [wt,rd,bk,wt,wt,rd,bk,wt]
        self.matrix.setMatrixRow(1,row)
        row = [wt,bk,bk,wt,wt,bk,bk,wt]
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #5
        row = [wt,bk,rd,wt,wt,bk,rd,wt]
        self.matrix.setMatrixRow(1,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #6
        row = [wt,bk,bk,wt,wt,bk,bk,wt]
        self.matrix.setMatrixRow(1,row)
        row = [wt,bk,rd,wt,wt,bk,rd,wt]
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)        
  
    
    def icon_halloween(self):
        bk = (0,0,0)
        gn = (35,154,10)
        og = (240,122,18)
        yl = [232,223,5]
        #1
        row=[bk,bk,bk,gn,gn,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row=[bk,bk,bk,gn,bk,bk,bk,bk]
        self.matrix.setMatrixRow(1,row)
        row=[bk,og,og,og,og,og,og,bk]
        self.matrix.setMatrixRow(2,row)
        row=[og,og,bk,og,og,bk,og,og]
        self.matrix.setMatrixRow(3,row)
        row=[og,og,og,og,og,og,og,og]
        self.matrix.setMatrixRow(4,row)
        row=[og,bk,og,og,og,og,bk,og]
        self.matrix.setMatrixRow(5,row)
        row=[og,og,bk,bk,bk,bk,og,og]
        self.matrix.setMatrixRow(6,row)
        row=[bk,og,og,og,og,og,og,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)   
        #2  
        row=[og,og,yl,og,og,yl,og,og]
        self.matrix.setMatrixRow(3,row)   
        row=[og,yl,og,og,og,og,yl,og]
        self.matrix.setMatrixRow(5,row)
        row=[og,og,yl,yl,yl,yl,og,og]
        self.matrix.setMatrixRow(6,row,True) 
        time.sleep(0.1)
        #3
        row=[og,og,bk,og,og,bk,og,og]
        self.matrix.setMatrixRow(3,row)  
        row=[og,bk,og,og,og,og,bk,og]
        self.matrix.setMatrixRow(5,row)
        row=[og,og,bk,bk,bk,bk,og,og]
        self.matrix.setMatrixRow(6,row,True) 
    
    def icon_ottodiy(self):
        bk = (0,0,0)
        wt = (255,255,255)
        gn = (138,255,15)
        #1
        row = [bk,gn,gn,gn,gn,gn,bk,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(2,row)
        row = [bk,gn,bk,gn,bk,gn,bk,bk]
        self.matrix.setMatrixRow(1,row)        
        row = [bk,wt,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(3,row)
        self.matrix.setMatrixRow(4,row)      
        row = [bk,wt,wt,bk,wt,wt,bk,bk]
        self.matrix.setMatrixRow(5,row)
        self.matrix.setMatrixRow(6,row)   
        row = [wt,wt,wt,bk,wt,wt,wt,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #2
        row = [bk,bk,gn,gn,bk,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,gn,gn,bk,gn,bk,bk,bk]
        self.matrix.setMatrixRow(1,row)
        row = [gn,bk,gn,gn,wt,wt,bk,wt]
        self.matrix.setMatrixRow(2,row)
        row = [bk,gn,gn,wt,wt,wt,wt,wt]
        self.matrix.setMatrixRow(3,row)
        row = [bk,bk,wt,wt,wt,wt,wt,wt]
        self.matrix.setMatrixRow(4,row)
        row = [bk,bk,bk,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(5,row)
        self.matrix.setMatrixRow(7,row)
        row = [bk,bk,bk,bk,wt,wt,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.5)        
        #3
        row = [bk,bk,gn,gn,gn,gn,gn,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,gn,bk,gn,bk,gn,bk]
        self.matrix.setMatrixRow(1,row)        
        row = [bk,bk,wt,wt,wt,wt,wt,bk]
        self.matrix.setMatrixRow(3,row)
        self.matrix.setMatrixRow(4,row)      
        row = [bk,bk,wt,wt,bk,wt,wt,bk]
        self.matrix.setMatrixRow(5,row)
        self.matrix.setMatrixRow(6,row)   
        row = [bk,wt,wt,wt,bk,wt,wt,wt]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #4
        row = [bk,bk,bk,bk,gn,gn,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,bk,bk,gn,bk,gn,gn,bk]
        self.matrix.setMatrixRow(1,row)
        row = [wt,bk,wt,wt,gn,gn,bk,gn]
        self.matrix.setMatrixRow(2,row)
        row = [wt,wt,wt,wt,wt,gn,gn,bk]
        self.matrix.setMatrixRow(3,row)
        row = [wt,wt,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(4,row)
        row = [bk,bk,wt,wt,wt,bk,bk,bk]
        self.matrix.setMatrixRow(5,row)
        self.matrix.setMatrixRow(7,row)
        row = [bk,bk,wt,wt,bk,bk,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.5)        
        #5
        row = [bk,gn,gn,gn,gn,gn,bk,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(2,row)
        row = [bk,gn,bk,gn,bk,gn,bk,bk]
        self.matrix.setMatrixRow(1,row)        
        row = [bk,wt,wt,wt,wt,wt,bk,bk]
        self.matrix.setMatrixRow(3,row)
        self.matrix.setMatrixRow(4,row)      
        row = [bk,wt,wt,bk,wt,wt,bk,bk]
        self.matrix.setMatrixRow(5,row)
        self.matrix.setMatrixRow(6,row)   
        row = [wt,wt,wt,bk,wt,wt,wt,bk]
        self.matrix.setMatrixRow(7,row,True)        
    
    def icon_hpotto(self):
        bk = (0,0,0)
        gy = (204,204,204)
        bl = (73,189,254)
        #1
        row = [bk,gy,gy,gy,gy,gy,bk,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(3,row)
        row = [bk,bl,bk,bl,bk,bl,bk,bk]
        self.matrix.setMatrixRow(1,row) 
        row = [bk,bl,bl,bl,bl,bl,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bl,gy,gy,gy,gy,gy,bl,bk]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bl,bk,bk,gy,bk,bk,bl,bk]
        self.matrix.setMatrixRow(6,row) 
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.5)
        #2
        row = [bk,gy,gy,gy,gy,gy,gy,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(3,row)
        row = [bk,bl,bl,bl,bl,bk,bl,bk]
        self.matrix.setMatrixRow(1,row) 
        row = [bk,bl,bl,bl,bl,bl,bl,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bl,bl,bl,gy,gy,gy,gy,bk]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bl,bl,bl,bk,bl,gy,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #3
        row = [bk,bk,gy,gy,gy,gy,gy,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(3,row)
        row = [bk,bk,bl,bl,bl,bl,bk,bk]
        self.matrix.setMatrixRow(1,row) 
        row = [bk,bk,bl,bl,bl,bl,bl,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,bk,bl,bl,bl,gy,gy,bk]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,bl,bl,bl,bk,gy,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #4
        row = [bk,bk,bl,bl,bl,bl,bl,bk]
        self.matrix.setMatrixRow(1,row) 
        row = [bk,bk,gy,bl,bl,bl,gy,bk]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,bk,bl,bl,bl,gy,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #5
        row = [bk,bl,gy,gy,gy,gy,gy,bl]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bk,bl,bk,bk,gy,bk,bk,bl]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #6
        row = [bk,gy,gy,gy,gy,gy,bk,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(3,row)
        row = [bk,bl,bl,bl,bl,bl,bk,bk]
        self.matrix.setMatrixRow(1,row) 
        self.matrix.setMatrixRow(2,row)
        row = [bk,gy,bl,bl,bl,gy,bk,bk]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bk,gy,bl,bl,bl,bk,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #7
        row = [bk,bk,bl,bl,bl,bl,bk,bk]
        self.matrix.setMatrixRow(1,row) 
        row = [bk,gy,gy,bl,bl,bl,bk,bk]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bk,gy,bk,bl,bl,bl,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #8
        row = [bk,gy,gy,gy,gy,gy,gy,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(3,row)
        row = [bk,bl,bk,bl,bl,bl,bl,bk]
        self.matrix.setMatrixRow(1,row) 
        row = [bk,bl,bl,bl,bl,bl,bl,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,gy,gy,gy,gy,bl,bl,bl]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,gy,bl,bk,bl,bl,bl]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.1)
        #9
        row = [bk,gy,gy,gy,gy,gy,bk,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(3,row)
        row = [bk,bl,bk,bl,bk,bl,bk,bk]
        self.matrix.setMatrixRow(1,row) 
        row = [bk,bl,bl,bl,bl,bl,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bl,gy,gy,gy,gy,gy,bl,bk]
        self.matrix.setMatrixRow(4,row)  
        self.matrix.setMatrixRow(5,row)
        row = [bl,bk,bk,gy,bk,bk,bl,bk]
        self.matrix.setMatrixRow(6,row,True)
        
    def icon_bender(self):
        bk = (0,0,0)
        g1 = (65,65,65)
        g2 = (160,160,160)
        g3 = (186,186,186)
        yl = (255,248,0)
        gn = (49,255,0)
        #1
        row = [bk,bk,bk,g2,g1,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        self.matrix.setMatrixRow(1,row)
        row_1_0 = row
        row = [bk,bk,g3,g2,g2,g1,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row_1_2 = row
        row = [bk,g3,g2,g2,g2,g2,g1,bk]
        self.matrix.setMatrixRow(3,row)
        row_1_3 = row
        row = [g3,g2,g2,g2,g2,g2,g2,g1]
        self.matrix.setMatrixRow(4,row)
        self.matrix.setMatrixRow(7,row)
        row_1_4 = row
        row = [g3,yl,yl,g2,g2,yl,yl,g1]
        self.matrix.setMatrixRow(5,row)
        row_1_5 = row
        row = [g3,yl,bk,g2,g2,yl,bk,g1]
        self.matrix.setMatrixRow(6,row,True)
        row_1_6 = row
        time.sleep(0.8)
        #2
        row = [g3,bk,yl,g2,g2,bk,yl,g1]
        self.matrix.setMatrixRow(6,row,True)
        row_2_6 = row
        time.sleep(0.8)
        #3
        self.matrix.setMatrixRow(2,row_1_0)
        self.matrix.setMatrixRow(3,row_1_2)
        self.matrix.setMatrixRow(4,row_1_3)
        self.matrix.setMatrixRow(5,row_1_4)
        self.matrix.setMatrixRow(6,row_1_5)
        self.matrix.setMatrixRow(7,row_1_6,True)
        time.sleep(0.2)
        #4
        row = [bk,bk,bk,bk,bk,bk,bk,bk]
        self.matrix.setMatrixRow(0,row)
        row_blk = row
        self.matrix.setMatrixRow(3,row_1_0)
        self.matrix.setMatrixRow(4,row_1_2)
        self.matrix.setMatrixRow(5,row_1_3)
        self.matrix.setMatrixRow(6,row_1_4)
        self.matrix.setMatrixRow(7,row_1_5,True)
        time.sleep(0.2)
        #5
        self.matrix.setMatrixRow(1,row_blk)
        self.matrix.setMatrixRow(4,row_1_0)
        self.matrix.setMatrixRow(5,row_1_2)
        self.matrix.setMatrixRow(6,row_1_3)
        self.matrix.setMatrixRow(7,row_1_4,True)
        time.sleep(0.2)
        #6
        self.matrix.setMatrixRow(2,row_blk)
        self.matrix.setMatrixRow(5,row_1_0)
        self.matrix.setMatrixRow(6,row_1_2)
        self.matrix.setMatrixRow(7,row_1_3,True)
        time.sleep(0.3)
        #7
        self.matrix.setMatrixRow(3,row_blk)
        self.matrix.setMatrixRow(6,row_1_0)
        self.matrix.setMatrixRow(7,row_1_2,True)
        time.sleep(0.3)
        #8
        row = [bk,bk,bk,gn,gn,bk,bk,bk]
        self.matrix.setMatrixRow(3,row)
        row_8_3 = row        
        row = [bk,bk,gn,g2,g1,gn,bk,bk]
        self.matrix.setMatrixRow(4,row,True)
        row_8_4 = row        
        time.sleep(0.2)
        #9
        row = [bk,bk,gn,gn,gn,gn,bk,bk]
        self.matrix.setMatrixRow(2,row)
        row_9_2 = row
        row = [bk,gn,bk,bk,bk,bk,gn,bk]
        self.matrix.setMatrixRow(3,row)
        row_9_3 = row
        row = [gn,bk,bk,g2,g1,bk,bk,gn]
        self.matrix.setMatrixRow(4,row,True)
        row_9_4 = row     
        time.sleep(0.2)
        #10
        self.matrix.setMatrixRow(1,row_9_2)
        self.matrix.setMatrixRow(2,row_9_3)
        row = [gn,bk,bk,bk,bk,bk,bk,gn]
        self.matrix.setMatrixRow(3,row)
        row_10_3 = row
        self.matrix.setMatrixRow(4,row_1_0,True)
        time.sleep(0.2)
        #11        
        self.matrix.setMatrixRow(0,row_9_2)
        self.matrix.setMatrixRow(1,row_9_3)
        self.matrix.setMatrixRow(2,row_10_3)
        self.matrix.setMatrixRow(3,row_8_3)
        self.matrix.setMatrixRow(4,row_8_4,True)
        time.sleep(0.2)
        #12
        self.matrix.setMatrixRow(0,row_9_3)
        self.matrix.setMatrixRow(1,row_10_3)
        self.matrix.setMatrixRow(2,row_8_3)
        row = [bk,bk,gn,bk,bk,gn,bk,bk]
        self.matrix.setMatrixRow(3,row)
        row_12_3 = row
        self.matrix.setMatrixRow(4,row_1_0,True)
        time.sleep(0.2)
        #13        
        row = [gn,bk,bk,gn,gn,bk,bk,gn]
        self.matrix.setMatrixRow(1,row)
        #row_13_1 = row
        self.matrix.setMatrixRow(2,row_12_3)
        self.matrix.setMatrixRow(3,row_9_3,True)
        time.sleep(0.2)
        #14
        self.matrix.setMatrixRow(0,row_blk)
        self.matrix.setMatrixRow(1,row_9_2)
        self.matrix.setMatrixRow(2,row_9_3)
        self.matrix.setMatrixRow(3,row_10_3,True)
        time.sleep(0.1)
        #15   
        self.matrix.setMatrixRow(0,row_9_2)
        self.matrix.setMatrixRow(1,row_9_3)
        self.matrix.setMatrixRow(2,row_10_3)
        self.matrix.setMatrixRow(3,row_blk,True)
        time.sleep(0.2)
        #16
        self.matrix.setMatrixRow(0,row_9_3)
        self.matrix.setMatrixRow(1,row_10_3)
        self.matrix.setMatrixRow(2,row_blk,True)
        time.sleep(0.2)
        #17
        self.matrix.setMatrixRow(0,row_blk,True)
        self.matrix.setMatrixRow(1,row_blk,True)
        time.sleep(0.5)
        #18
        self.matrix.setMatrixRow(3,row_1_0)
        self.matrix.setMatrixRow(6,row_1_2)
        self.matrix.setMatrixRow(7,row_1_3,True)
        time.sleep(0.3)
        #19
        self.matrix.setMatrixRow(2,row_1_0)
        self.matrix.setMatrixRow(5,row_1_2)
        self.matrix.setMatrixRow(6,row_1_3)
        self.matrix.setMatrixRow(7,row_1_4,True)
        time.sleep(0.3)
        #20
        self.matrix.setMatrixRow(1,row_1_0)
        self.matrix.setMatrixRow(4,row_1_2)
        self.matrix.setMatrixRow(5,row_1_3)
        self.matrix.setMatrixRow(6,row_1_4)
        self.matrix.setMatrixRow(7,row_1_5,True)
        time.sleep(0.3)
        #21
        self.matrix.setMatrixRow(0,row_1_0)
        self.matrix.setMatrixRow(3,row_1_2)
        self.matrix.setMatrixRow(4,row_1_3)
        self.matrix.setMatrixRow(5,row_1_4)
        self.matrix.setMatrixRow(6,row_1_5)
        self.matrix.setMatrixRow(7,row_2_6,True)
        time.sleep(0.2)
        #22
        self.matrix.setMatrixRow(2,row_1_2)
        self.matrix.setMatrixRow(3,row_1_3)
        self.matrix.setMatrixRow(4,row_1_4)
        self.matrix.setMatrixRow(5,row_1_5)
        self.matrix.setMatrixRow(6,row_2_6)
        self.matrix.setMatrixRow(7,row_1_4,True)
        time.sleep(0.2)
        
    def icon_dog(self):
        #uses columns for horizontal scrolling
        bk = (0,0,0)
        b1 = (255,179,0)
        b2 = (95,55,5)       
        col_blk = [bk,bk,bk,bk,bk,bk,bk,bk]
        #1
        col = [bk,bk,b1,b1,bk,bk,bk,b2]
        self.matrix.setMatrixCol(0,col)
        col_1_0 = col
        self.matrix.setMatrixCol(1,col_blk)
        self.matrix.setMatrixCol(2,col_blk)
        self.matrix.setMatrixCol(3,col_blk)
        self.matrix.setMatrixCol(4,col_blk)
        self.matrix.setMatrixCol(5,col_blk)
        self.matrix.setMatrixCol(6,col_blk)
        self.matrix.setMatrixCol(7,col_blk,True)
        time.sleep(0.3)
        #2
        col = [bk,bk,b1,b1,bk,bk,b1,bk]
        self.matrix.setMatrixCol(0,col)
        col_2_0 = col
        col = [bk,bk,b1,b1,bk,bk,bk,b1]
        self.matrix.setMatrixCol(1,col,True)
        col_2_1 = col
        time.sleep(0.3)
        #3
        col = [bk,b1,b1,b1,b1,b1,b1,b1]
        self.matrix.setMatrixCol(0,col)
        col_3_0 = col
        col = [bk,bk,b1,b1,bk,bk,b2,bk]
        self.matrix.setMatrixCol(1,col)
        col_3_1 = col
        self.matrix.setMatrixCol(2,col_1_0,True)
        time.sleep(0.3)
        #4
        col = [bk,bk,bk,bk,b1,b1,bk,bk]
        self.matrix.setMatrixCol(0,col)
        col_4_0 = col
        col = [bk,b1,b1,b1,b1,b1,b2,b2]
        self.matrix.setMatrixCol(1,col)
        col_4_1 = col
        self.matrix.setMatrixCol(2,col_2_0)
        self.matrix.setMatrixCol(3,col_2_1,True)
        time.sleep(0.3)
        #5
        col = [bk,bk,bk,bk,b1,b1,bk,b2]
        self.matrix.setMatrixCol(0,col)
        col_5_0 = col
        self.matrix.setMatrixCol(1,col_4_0)
        self.matrix.setMatrixCol(2,col_3_0)
        self.matrix.setMatrixCol(3,col_3_1)
        self.matrix.setMatrixCol(4,col_1_0,True)
        time.sleep(0.3)
        #6
        col = [bk,bk,bk,bk,b1,b1,b1,bk]
        self.matrix.setMatrixCol(0,col)
        col_6_0 = col        
        col = [bk,bk,bk,bk,b1,b1,bk,b1]
        self.matrix.setMatrixCol(1,col)
        col_6_1 = col
        self.matrix.setMatrixCol(2,col_4_0)
        self.matrix.setMatrixCol(3,col_4_1)
        self.matrix.setMatrixCol(4,col_2_0)
        self.matrix.setMatrixCol(5,col_2_1,True)
        time.sleep(0.3)
        #7
        col = [bk,bk,b1,b1,b1,b1,b1,b1]
        self.matrix.setMatrixCol(0,col)
        col_7_0 = col        
        col = [bk,bk,bk,bk,b1,b1,b2,bk]
        self.matrix.setMatrixCol(1,col)
        col_7_1 = col        
        self.matrix.setMatrixCol(2,col_5_0)
        self.matrix.setMatrixCol(3,col_4_0)
        self.matrix.setMatrixCol(4,col_3_0)
        self.matrix.setMatrixCol(5,col_3_1)
        self.matrix.setMatrixCol(6,col_1_0,True)
        time.sleep(0.3)
        #8
        col = [bk,bk,b1,bk,bk,bk,bk,bk]
        self.matrix.setMatrixCol(0,col)
        col_8_0 = col       
        col = [bk,bk,bk,b1,b1,b1,b2,b2]
        self.matrix.setMatrixCol(1,col)
        col_8_1 = col   
        self.matrix.setMatrixCol(2,col_6_0)     
        self.matrix.setMatrixCol(3,col_6_1)
        self.matrix.setMatrixCol(4,col_4_0)
        self.matrix.setMatrixCol(5,col_4_1)
        self.matrix.setMatrixCol(6,col_2_0)
        self.matrix.setMatrixCol(7,col_2_1,True)
        time.sleep(0.3)
        #9
        self.matrix.setMatrixCol(0,col_blk)        
        self.matrix.setMatrixCol(1,col_blk)
        self.matrix.setMatrixCol(2,col_7_0)
        self.matrix.setMatrixCol(3,col_7_1)
        self.matrix.setMatrixCol(4,col_5_0)
        self.matrix.setMatrixCol(5,col_4_0)
        self.matrix.setMatrixCol(6,col_3_0)
        self.matrix.setMatrixCol(7,col_3_1,True)
        time.sleep(0.3)
        #10
        self.matrix.setMatrixCol(2,col_8_0)
        self.matrix.setMatrixCol(3,col_8_1)     
        self.matrix.setMatrixCol(4,col_6_0)     
        self.matrix.setMatrixCol(5,col_6_1)
        self.matrix.setMatrixCol(6,col_4_0)
        self.matrix.setMatrixCol(7,col_4_1,True)
        time.sleep(0.3)
        #11 there is no change from 10
        #12
        self.matrix.setMatrixCol(2,col_blk)    
        self.matrix.setMatrixCol(3,col_blk)        
        self.matrix.setMatrixCol(4,col_7_0)
        self.matrix.setMatrixCol(5,col_7_1)
        self.matrix.setMatrixCol(6,col_5_0)
        self.matrix.setMatrixCol(7,col_4_0,True)
        time.sleep(0.3)
        #13
        self.matrix.setMatrixCol(4,col_8_0)
        self.matrix.setMatrixCol(5,col_8_1)     
        self.matrix.setMatrixCol(6,col_6_0)     
        self.matrix.setMatrixCol(7,col_6_1,True)
        time.sleep(0.3)
        #14
        self.matrix.setMatrixCol(4,col_blk)    
        self.matrix.setMatrixCol(5,col_blk)        
        self.matrix.setMatrixCol(6,col_7_0)
        self.matrix.setMatrixCol(7,col_7_1,True)
        time.sleep(0.3)
        #15
        self.matrix.setMatrixCol(6,col_8_0)        
        col = [bk,bk,bk,b1,b1,b1,bk,bk]
        self.matrix.setMatrixCol(7,col,True)
        time.sleep(0.3)  
        #16
        self.matrix.setMatrixCol(6,col_blk)
        self.matrix.setMatrixCol(7,col_blk,True)
        time.sleep(0.3)
        
    def icon_cat(self):
        bk = (0,0,0)
        g1 = [136,136,136]
        g2 = [86,86,86]
        pk = [248,134,137]
        rd = [195,51,55]
        #1
        row = [bk,g1,bk,bk,bk,bk,g1,bk]
        self.matrix.setMatrixRow(0,row)
        row = [bk,pk,g1,bk,bk,g1,pk,bk]
        self.matrix.setMatrixRow(1,row)
        row = [bk,g1,g1,g1,g1,g1,g1,bk]
        self.matrix.setMatrixRow(2,row)
        row = [bk,g1,bk,g1,g1,bk,g1,bk]
        self.matrix.setMatrixRow(3,row)
        row = [g1,g1,g1,g1,g1,g1,g1,g1]
        self.matrix.setMatrixRow(4,row)
        row = [bk,g2,g2,pk,pk,g2,g2,bk]
        self.matrix.setMatrixRow(5,row)
        row = [bk,bk,g2,g1,g1,g2,bk,bk]
        self.matrix.setMatrixRow(6,row)
        row = [bk,g1,bk,g2,g2,bk,g1,bk]
        self.matrix.setMatrixRow(7,row,True)
        time.sleep(0.2)
        #2        
        row = [bk,bk,g2,rd,rd,g2,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.2)
        #3  
        row = [bk,bk,g2,rd,g2,g2,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.2)
        #4  
        row = [bk,bk,g2,rd,rd,g2,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.2)
        #5  
        row = [bk,bk,g2,rd,g2,g2,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.2)
        #6
        row = [bk,bk,g2,g1,g1,g2,bk,bk]
        self.matrix.setMatrixRow(6,row,True)
        time.sleep(0.2)
        
if __name__ == '__main__':
    # creates an instance of the class
    ico = OttoRGBMatrixIcon(3)
    ico.matrix.setBrightness(0.5)

    for j in range(12):
        for i in range(2):
            ico.showIconByNumber(j)
            time.sleep(0.5)

