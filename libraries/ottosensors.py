# ottosensors v2.0 23.10.2024
'''
added ottolight.py from Alex Etchells
added dht
'''
import machine, dht
from machine import Pin, ADC

class FollowLine:
        
    def __init__(self, pin1, pin2, pin3, pin4):
        self.analogL=ADC(Pin(pin1))                 
        self.analogR=ADC(Pin(pin2))  
        self.digitalL = machine.Pin((pin3), machine.Pin.IN)
        self.digitalR = machine.Pin((pin4), machine.Pin.IN)    
            
    def detectLineLeft(self):
        return self.digitalL.value()

    def detectLineRight(self):
        return self.digitalR.value()

    def readLineLeft(self):
        return self.analogL.read()

    def readLineRight(self):
        return self.analogR.read()

class DHT:

    def __init__(self, pin):
        self.d = dht.DHT11(Pin(pin))
         
    def temperature(self):
        try:
            self.d.measure()
            temp=self.d.temperature()
            return (temp)
        except OSError as e:
            print('Failed to read temp sensor.')
            return "0"
        
    def humidity(self):
        try:
            self.d.measure()
            hum=self.d.humidity()
            return (hum)
        except OSError as e:
            print('Failed to read temp sensor.')
            return "0"
        
class Percentage:
    def __init__(self, connector=5):
        connectorPin = [None,None,None,None,26,4,32,33,27,15,14,13] #GPIO pin for the 3pin connectors (4 to 11)
        self.adc=ADC(Pin(connectorPin[connector]))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
    
    #return a value from 0 to 100
    def Read(self):
        try:
            # 0 to 4095 where 4095 is dark
            adcValue=self.adc.read()
            return int((4095-adcValue)/40.95)
        except:
            return -1
