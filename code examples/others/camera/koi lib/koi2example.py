from future import PINMAP
from machine import UART
import time
import json
__version__ = "1.0.7"

class KOI2:
    #basic
    def __init__(self,tx='P2',rx='P12',id=1):
        self.uart = UART(id,115200,tx=PINMAP[tx],rx=PINMAP[rx])
        self.xywh = [-1] * 4
        self.xy12 = [-1] * 4
        self.numberVal = -1
        self.strVal = None
        self.faceAttr = [-1]*13
        self.btnStateA = 0
        self.btnStateB = 0
        self.btnStateAB = 0

        self.updateTime = time.ticks_ms()
    
    def valReset(self):
        self.xywh = [-1] * 4
        self.xy12 = [-1] * 4
        self.numberVal = -1
        self.strVal = None
        self.faceAttr = [-1]*13

    def read_from_uart(self):
        strModel = ["K81","K82","K84","K20","K85"]
        numModel = ["K31","K83","K86"]
        try:
            if time.ticks_ms() - self.updateTime > 1000:
                self.valReset()
            if self.uart.any():
                self.updateTime = time.ticks_ms()
                cmd = self.uart.read().decode().split("\r\n")[-2]
                if cmd[0] == 'K':
                    try:
                        cmd = cmd.strip().split(" ")
                    except:
                        pass
                    if cmd[0] in numModel:#face
                        self.xywh = [int(i) for i in cmd[1:5]]
                        self.numberVal = int(cmd[5])
                    elif cmd[0] in strModel:#model type
                        self.xywh = [int(i) for i in cmd[1:5]]
                        self.strVal = cmd[5] 
                    elif cmd[0] == "K42":#feature extraction
                        self.strVal = cmd[1]
                        self.numberVal = float(cmd[2])
                    elif cmd[0] == "K15":#color blob
                        self.xywh = [int(i) for i in cmd[1:5]]
                    elif cmd[0] == "K19":#line follower color
                        self.xy12 = [int(i) for i in cmd[1:5]]
                    elif cmd[0] == "K65":
                        self.strVal = "-".join(cmd[1:])
                    elif cmd[0] == "K34":
                        self.faceAttr = cmd[1:]
                        self.xywh = cmd[1:5]
                    elif cmd[0] == "K3":#btn
                        btnState =  int(cmd[1])
                        if btnState == 1:
                            self.btnStateA = 1
                        elif btnState == 2:
                            self.btnStateB = 1
                        elif btnState == 3:
                            self.btnStateAB = 1

        except Exception as e:
            print(e)

    #basic
    def deinit(self):
        time.sleep(0.1)  # Give the thread some time to stop
        self.uart.deinit()
    
    def getBtnState(self,btn):
        if btn == 'A':
            if self.btnStateA:
                self.btnStateA = 0
                return True
        elif btn == 'B':
            if self.btnStateB:
                self.btnStateB = 0
                return True
        elif btn == 'AB':
            if self.btnStateAB:
                self.btnStateAB = 0
                return True
        return False

    def setModel(self,model):
        if model == 0x9:
            self.numberVal = 0
        elif model == 0x4:
            self.numberVal = -1
        elif model == 0x5:
            self.numberVal = 5
        time.sleep(0.3)
        self.uart.write("\r\n")
        time.sleep(0.3)
        self.uart.write("\r\n")
        self.uart.write("K97 %d\r\n"%(model))
    
    def direction(self,dir):
        self.uart.write("K6 %d\r\n"%(dir))

    def mirror(self,enabled):
        self.uart.write(b'K7 %d\r\n'%(enabled))     

    #audio
    def recorded(self,name,sec):
        self.uart.write("K61 %s %d\r\n"%(name,sec))

    def playAudio(self,name):
        self.uart.write("K62 %s\r\n"%(name))

    #face
    def getFaceAttr(self,index):
        try:
            if index == 13:
                return int(self.faceAttr[8]) - int(self.faceAttr[9])
            return self.faceAttr[index]
        except Exception as e:
            print(e)
            return -1

    #color blob
    def colorCalibration(self):
        self.uart.write("K16\r\n")
    
    def colorSetting(self,v1,v2,v3,v4,v5,v6):
        self.uart.write("K17 %d %d %d %d %d %d\r\n"%(v1,v2,v3,v4,v5,v6))

    def colorSwitch(self,key):
        self.uart.write("K18 %d\r\n"%(key))

    #line blob
    def lineCalibration(self):
        self.uart.write("K16\r\n")
    
    def lineSetting(self,v1,v2,v3,v4,v5,v6):
        self.uart.write("K17 %d %d %d %d %d %d\r\n"%(v1,v2,v3,v4,v5,v6))

    def lineSwitch(self,key):
        self.uart.write("K18 %d\r\n"%(key))
    
    #classifier
    def classifierReset(self):
        self.uart.write("K45\r\n")

    def classifierAddTag(self,tag):
        self.uart.write("K41 %s\r\n"%(tag))
    
    def classifierGetMostSimilarResults(self):
        self.uart.write("K42\r\n")

    def classifierSetDetectionTarget(self,tag):
        self.uart.write("K42 %s\r\n"%(tag))

    def classifierSave(self,name):
        self.uart.write("K43 %s\r\n"%(name))

    def classifierLoad(self,name):
        self.uart.write("K44 %s\r\n"%(name))

    def getSimilarity(self):
        if self.numberVal == -1:
            self.numberVal = 5
        x = min(self.numberVal,5)
        return round((5-x)/5*100,2)
    
    #scan code
    def scanCodeSwitchType(self,type):
        self.uart.write("K21 %d\r\n"%(type))

    #asr
    def asrSetKey(self,key):
        self.uart.write("K64 %s\r\n"%(key))

    #take a picture
    def takePic(self,path):
        self.uart.write("K2 %s\r\n"%(path))
    
    def displayPic(self,path,ms):
        self.uart.write("K1 %s %d\r\n"%(path,ms))
    
    #display text
    def displayText(self,x,y,delay,color,text):
        strColor = ",".join(str(i) for i in color)
        self.uart.write("K4 %d %d %d %s %s\r\n"%(x,y,delay,strColor,text))
    
    def initCustomModel(self,addr,anchor):
        addrType = 0
        if type(addr) == str:
            addrType = 1
        elif addr == int:
            addrType = 0
        anchorStr = ""
        for i in anchor:
            anchorStr += str(i)+","
        anchorStr = anchorStr[:-1]
        data = "K87 %d %s %s\r\n"%(addrType,str(addr),anchorStr)
        self.uart.write(data)
        
