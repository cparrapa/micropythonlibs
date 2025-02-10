import board
from busio import UART
import time
from future import uartMap
from board_map import usePin,saveObj

__version__ = "1.0.8"
VERSIONS = 'K0'
QRCODE = 'K11'
RECOGNIZE = "K12"
PLAYWAV = "K15"
ISDARKNESS = "K17"
AUDIOTEST = "K18"
BUTTONSTATE = "K19"
MQQTTCONNECT = "K20"
MQTTSUBSCRIPTION = "K21"
MQTTMESSAGE = "K22"
MQTTSEND = "K23"
SETGRB = "K16"
SETALLRGB = "K25"
TAKEPICTURE = "K27"
class SugarCam:
    def __init__(self,uart):
        self.space = ['0']*8
        self.excess = 5
        self.uart = UART(usePin(uartMap[uart][0]),usePin(uartMap[uart][1]),baudrate=115200,timeout = 0)
        saveObj(uartMap[uart][0],self.uart)
        saveObj(uartMap[uart][1],self.uart)
        
        self.uart.write(bytes('\n\n','utf-8'))
        time.sleep(0.4)
        flag = ''
        count = 0

        self.topicMap = {}
        while True:
            if count == 10:
                print("Please try to reset the sugar_cam!!")
                count = 0
            data = self.uart.readline()
            print(data)
            if data:
                try:
                    flag = str(data,'UTF-8')
                    if VERSIONS in flag:
                        pass
                        break
                    else:
                        pass
                except:
                    pass
                    flag = ''
            else:
                self.uart.write('{} \r\n'.format(VERSIONS).encode())
                count+=1
                time.sleep(1)
    def getQRcode(self):
        data = None
        self.uart.read()
        self.uart.write('{} \r\n'.format(QRCODE).encode())
        time.sleep(2)
        data = self.uart.read()
        if data:
            try:
                data = data.decode().split(" ")
                if data[0] != QRCODE:
                    return None
                else:
                    if data[1][0:4] == 'None':
                        return None
                    else:
                        data = data[1].replace("\n","").replace("\r","").lstrip().rstrip()
                        return data
            except:
                return None
            
    def isDarkness(self):    
        data = None
        self.uart.read()
        self.uart.write('{} \r\n'.format(ISDARKNESS).encode())
        time.sleep(0.5)
        data = self.uart.read()
        if data:
            try:
                data = data.decode().split(" ")
                print(data)
                if data[0] != ISDARKNESS:
                    return None
                elif "False" in str(data[1]):
                    return False 
                elif "True" in str(data[1]):
                    return True 
            except:
                return False
            
    def playWav(self,wav):
        self.uart.write('{} {} \r\n'.format(PLAYWAV,wav).encode())
        time.sleep(1)

    def audioTest(self):
        self.uart.write('{} \r\n'.format(AUDIOTEST).encode())
        time.sleep(1)

    def setColor(self,color1,color2):
        self.uart.write('{} {} {} \r\n'.format(SETGRB,str(color1).replace(' ',''),str(color2).replace(' ','')).encode())
        time.sleep(1)

    def setAllColor(self,color1):
        self.uart.write('{} {} \r\n'.format(SETALLRGB,str(color1).replace(' ','')).encode())
        time.sleep(1)

    def takePicture(self,filename):
        self.uart.write('{} {} \r\n'.format(TAKEPICTURE,str(filename).replace(' ','')).encode())
        time.sleep(1)
        

    def recognize(self,sec,vid):
        data = None
        data = self.uart.read()
        self.uart.write('{} {} {} \r\n'.format(RECOGNIZE,sec,vid).encode())
        num=0
        while num != 12:
            time.sleep(1)
            data = self.uart.read()
            if data:
                try:
                    data = data.decode().strip().split(" ")
                    if data[0] != RECOGNIZE:
                        return None
                    else:
                        return data[1]
                except:
                    return None
            num+=1
    def buttonState(self,button):
        data = None
        self.uart.read()
        self.uart.write('{} {} \r\n'.format(BUTTONSTATE,button).encode())
        time.sleep(1.5)
        data = self.uart.read()
        if data:
            try:
                data = data.decode().split(" ")
                if data[0] != BUTTONSTATE:
                    return None
                else:
                    if len(data)!=4:
                        return None
                    if data[1] != button:
                        return None
                    return bool(int(data[2]))
            except:
                return None
    def mqttConnect(self,addr,client,user="",pwd=""):
        if user != "" and pwd != "":
            self.uart.write('{} {} {} {} {} \r\n'.format(MQQTTCONNECT,addr,client,user,pwd).encode())
        else:
            self.uart.write('{} {} {} \r\n'.format(MQQTTCONNECT,addr,client).encode())
        time.sleep(1)

    def mqttSubscription(self,topic):
        self.topicMap[topic] = None
        self.uart.write('{} {} \r\n'.format(MQTTSUBSCRIPTION,topic).encode())
        time.sleep(1)
    
    def mqttSend(self,topic,message):
        self.uart.write('{} {} {} \r\n'.format(MQTTSEND,topic,message).encode())
        time.sleep(1)

    def mqttMessage(self,topic):
        data = None
        self.uart.read()
        self.uart.write('{} \r\n'.format(MQTTMESSAGE).encode())
        time.sleep(1.5)
        data = self.uart.read()
        if data:
            data = data.decode().strip().split(" ")
            if data[0] != MQTTMESSAGE:
                return None
            else:
                self.topicMap[data[2]] = data[1]
        data = self.topicMap[topic]
        if data:
            self.topicMap[topic] = None
            return data
        else:
            return None