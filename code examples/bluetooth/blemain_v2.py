# ble wireless programming in blocks v02 19.07.2024
import random, ubluetooth
from machine import Pin, Timer, PWM, ADC
from time import sleep_ms
      
class BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()
        self._write_callback = None

    def connected(self):        
        print('')

    def disconnected(self):        
        print('')

    def on_write(self, callback):
        self._write_callback = callback
        
    def ble_irq(self, event, data):
        if event == 1:
            '''Connected'''
            self.connected()

        elif event == 2:
            '''Disconnected'''
            self.advertiser()
            self.disconnected()

        elif event == 3:
            '''New message received'''            
            buffer = self.ble.gatts_read(self.tx)
            message = buffer.decode('UTF-8').strip()
            self._write_callback(buffer)

    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_READ)
        BLE_UART = (BLE_NUS, (BLE_TX,))
        SERVICES = (BLE_UART, )
        ((self.tx,), ) = self.ble.gatts_register_services(SERVICES)
    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '')
    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytes([0x02, 0x01, 0x02]) + bytes([len(name) + 1, 0x09]) + name)

ble = BLE("Otto")
i = 0
commandSet = bytearray(b'')
key = bytearray(b'EoChunk')
last_chars = b''

def on_rx(x):
    global i, commandSet, key, last_chars
    commandSet.extend(x)
    #ble.send(x)
    last_command = commandSet[:]
    last_chars = last_command[-len(key):]
    
    if last_chars == key:
        realCommand = commandSet[:-len(key)].decode("utf-8")
        try:
            exec(realCommand)
        except Exception as e:
            ble.send(e)
            print (e)
        commandSet = bytearray(b'')

ble.on_write(on_rx)
