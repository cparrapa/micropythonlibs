
#!/usr/bin/env python3
# -*- coding: utf8 -*-

import digitalio
from time import sleep
from future import uartMap
from board_map import usePin, saveObj


__version__ = "1.0.2"

class Keypad:

    def __init__(self, uart, inputs=16):
        self.map = {
            3:"1",15:"2",4:"3",8:"A",2:"4",14:"5",5:"6",9:"B",1:"7",13:"8",6:"9",10:"C",0:"*",12:"0",7:"#",11:"D",-1:None
        }
        self._scl_pin = digitalio.DigitalInOut(usePin(uartMap[uart][0]))
        self._scl_pin.switch_to_output()
        self._sdo_pin = digitalio.DigitalInOut(usePin(uartMap[uart][1]))
        self._sdo_pin.switch_to_input()
        saveObj(uartMap[uart][0],self._scl_pin)
        saveObj(uartMap[uart][1],self._sdo_pin)
        
        self._inputs = inputs
    
    def read(self):
        key = [1] * self._inputs
        self._scl_pin.value = 1
        sleep(0.001)
        for i in range(self._inputs):
            self._scl_pin.value = 0
            sleep(0.001)
            key[i] = self._sdo_pin.value
            self._scl_pin.value = 1
            sleep(0.001)
        sleep(0.001)
        key_single = -1
        for i in range(self._inputs):
            if key[i] == 0:
                key_single = i
                break
        
        return self.map[key_single]
    