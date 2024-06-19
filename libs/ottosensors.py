# ottosensors v01 11.03.2024
import machine
from machine import Pin 
from machine import ADC

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
