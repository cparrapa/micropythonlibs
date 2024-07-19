'''
ottolight.py v00 19/07/24
a library for the photoresistor module
v00 Alex Etchells
'''
from machine import Pin,ADC


class LightSensor:
    def __init__(self, connector=5):
        connectorPin = [None,None,None,None,26,4,32,33,27,15,14,13] #GPIO pin for the 3pin connectors (4 to 11)
        self.adc=ADC(Pin(connectorPin[connector]))
        self.adc.atten(ADC.ATTN_11DB)
        self.adc.width(ADC.WIDTH_12BIT)
    
    #return a value from 0 to 100
    def Read(self):
        # 0 to 4095 where 4095 is dark
        adcValue=self.adc.read()
        try:
            return int((4095-adcValue)/40.95)
        except:
            return -1
          
