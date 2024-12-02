from busio import UART
from time import sleep
from future import uartMap
from board_map import usePin,saveObj
import time
__version__ = "1.0.0"
class SugarTTS:
    def __init__(self,uart):
        self.uart = UART(usePin(uartMap[uart][0]),usePin(uartMap[uart][1]),baudrate=9600,timeout = 0)
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
                    if 'K0' in flag:
                        pass
                        break
                    else:
                        pass
                except:
                    pass
                    flag = ''
            else:
                self.uart.write('{} \r\n'.format('K0').encode())
                count+=1
                time.sleep(1)
    def mp3Mode(self):
        self.uart.write("K1\n".encode())
        time.sleep(0.5)
    def play(self):
        self.uart.write("K2\n".encode())
        time.sleep(0.5)
    def stop(self):
        self.uart.write("K3\n".encode())
        time.sleep(0.5)
    def next(self):
        self.uart.write("K4\n".encode())
        time.sleep(0.5)
    def prev(self):
        self.uart.write("K5\n".encode())
        time.sleep(0.5)
    def playName(self,name):
        if name[-4:] != ".mp3":
            name += ".mp3"
        self.uart.write("K6 {}\n".format(name).encode())
        time.sleep(0.5)
    def playId(self,id):
        self.uart.write("K7 {}\n".format(id).encode())
        time.sleep(0.5)
    def ttsMode(self):
        self.uart.write("K8\n".encode())
        time.sleep(0.5)
    def playText(self,text):
        self.uart.write("K9 {}\n".format(text).encode())
        time.sleep(0.5)
if __name__ == '__main__':
    pass