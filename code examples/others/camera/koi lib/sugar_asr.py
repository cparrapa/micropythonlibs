import board
from busio import UART
from time import sleep
import struct
from future import uartMap
from board_map import usePin,saveObj
__version__ = "1.0.2"

UART_SEND_HEAD = b'\xaa\x55'    # head of data
UART_SEND_FOOT = b'\x55\xaa'    # foot of data
UART_HEAD_LEN = 2
UART_FOOT_LEN = 2

TTS_INTEGER_CMD = 0x20          # tts id : signed integer
TTS_DOUBLE_CMD = 0x1f           # tts id : signed double
TTS_CLOCK_CMD = 0x03            # tts id : clock => (hour,minute)
TTS_DATE_CMD = 0x04             # tts id : date => (year,mouth,day)
INTEGER_LEN = 4                 # 4 bytes int
DOUBLE_LEN = 8                  # 8 bytes double
CLOCK_LEN = 2                   # 2 bytes clock(1,1)
DATE_LEN = 6                    # 2 bytes date(4,1,1)
'''高级模块_ASR语音识别模块'''
class SugarASR:
    def __init__(self,uart):
        self.uart = UART(usePin(uartMap[uart][0]),usePin(uartMap[uart][1]),baudrate=115200,timeout = 0)
        saveObj(uartMap[uart][0],self.uart)
        saveObj(uartMap[uart][1],self.uart)
        self.cmd = ''
    def detected(self):
        try:
            data = self.uart.read()
            if data:
                data = data.decode()
                self.cmd = data
                if not('asr' in self.cmd):
                    return 0
                else:
                    self.cmdParse()
                    return True
            else:
                return 0
        except:
            return 0
        finally:
            sleep(0.1)


    # 语音识别结果 (bool)
    def cmdParse(self):
        try:
            self.cmd = self.cmd.split('asr')[1]
        except Exception as err:
            # gc.collect()
            return 0


    # 限制数据
    def constrain(self, val, min, max): 
        if val < min: return min
        if val > max: return max
        return val


    # 语音播报整数
    def tts_int(self,num):
        buf = bytearray(9)
        num = self.constrain(num, -2**26, 2**26)
        int_to_bytearray = struct.pack('<L', int(num))
        print(int_to_bytearray)
        for i in range(UART_HEAD_LEN):  
            buf[i+0] = UART_SEND_HEAD[i]
        buf[2] = TTS_INTEGER_CMD              
        for i in range(INTEGER_LEN):    
            buf[i+3] = int_to_bytearray[i]
        for i in range(UART_FOOT_LEN):  
            buf[i+7] = UART_SEND_FOOT[i]
        self.uart.write(buf) 
        

    # 语音播报双精度小数
    def tts_double(self,f):
        buf = bytearray(13)
        f = self.constrain(f, -2**17, 2**17)
        float_to_bytearray = struct.pack('d', f)
        for i in range(UART_HEAD_LEN):  
            buf[i+0] = UART_SEND_HEAD[i]
        buf[2] = TTS_DOUBLE_CMD              
        for i in range(DOUBLE_LEN):    
            buf[i+3] = float_to_bytearray[i]
        for i in range(UART_FOOT_LEN):  
            buf[i+11] = UART_SEND_FOOT[i]
        self.uart.write(buf) 


    # 语音播报日期
    def tts_date(self,y,m,d):
        buf = bytearray(11)
        date_to_bytearray = struct.pack('<iBB',y,m,d)
        print(date_to_bytearray)
        for i in range(UART_HEAD_LEN):  
            buf[i+0] = UART_SEND_HEAD[i]
        buf[2] = TTS_DATE_CMD            
        for i in range(DATE_LEN):    
            buf[i+3] = date_to_bytearray[i]
        for i in range(UART_FOOT_LEN):  
            buf[i+9] = UART_SEND_FOOT[i]
        self.uart.write(buf)  
    

    # 语音播报时间
    def tts_clock(self,h,m):
        buf = bytearray(7)
        clock_to_bytearray = struct.pack('BB',h,m)
        for i in range(UART_HEAD_LEN):  
            buf[i+0] = UART_SEND_HEAD[i]
        buf[2] = TTS_CLOCK_CMD             
        for i in range(CLOCK_LEN):    
            buf[i+3] = clock_to_bytearray[i]
        for i in range(UART_FOOT_LEN):  
            buf[i+5] = UART_SEND_FOOT[i]
        self.uart.write(buf)  


    # 语音播报语句
    def tts_words(self, id):
        self.uart.write(bytearray([0xaa, 0x55, id, 0x55, 0xaa]))

if __name__ == '__main__':
    asr = SugarASR("uart1")
    asr.tts_words(5)