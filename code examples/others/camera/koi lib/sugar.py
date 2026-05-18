import board
import digitalio
import analogio
import pwmio
import struct
from micropython import const
import time
import pulseio
import adafruit_irremote
from board_map import usePin, saveObj


__version__ = "1.2.2"


class ANALOG:
    def __init__(self, pin):   
        self.p = analogio.AnalogIn(usePin(pin))
        saveObj(pin,self.p)


class IN:
    def __init__(self, pin):
        self.p = digitalio.DigitalInOut(usePin(pin))
        saveObj(pin,self.p)
        self.p.switch_to_input(pull=digitalio.Pull.UP)


class OUT:
    def __init__(self, pin): 
        self.p = digitalio.DigitalInOut(usePin(pin))
        saveObj(pin,self.p)
        self.p.switch_to_output()


'''传感器_数字类_人体热释电传感器'''
class PIR(IN):
    def __init__(self, pin):
        self.pin = pin
        super(PIR,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = self.p.value
        except ValueError:
            super(PIR,self).__init__(self.pin)
            val = self.p.value
        return val


'''传感器_数字类_数字巡线传感器'''
class Tracker(IN):
    def __init__(self, pin):
        self.pin = pin
        super(Tracker,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = self.p.value
        except ValueError:
            super(Tracker,self).__init__(self.pin)
            val = self.p.value
        return val


'''传感器_数字类_霍尔传感器'''
class Hall(IN):
    def __init__(self, pin):
        self.pin = pin
        super(Hall,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = self.p.value
        except ValueError:
            super(Hall,self).__init__(self.pin)
            val = self.p.value
        return val



'''传感器_数字类_按键'''
class Button(IN):
    def __init__(self, pin):
        self.pin = pin
        super(Button,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = self.p.value
        except ValueError:
            super(Button,self).__init__(self.pin)
            val = self.p.value
        return val

'''传感器_数字类_碰撞开关'''
class Crash(IN):
    def __init__(self, pin):
        self.pin = pin
        super(Crash,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = self.p.value
        except ValueError:
            super(Crash,self).__init__(self.pin)
            val = self.p.value
        return val


'''传感器_数字类_触摸开关'''
class Touch(IN):
    def __init__(self, pin):
        self.pin = pin
        super(Touch,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = self.p.value
        except ValueError:
            super(Touch,self).__init__(self.pin)
            val = self.p.value
        return val

'''传感器_模拟类_声音传感器'''
class Sound(ANALOG):
    def __init__(self, pin):
        self.pin = pin
        super(Sound,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = 4050 - int(self.p.value/15.009)
        except ValueError:
            super(Sound,self).__init__(self.pin)
            val = 4050 - int(self.p.value/15.009)
        return val

'''显示模块_数字类_LED灯'''
class LED:
    def __init__(self, pin):
        self.pin = pin
        self.setMode()
        
    def setMode(self):
        try:
            self.p = pwmio.PWMOut(usePin(self.pin), frequency=500, variable_frequency=False)
            self.p.duty_cycle = 0
            saveObj(self.pin,self.p)
        except Exception as e:
            print(e)
    
    def brightness(self, val):
        try:
            val = min(100,max(0,val))
            self.p.duty_cycle = int(val*65535/100)
        except ValueError:
            self.__init__(self.pin)
            self.p.duty_cycle = int(val*65535/100)
            
    def state(self, sta):
        if type(sta) == str:
            sta = sta.upper()
            if sta == 'ON':
                sta = 1
            elif sta == 'OFF':
                sta = 0
        try:
            if sta:
                self.p.duty_cycle = 65535
            elif sta==0:
                self.p.duty_cycle = 0
        except ValueError:
            self.__init__(self.pin)
            if sta:
                self.p.duty_cycle = 65535
            elif sta==0:
                self.p.duty_cycle = 0



'''执行模块_数字类_振动马达'''
class Vibrate(OUT):
    def __init__(self, pin):
        self.pin = pin
        super(Vibrate,self).__init__(pin)
            
    def state(self, sta):
        if type(sta) == str:
            sta = sta.upper()
            if sta == 'ON':
                sta = 1
            elif sta == 'OFF':
                sta = 0
        try:
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0
        except ValueError:
            super(Vibrate,self).__init__(self.pin)
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0


'''执行模块_数字类_有源蜂鸣器'''
class BuzzerA(OUT):
    def __init__(self, pin):
        self.pin = pin
        super(BuzzerA,self).__init__(pin)
            
    def state(self, sta):
        if type(sta) == str:
            sta = sta.upper()
            if sta == 'ON':
                sta = 1
            elif sta == 'OFF':
                sta = 0
        try:
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0
        except ValueError:
            super(BuzzerA,self).__init__(self.pin)
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0


'''显示模块_数字类_红点激光'''
class Laser(OUT):
    def __init__(self, pin):
        self.pin = pin
        super(Laser,self).__init__(pin)
            
    def state(self, sta):
        if type(sta) == str:
            sta = sta.upper()
            if sta == 'ON':
                sta = 1
            elif sta == 'OFF':
                sta = 0
        try:
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0
        except ValueError:
            super(Laser,self).__init__(self.pin)
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0

'''显示模块_数字类_雾化模块'''
class Fogging(OUT):
    def __init__(self, pin):
        self.pin = pin
        super(Fogging,self).__init__(pin)
            
    def state(self, sta):
        if type(sta) == str:
            sta = sta.upper()
            if sta == 'ON':
                sta = 1
            elif sta == 'OFF':
                sta = 0
        try:
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0
        except ValueError:
            super(Laser,self).__init__(self.pin)
            if sta:
                self.p.value = 1
            elif sta == 0:
                self.p.value = 0

'''传感器_模拟类_火焰传感器'''
class Flame(ANALOG):
    def __init__(self, pin):
        self.pin = pin
        super(Flame,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = int(self.p.value/15.009)
        except ValueError:
            super(Flame,self).__init__(self.pin)
            val = int(self.p.value/15.009)
        return val


'''传感器_模拟类_亮度传感器'''
class Light(ANALOG):
    def __init__(self, pin):
        self.pin = pin
        super(Light,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = int(self.p.value/15.009)
        except ValueError:
            super(Light,self).__init__(self.pin)
            val = int(self.p.value/15.009)
        return val


'''传感器_模拟类_电位器'''
class Angle(ANALOG):
    def __init__(self, pin):
        self.pin = pin
        super(Angle,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = int(self.p.value/15.009)
        except ValueError:
            super(Angle,self).__init__(self.pin)
            val = int(self.p.value/15.009)
        return val
    
'''传感器_模拟类_灰度传感器'''
class Grayscale(ANALOG):
    def __init__(self, pin):
        self.pin = pin
        super(Grayscale,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = int(self.p.value/15.009)
        except ValueError:
            super(Grayscale,self).__init__(self.pin)
            val = int(self.p.value/15.009)
        return val

    

'''传感器_模拟类_土壤湿度感器'''
class Soil(ANALOG):
    def __init__(self, pin):
        self.pin = pin
        super(Soil,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = int(self.p.value/15.009)
        except ValueError:
            super(Soil,self).__init__(self.pin)
            val = int(self.p.value/15.009)
        return val


'''传感器_模拟类_水位雨滴传感器'''
class WaterLevel(ANALOG):
    def __init__(self, pin):
        self.pin = pin
        super(WaterLevel,self).__init__(pin)
    
    def value(self):
        val= None
        try:
            val = int(self.p.value/15.009)
        except ValueError:
            super(WaterLevel,self).__init__(self.pin)
            val = int(self.p.value/15.009)
        return val



class TOFDistance:

    def __init__(self):
        self._VL53L0X_ADDR = const(0x5e)
        try:
            self.iic = board.I2C()
        except RuntimeError:
            from screen import Screen
            import sys
            screens = Screen()
            screens.init()
            screens.autoRefresh(False)
            screens.setRotation(90)
            screens.fill((0, 0, 0))
            screens.rect(0,0,160,20,(255, 0, 0),1)
            screens.text('I2C模块连接异常',5,5,1,(255, 255, 255))
            screens.text('请将右侧的4针I2C模块重新连接',5,30,1,(255, 255, 255))
            screens.text('然后再复位主板',5,50,1,(255, 255, 255))
            screens.refresh()
            sys.exit()
        self.iic.try_lock()

    def value(self):
        try:
            v = bytearray(2)
            self.iic.writeto(self._VL53L0X_ADDR,bytearray([1,2]))
            self.iic.readfrom_into(0x5e,v)
            dis = struct.unpack('h', v)[0]
            if dis > 8000:
                print('out of limited 1200mm')
                return 9999
            else:
                return dis
        except OSError:
            from screen import Screen
            import sys
            screens = Screen()
            screens.init()
            screens.autoRefresh(False)
            screens.setRotation(90)
            screens.fill((0, 0, 0))
            screens.rect(0,0,160,20,(255, 0, 0),1)
            screens.text('未检测到激光测距模块！',5,5,1,(255, 255, 255))
            screens.text('请将激光测距模块连接到右侧',5,30,1,(255, 255, 255))
            screens.text('带有I2C标识的4针接口',5,50,1,(255, 255, 255))
            screens.refresh()
            sys.exit()




'''传感器_IIC_温湿度传感器AHT20'''
class ENV:

    def __init__(self):
        self.temp = 0
        self.humi = 0
        try:
            self.iic = board.I2C()
        except RuntimeError:
            from screen import Screen
            import sys
            screens = Screen()
            screens.init()
            screens.autoRefresh(False)
            screens.setRotation(90)
            screens.fill((0, 0, 0))
            screens.rect(0,0,160,20,(255, 0, 0),1)
            screens.text('I2C模块连接异常',5,5,1,(255, 255, 255))
            screens.text('请将右侧的4针I2C模块重新连接',5,30,1,(255, 255, 255))
            screens.text('然后再复位主板',5,50,1,(255, 255, 255))
            screens.refresh()
            sys.exit()
        self.iic.try_lock()
        self._AHT20_ADDR = const(0x38)

    def _ahtState(self):
        n = bytearray(1)
        self.iic.readfrom_into(self._AHT20_ADDR, n)
        return n[0]

    def update(self):
        self.iic.writeto(self._AHT20_ADDR, b'\xac\x33\x00')
        s = self._ahtState()
        while s & 0x80:
            time.sleep(0.01)
            s = self._ahtState()
        n = bytearray(6)
        self.iic.readfrom_into(self._AHT20_ADDR, n)
        h = ((n[1] << 16) | (n[2] << 8) | (n[3])) >> 4
        self.humi = round(h*0.000095, 1)
        t = ((n[3]&0x0f)<<16|(n[4]<<8)|n[5])
        self.temp = round(t*0.000191 - 50, 1)
        return (self.temp, self.humi)


'''高级模块_五向摇杆模块'''
class Joystick:
    def __init__(self):
        self.sta = None
        self._JOYSTICK_ADDR = const(0x5c)
        try:
            self.iic = board.I2C()
        except RuntimeError:
            from screen import Screen
            import sys
            screens = Screen()
            screens.init()
            screens.autoRefresh(False)
            screens.setRotation(90)
            screens.fill((0, 0, 0))
            screens.rect(0,0,160,20,(255, 0, 0),1)
            screens.text('I2C模块连接异常',5,5,1,(255, 255, 255))
            screens.text('请将右侧的4针I2C模块重新连接',5,30,1,(255, 255, 255))
            screens.text('然后再复位主板',5,50,1,(255, 255, 255))
            screens.refresh()
            sys.exit()
        self.iic.try_lock()
        sta = bytearray(1)
        try:
            self.iic.writeto(self._JOYSTICK_ADDR,bytearray([1,1]))
            self.iic.readfrom_into(self._JOYSTICK_ADDR,sta)
        except OSError:
            from screen import Screen
            import sys
            screens = Screen()
            screens.init()
            screens.autoRefresh(False)
            screens.setRotation(90)
            screens.fill((0, 0, 0))
            screens.rect(0,0,160,20,(255, 0, 0),1)
            screens.text('未检测到摇杆模块！',5,5,1,(255, 255, 255))
            screens.text('请将摇杆模块连接到右侧',5,30,1,(255, 255, 255))
            screens.text('带有I2C标识的4针接口',5,50,1,(255, 255, 255))
            screens.refresh()
            sys.exit()

    def state(self):
        sta = bytearray(1)
        self.iic.writeto(self._JOYSTICK_ADDR,bytearray([1,1]))
        self.iic.readfrom_into(self._JOYSTICK_ADDR,sta)
        sta = sta[0]
        if sta & 0x1:
            self.sta = "pressed"
        elif sta & 0x10:
            self.sta = "left"
        elif sta & 0x08:
            self.sta = "right"
        elif sta & 0x04:
            self.sta = "up"
        elif sta & 0x02:
            self.sta = "down"
        else:
            self.sta = 'none'
        return self.sta

    def value(self, d):
        adc = bytearray(4)
        self.iic.writeto(self._JOYSTICK_ADDR,bytearray([2,4]))
        self.iic.readfrom_into(self._JOYSTICK_ADDR,adc)
        adc = struct.unpack('hh',adc)
        if d.isalpha():
            d = d.upper()
            if d == 'X':
                return int(255/2048*adc[0]-255)
            if d == 'Y':
                return int(255/2048*adc[1]-255)


'''显示模块_数码管'''
class Nixietube():


    def __init__(self, iic=board.I2C()):
        # 0~9/A~F
        self._TM1650_BUF = (0x3F,0x06,0x5B,0x4F,0x66,0x6D,0x7D,0x07,0x7F,0x6F,0x77,0x7C,0x39,0x5E,0x79,0x71)
        # -
        self._TM1650_MINUS = const(0x40)
        try:
            self.i2c = iic
            self.i2c.try_lock()
            self._intensity = 4
            self.dbuf = [0, 0, 0, 0]
            self.tbuf = bytearray(1)
            self.num_len = 0
            self.tbuf[0] = self._intensity|0x01
            self.i2c.writeto(0x24,self.tbuf)
        except Exception as e:
            print("Display init fail", e)

    def intensity(self, val = -1):
        if val < 0 or val > 8:
            return self._intensity
        if val == 0:
            self.off()
        else:
            self._intensity = val
            self.cmd((val<<4)|0x01)

    def on(self):
        self.cmd(self._intensity|0x01)

    def off(self):
        self._intensity = 0
        self.cmd(0)

    def clear(self):
        self.dat(0, 0)
        self.dat(1, 0)
        self.dat(2, 0)
        self.dat(3, 0)
        self.dbuf = [0, 0, 0, 0]
      
    def cmd(self, c):
        try:
            self.tbuf[0] = c
            self.i2c.writeto(0x24,self.tbuf)
        except:
            pass

    def dat(self, bit, d):
        try:
            self.tbuf[0] = d
            self.i2c.writeto(0x34 + bit%4,self.tbuf)
        except:
            pass
      
    def showbit(self, num, bit = 0):
        if num=='-':
            self.dat(bit, self._TM1650_MINUS)
        else:
            self.dbuf[bit%4] = self._TM1650_BUF[num%16]
            self.dat(bit, self._TM1650_BUF[num%16])

    def shownum(self, num):
        if self.num_len<4:
            self.dat(3-self.num_len, 0)
        if num < 0:
            if num<-999:
                num = -999
            self.dat(4-len(str(num)), self._TM1650_MINUS)   # '-'
            num = -num
        elif num > 9999:
            num = 9999
        self.num_len = len(str(num))
        num2str = str(num).strip('-')
        index = 0
        for i in num2str:
            self.showbit(int(i), 4-len(num2str)+index)
            index+=1

    def showDP(self, bit = 1, show = True):
        if show:
            self.dat(bit, self.dbuf[bit % 4] | 0x80)
        else:
            self.dat(bit, self.dbuf[bit % 4] & 0x7F)


'''传感器_IIC类_气压海拔传感器'''
class ENV2():
    _HP203N_ADDR = const(0x76)
    # HP203N Command Set
    _HP203N_SOFT_RST = const(0x06) # Soft reset the device
    _HP203N_ADC_CVT = const(0x40) # Perform ADC conversion
    _HP203N_READ_PT = const(0x10) # Read the temperature and pressure values
    _HP203N_READ_AT = const(0x11) # Read the temperature and altitude values
    _HP203N_READ_P = const(0x30) # Read the pressure value only
    _HP203N_READ_A = const(0x31) # Read the altitude value only
    _HP203N_READ_T = const(0x32) # Read the temperature value only
    _HP203N_ANA_CAL = const(0x28) # Re-calibrate the internal analog blocks
    _HP203N_READ_REG = const(0x80) # Read out the control registers
    _HP203N_WRITE_REG = const(0xC0) # Write in the control registers

    # OSR Configuration
    _HP203N_OSR_4096 = const(0x00) # Conversion time: 131.1ms
    _HP203N_OSR_2048 = const(0x04) # Conversion time: 65.6ms
    _HP203N_OSR_1024 = const(0x08) # Conversion time: 32.8ms
    _HP203N_OSR_512 = const(0xC0) # Conversion time: 16.4ms
    _HP203N_OSR_256 = const(0x10) # Conversion time: 8.2ms
    _HP203N_OSR_128 = const(0x14) # Conversion time: 4.1ms

    _HP203N_CH_PRESSTEMP = const(0x00) # Sensor Pressure and Temperature Channel 
    _HP203N_CH_TEMP = const(0x02) # Temperature Channel

    def __init__(self, iic = board.I2C()):
        try:
            self.i2c = iic
            self.i2c.try_lock()
            self.p_cnvrsn_config()
        except OSError:
            from screen import Screen
            import sys
            screens = Screen()
            screens.init()
            screens.autoRefresh(False)
            screens.setRotation(90)
            screens.fill((0, 0, 0))
            screens.rect(0,0,160,20,(255, 0, 0),1)
            screens.text('未检测ENV2模块！',5,5,1,(255, 255, 255))
            screens.text('请将ENV2模块连接到右侧',5,30,1,(255, 255, 255))
            screens.text('带有I2C标识的4针接口',5,50,1,(255, 255, 255))
            screens.refresh()
            sys.exit()
        except RuntimeError:
            from screen import Screen
            import sys
            screens = Screen()
            screens.init()
            screens.autoRefresh(False)
            screens.setRotation(90)
            screens.fill((0, 0, 0))
            screens.rect(0,0,160,20,(255, 0, 0),1)
            screens.text('I2C模块连接异常',5,5,1,(255, 255, 255))
            screens.text('请将右侧的4针I2C模块重新连接',5,30,1,(255, 255, 255))
            screens.text('然后再复位主板',5,50,1,(255, 255, 255))
            screens.refresh()
            sys.exit()

    def p_cnvrsn_config(self):
        """Select the OSR and Channel Configuration Command from the given provided value"""
        CNVRSN_CONFIG = bytearray([_HP203N_ADC_CVT | _HP203N_OSR_1024 | _HP203N_CH_PRESSTEMP])
        self.i2c.writeto(_HP203N_ADDR, CNVRSN_CONFIG)   
        
    def read_pres(self):
        """Read back data from _HP203N_READ_P(0x30), 3 bytes
        pressure MSB, pressure CSB, pressure LSB"""
        self.p_cnvrsn_config()
        data = bytearray(3)
        self.i2c.writeto(_HP203N_ADDR,bytearray([_HP203N_READ_P]))
        self.i2c.readfrom_into(_HP203N_ADDR,data)
        pressure = (((data[0] & 0x0F) <<16) + (data[1] <<8) + data[2]) / 100.00
        return pressure

    def read_temp(self):
        """Read back data from _HP203N_READ_T(0x32), 3 bytes
        pressure MSB, pressure CSB, pressure LSB"""
        self.p_cnvrsn_config()
        data = bytearray(3)
        self.i2c.writeto(_HP203N_ADDR,bytearray([_HP203N_READ_T]))
        self.i2c.readfrom_into(_HP203N_ADDR,data)
        cTemp = (((data[0] & 0x0F) <<16) + (data[1] <<8) + data[2]) / 100.00
        fTemp = (cTemp * 1.8) + 32
        return (cTemp,fTemp)

    def read_altitude(self):
        self.p_cnvrsn_config()
        data = bytearray(3)
        self.i2c.writeto(_HP203N_ADDR,bytearray([_HP203N_READ_A]))
        self.i2c.readfrom_into(_HP203N_ADDR,data)
        altitude = (((data[0] & 0x0F) << 16) + (data[1] << 8) + data[2]) / 10000.00
        return altitude



'''传感器_数字类_红外接收'''
class InfraRx:
    def __init__(self, pin, callback=None):
        
        self.pulsein = pulseio.PulseIn(usePin(pin), maxlen=120, idle_state=True)
        self.decoder = adafruit_irremote.GenericDecode()
        saveObj(pin,self.pulsein)
    def getInfraRxData(self):
        pulses = self.decoder.read_pulses(self.pulsein,blocking=False)
        if pulses:
            try:
                code = self.decoder.decode_bits(pulses)
                data = code[0] << 24 | code[1] << 16 | code[2] << 8 | code[3]
                return hex(data).split('0x')[1]
            except adafruit_irremote.IRNECRepeatException:  # unusual short code!
                return None
            except adafruit_irremote.IRDecodeException as e:     # failed to decode
                return None
            except:
                return None
        else:
            return None