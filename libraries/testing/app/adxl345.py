# adxl345.py v1.0 28/06/24
import math
from machine import Pin, SoftI2C
from time import sleep

# ADXL-345 Registers 
_DATA_FORMAT = const(0x31)
_POWER_CTL = const(0x2D)
_DATAX0 = const(0x32)
_X_CAL = const(0x1E)
_Y_CAL = const(0x1F)
_Z_CAL = const(0x20)

class ADXL345:
    def __init__(self, i2c, address=0x53):
        self.i2c = i2c
        self.address = address
        self.i2c.start()
        # power on
        self.i2c.writeto(self.address, bytearray([_POWER_CTL, 0x08])) 
        # -2g to +2g resolution
        self.i2c.writeto(self.address, bytearray([_DATA_FORMAT, 0x08])) 
        self.i2c.stop()
        self.Calibrate()
        
    def ReadXYZ(self):   #-2g to +2g is -512 to + 511
        x, y, z = self.ReadRawXYZ()
        return (x/256, y/256, z/256)
    
    def ReadRawXYZ(self):
        self.i2c.start()
        self.i2c.writeto(self.address, bytearray([_DATAX0]))
        #read 6 registers, 2 for each co-ordinate
        data = self.i2c.readfrom(self.address, 6)
        self.i2c.stop()
        
        x = ((data[1] << 8) | data[0])
        x = x & 1023    #10 bit - was getting some noise in bits 11 - 16
        if x > 511:     #values are signed
            x = x - 1024        
        y = ((data[3] << 8) | data[2])   
        y = y & 1023
        if y > 511:
            y = y - 1024
        z = ((data[5] << 8) | data[4])
        z = z & 1023
        if z > 511:
            z = z -1024
        return (x, y, z)
          
    #still not happy with these calculations
    def RollPitch(self):
        x,y,z = self.ReadXYZ()
        roll = math.atan2(x , math.sqrt(pow(x, 2) + pow(z, 2))) * 180 / math.pi;
        pitch = math.atan2(-x , math.sqrt(pow(y, 2) + pow(z, 2))) * 180 / math.pi;        
        return (roll,pitch)
    
    def Calibrate(self):
        errX = 0
        errY = 0
        errZ = 0
        # take 200 readings
        for _ in range (200):
            x, y, z = self.ReadRawXYZ()
            # Sum all readings            
            errX += x
            errY += y
            errZ += z
        #divide by 200         
        errX = errX/200
        errY = errX/200
        errZ = errX/200        
        # x should be 0, y should be 0  z should be 1g (255)
        # calculate offset and divide by 4
        errX = int((0 - errX)/4)
        errY = int((0- errY)/4)
        errZ = int(255 - errZ/4)
        # write these to the calibration registers
        #X-axis        
        self.i2c.start()
        self.i2c.writeto(self.address, bytearray([_X_CAL, errX]))
        self.i2c.stop()
        sleep(0.1)
        #Y-axis        
        self.i2c.start()
        self.i2c.writeto(self.address, bytearray([_Y_CAL, errY]))
        self.i2c.stop()
        sleep(0.1)
        #Z-axis        
        self.i2c.start()
        self.i2c.writeto(self.address, bytearray([_Z_CAL, errZ]))
        self.i2c.stop()
        sleep(0.1)