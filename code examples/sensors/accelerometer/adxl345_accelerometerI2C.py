import time, ustruct
from machine import Pin, I2C

DATA_FORMAT = 0x31
BW_RATE  = 0x2c
POWER_CTL = 0x2d
INT_ENABLE  = 0x2E
OFSX = 0x1e
OFSY =0x1f
OFSZ =0x20

cs = Pin(2, Pin.OUT)
cs.value(1)
time.sleep(1)
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=10000) # Connector 3
slv = i2c.scan()

for s in slv:
    buf = i2c.readfrom_mem(s, 0, 1)
    if buf[0] == 0xe5:
      slvAddr = s
      print('adxl345 found at I2C address: ', slv)
      break

def writeByte(addr, data):
  d = bytearray([data])
  i2c.writeto_mem(slvAddr, addr, d)

def readByte(addr):
  return i2c.readfrom_mem(slvAddr, addr, 1)

writeByte(DATA_FORMAT,0x2B)
writeByte(BW_RATE,0x0A)
writeByte(INT_ENABLE,0x00)
writeByte(OFSX,0x00)
writeByte(OFSY,0x00)
writeByte(OFSZ,0x00)
writeByte(POWER_CTL,0x28)
time.sleep(1)


while True: 
   fmt = '<h' #little-endian
   buf1 = readByte(0x32)
   buf2 = readByte(0x33)
   buf = bytearray([buf1[0], buf2[0]])
   x, = ustruct.unpack(fmt, buf)
   x = x*3.9
   time.sleep(0.5)
   
   
   buf1 = readByte(0x34)
   buf2 = readByte(0x35)
   buf = bytearray([buf1[0], buf2[0]])
   y, = ustruct.unpack(fmt, buf)
   y = y*3.9
   time.sleep(0.5)
   
   buf1 = readByte(0x36)
   buf2 = readByte(0x37)
   buf = bytearray([buf1[0], buf2[0]])
   z, = ustruct.unpack(fmt, buf)
   z = z*3.9
   print('x:',x,'mg ','y:',y,'mg ','z:',z,'mg')
   time.sleep(1)