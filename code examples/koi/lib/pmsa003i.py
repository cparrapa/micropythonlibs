from board import I2C
from time import sleep

__version__ = "1.0.0"

class PMSA003I:
    def __init__(self):
        self.addr = 0x12
        self.i2c = I2C()
        self.i2c.try_lock()
        self.dataList = [0]*6
    
    def read(self):
        data = bytearray(32)
        self.i2c.readfrom_into(self.addr,data)
        verify_expect  = (data[0x1e] << 8) | data[0x1f]
        if verify_expect != sum(i for i in data[0:30]):
            return self.dataList
        
        ##PM1.0,PM2.5,PM10
        ##CF=1,标准颗粒物
        self.dataList[0] = (data[0x04] << 8) | data[0x05]
        self.dataList[1] = (data[0x06] << 8) | data[0x07]
        self.dataList[2] = (data[0x08] << 8) | data[0x09]

        ##PM1.0,PM2.5,PM10
        ##大气环境下
        self.dataList[3] = (data[0x0a] << 8) | data[0x0b]
        self.dataList[4] = (data[0x0c] << 8) | data[0x0d]
        self.dataList[5] = (data[0x0e] << 8) | data[0x0f]

        sleep(0.1)

        return self.dataList