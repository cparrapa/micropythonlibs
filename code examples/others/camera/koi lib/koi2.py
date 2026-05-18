from busio import UART
from future import uartMap
from board_map import usePin,saveObj
import time
import json
__version__ = '1.0.3'

class KOI2:
    #basic
    def __init__(self,uart):
        self.uart = UART(usePin(uartMap[uart][0]),usePin(uartMap[uart][1]),baudrate=115200,timeout = 0)
        saveObj(uartMap[uart][0],self.uart)
        saveObj(uartMap[uart][1],self.uart)
        self.xywh = [-1] * 4
        self.xy12 = [-1] * 4
        self.numberVal = -1
        self.strVal = None
        self.faceAttr = [-1]*13
        self.btnStateA = 0
        self.btnStateB = 0
        self.btnStateAB = 0
        self.classifierMap = {}

        self.updateTime = time.monotonic()

    def valReset(self):
        self.xywh = [-1] * 4
        self.xy12 = [-1] * 4
        self.numberVal = -1
        self.strVal = None
        self.faceAttr = [-1]*13
        self.classifierMap = {}

    def read_from_uart(self):
        strModel = ['K81','K82','K84','K20','K85']
        numModel = ['K31','K83','K86']
        try:
            if time.monotonic() - self.updateTime > 1:
                self.valReset()
            data = self.uart.read()
            if data:
                cmd = data.decode().split('\r\n')[-2]
                if cmd[0] == 'K':
                    self.updateTime = time.monotonic()
                    try:
                        cmd = cmd.strip().split(' ')
                    except:
                        pass
                    if cmd[0] in numModel:#face
                        self.xywh = [int(i) for i in cmd[1:5]]
                        self.numberVal = int(cmd[5])
                    elif cmd[0] in strModel:#model type
                        self.xywh = [int(i) for i in cmd[1:5]]
                        self.strVal = cmd[5] 
                    elif cmd[0] == 'K42':#feature extraction
                        self.strVal = cmd[1]
                        self.numberVal = int(cmd[2])
                    elif cmd[0] == 'K15':#color blob
                        self.xywh = [int(i) for i in cmd[1:5]]
                    elif cmd[0] == 'K19':#line follower color
                        self.xy12 = [int(i) for i in cmd[1:5]]
                    elif cmd[0] == 'K65':
                        self.strVal = '-'.join(cmd[1:])
                    elif cmd[0] == 'K34':
                        self.faceAttr = cmd[1:]
                        self.xywh = cmd[1:5]
                    elif cmd[0] == 'K3':#btn
                        btnState =  int(cmd[1])
                        if btnState == 1:
                            self.btnStateA = 1
                        elif btnState == 2:
                            self.btnStateB = 1
                        elif btnState == 3:
                            self.btnStateAB = 1

        except Exception as e:
            print(e)

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

    #basic
    def setModel(self,model):
        if model == 0x9:
            self.numberVal = 0
        elif model == 0x4:
            self.numberVal = -1
        elif model == 0x5:
            self.numberVal = 5
        time.sleep(0.3)
        self.uart.write(b'\r\n')
        time.sleep(0.3)
        self.uart.write(b'\r\n')
        self.uart.write(b'K97 %d\r\n'%(model))
    
    def direction(self,dir):
        self.uart.write(b'K6 %d\r\n'%(dir))

    def mirror(self,enabled):
        self.uart.write(b'K7 %d\r\n'%(enabled))     

    #face
    def getFaceAttr(self,index):
        try:
            if index == 13:
                return int(self.faceAttr[8]) - int(self.faceAttr[9])
            return self.faceAttr[index]
        except Exception as e:
            print(e)
            return -1

    #audio
    def recorded(self,name,sec):
        self.uart.write(b'K61 %s %d\r\n'%(name,sec))

    def playAudio(self,name):
        self.uart.write(b'K62 %s\r\n'%(name))

    #color blob
    def colorCalibration(self):
        self.uart.write(b'K16\r\n')
    
    def colorSetting(self,v1,v2,v3,v4,v5,v6):
        self.uart.write(b'K17 %d %d %d %d %d %d\r\n'%(v1,v2,v3,v4,v5,v6))

    def colorSwitch(self,key):
        self.uart.write(b'K18 %d\r\n'%(key))

    #line blob
    def lineCalibration(self):
        self.uart.write(b'K16\r\n')
    
    def lineSetting(self,v1,v2,v3,v4,v5,v6):
        self.uart.write(b'K17 %d %d %d %d %d %d\r\n'%(v1,v2,v3,v4,v5,v6))

    def lineSwitch(self,key):
        self.uart.write(b'K18 %d\r\n'%(key))
    
    #classifier
    def classifierReset(self):
        self.uart.write(b'K45\r\n')

    def classifierAddTag(self,tag):
        self.uart.write(b'K41 %s\r\n'%(tag))

    def classifierSave(self,name):
        self.uart.write(b'K43 %s\r\n'%(name))

    def classifierLoad(self,name):
        self.uart.write(b'K44 %s\r\n'%(name))

    def classifierGetMostSimilarResults(self):
        self.uart.write(b'K42\r\n')

    def setDetectionTarget(self,name):
        self.uart.write(b'K42 %s\r\n'%name)

    def getSimilarity(self):
        if self.numberVal == -1:
            x = -5
        else:
            x = self.numberVal
        return round((5-x)/5*100,2)
    
    #scan code
    def scanCodeSwitchType(self,type):
        self.uart.write(b'K21 %d\r\n'%(type))

    #asr
    def asrSetKey(self,key):
        self.uart.write(b'K64 %s\r\n'%(key))

    #take a picture
    def takePic(self,path):
        self.uart.write(b'K2 %s\r\n'%(path))
    
    def displayPic(self,path,ms):
        self.uart.write(b'K1 %s %d\r\n'%(path,ms))
    
    #display text
    def displayText(self,x,y,delay,color,text):
        strColor = ','.join(str(i) for i in color)
        self.uart.write(b'K4 %d %d %d %s %s\r\n'%(x,y,delay,strColor,text))
    
    def initCustomModel(self,addr,anchor):
        addrType = 0
        if type(addr) == str:
            addrType = 1
        elif addr == int:
            addrType = 0
        anchorStr = ''
        for i in anchor:
            anchorStr += str(i)+','
        anchorStr = anchorStr[:-1]
        data = b'K87 %d %s %s\r\n'%(addrType,str(addr),anchorStr)
        self.uart.write(data)