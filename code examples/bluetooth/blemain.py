# ble wireless programming in blocks v01 16.06.2024
import bluetooth
import time
from machine import Pin, PWM
from ottoble import BLESimplePeripheral
from ottoneopixel import OttoNeoPixel

ring = OttoNeoPixel(4, 13)

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble, "6E400001-B5A3-F393-E0A9-E50E24DCCA9E", "6E400003-B5A3-F393-E0A9-E50E24DCCA9E", "6E400002-B5A3-F393-E0A9-E50E24DCCA9E","Otto")

i = 0
commandSet = bytearray(b'')
key = bytearray(b'EoChunk')
last_chars = b''

ring.fillAllRing(0, 255, 0)
      
def on_rx(x):
    global i, commandSet, key, last_chars
    commandSet.extend(x)
    print(x)
    last_command = commandSet[:]
    last_chars = last_command[-len(key):]
    
    if last_chars == key:
        realCommand = commandSet[:-len(key)].decode("utf-8")
        try:
            exec(realCommand)
        except Exception as e:
            print (e)
        commandSet = bytearray(b'')

sp.on_write(on_rx)