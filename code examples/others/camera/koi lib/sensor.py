import math
import board
import digitalio
import analogio
import struct
from future import MeowPin

__version__ = "1.0.7"

DA213ADDR = 39
ACC_REST = 400
ACC_SHAKE = 1600

class Sensor:
  def __init__(self):
    self.adcLight = analogio.AnalogIn(board.LUMI)
    self.btns = {}
    self.btns['a'] = digitalio.DigitalInOut(board.BTNA)
    self.btns['a'].switch_to_input(pull=digitalio.Pull.UP)

    self.btns['m'] = digitalio.DigitalInOut(board.BTNB)
    self.btns['m'].switch_to_input(pull=digitalio.Pull.UP)

    self.btns['b'] = digitalio.DigitalInOut(board.BTNC)
    self.btns['b'].switch_to_input(pull=digitalio.Pull.UP)

  def map2(self, x, in_min, in_max, out_min, out_max):
    return ((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

  def constrain(self, val, min, max): 
      if val < min: return min
      if val > max: return max
      return val

  # 700~4095 => 0~4095
  def getLight(self):
    return math.floor(self.map2(self.constrain(4096 - (self.adcLight.value >> 4), 700, 4095), 700, 4095, 0, 4095))

  def btnValue(self, btn=None):        
    pressed = []
    for n in self.btns:
      if self.btns[n].value == False:
        pressed.append(n)
    if btn:
      btn = btn.lower()
      return btn in pressed
    else:
      return pressed
    
class Da213:
  def __init__(self):
    self.i2c = board.I2C()
    self.i2c.try_lock()
    if DA213ADDR not in self.i2c.scan():
      print("IMU fail")
    else:
      self.da213Reg(0x7f, b'\x83')
      self.da213Reg(0x7f, b'\x69')
      self.da213Reg(0x7f, b'\xbd')
      a = bytearray(1)
      self.i2c.writeto_then_readfrom(DA213ADDR, b'\x8e', a)
      if a[0] == 0:
        self.da213Reg(0x8e, b'\x50')
      self.da213Reg(0x0f, b'\x40')
      self.da213Reg(0x20, b'\x00')
      self.da213Reg(0x11, b'\x34')
      self.da213Reg(0x10, b'\x07')
      self.da213Reg(0x1a, b'\x04')
      self.da213Reg(0x15, b'\x04')
      self.update()

  def da213Reg(self, reg, value):
    buf = bytearray([reg]) + value
    self.i2c.writeto(DA213ADDR, buf)

  def update(self):
    a = bytearray(6)
    self.i2c.writeto_then_readfrom(DA213ADDR, b'\x02', a)
    self.imu = struct.unpack('hhh', a)
    self.x = self.imu[1]/16 * -1
    self.y = self.imu[0]/16 * -1
    self.z = self.imu[2]/16
    return self.imu

  def accX(self):
    self.update()
    return self.x/1024.0
  
  def accY(self):
    self.update()
    return self.y/1024.0

  def accZ(self):
    self.update()
    return self.z/1024.0

  def acc(self, n):
    if n == 'X':
      return self.accX()
    if n == 'Y':
      return self.accY()
    if n == 'Z':
      return self.accZ()

  def _updatePR(self):
    self._roll = math.atan2(self.x, math.sqrt(self.y*self.y+self.z*self.z))*180/math.pi
    self._pitch = math.atan2(self.y, math.sqrt(self.x*self.x+self.z*self.z))*180/math.pi

  def pitch(self):
    self.update()
    self._updatePR()
    return self._pitch

  def roll(self):
    self.update()
    self._updatePR()
    return self._roll

  def attitude(self, att):
    if att == 'pitch':
      return self.pitch()
    if att == 'roll':
      return self.roll()
    return 0

  def gesture(self, gesCheck=None):
    self.update()
    shakeDect = False
    if (self.x < -ACC_SHAKE) or (self.x > ACC_SHAKE):
      shakeDect = True
    if (self.y < -ACC_SHAKE) or (self.y > ACC_SHAKE):
      shakeDect = True
    if (self.z < -ACC_SHAKE) or (self.z > ACC_SHAKE):
      shakeDect = True
    detGes = None
    self.gF = self.x*self.x + self.y*self.y + self.z*self.z
    if shakeDect:
      detGes='shake'
    elif self.gF < (200*200):
      detGes='freefall'
    elif self.y > 2*ACC_REST:
      detGes='tilt_up'#左倾
    elif self.y < -2*ACC_REST:
      detGes='tilt_down'#右倾
    elif self.x > 1.3*ACC_REST:
      detGes='tilt_left'#正立
    elif self.x < -1.3*ACC_REST:
      detGes='tilt_right'#倒立
    elif self.z < -2*ACC_REST:
      detGes='face_up'#朝上
    elif self.z > 2*ACC_REST:
      detGes='face_down'#朝下
    if gesCheck:
      return detGes==gesCheck
    else:
      return detGes   