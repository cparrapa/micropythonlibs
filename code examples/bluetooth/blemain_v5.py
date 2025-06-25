# ble wireless programming in blocks v05 5.03.2025 it has a bug that locks usb communication
import ubluetooth, time
import uasyncio as asyncio
from machine import Pin

from neopixel import NeoPixel
from ottobuzzer import Player
ring = NeoPixel(Pin(4), 13)
ring.fill((0,255,0))
ring.write()

nm = 64
matrix = NeoPixel(Pin(22), nm)
brightm = 0.2 
led = Pin(2, Pin.OUT)

def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(nm):
            rc_index = (i * 256 // nm) + j
            matrix[i] = wheel(rc_index & 255)
        matrix.write()
        time.sleep_ms(wait)

class BLE:
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self._write_callback = None
        self.tx = None
        self.register()
        self.advertiser()
        self.ble.irq(self.ble_irq)

    def connected(self):
        print("BLE Connected")

    def disconnected(self):
        print("BLE Disconnected")
        self.advertiser()

    def on_write(self, callback):
        self._write_callback = callback

    def ble_irq(self, event, data):
        if event == 1:  # Connected
            self.connected()
        elif event == 2:  # Disconnected
            self.disconnected()
        elif event == 3:  # New message received
            if self._write_callback:
                buffer = self.ble.gatts_read(self.tx)
                self._write_callback(buffer)

    def register(self):
        # Nordic UART Service (NUS)
        NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_READ)
        BLE_UART = (BLE_NUS, (BLE_TX,))
        SERVICES = (BLE_UART,)
        ((self.tx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytes([0x02, 0x01, 0x02]) + bytes([len(name) + 1, 0x09]) + name)

class CommandExecutor:
    def __init__(self, ble, player):
        self.ble = ble
        self.player = player  
        self.stop_flag = False

    async def exec_command(self, command):
        self.stop_flag = False
        try:
            # Pass global variables to exec
            exec_globals = {
                'nm': nm,
                'matrix': matrix,
                'wheel': wheel,
                'rainbow_cycle': rainbow_cycle,
                'time': time,  # add time module
                'Pin': Pin,
                'led': led,
                'stop_flag': lambda: self.stop_flag,
                'print': self.ble_print,
                'player': self.player  
            }
            exec(command, exec_globals)
        except Exception as e:
            self.ble_print(f"Error: {e}")
        finally:
            if self.stop_flag:
                self.player.stop()  

    def ble_print(self, *args, **kwargs):
        message = " ".join(map(str, args))
        self.ble.send(message)


def on_rx(executor, key):
    command_set = bytearray()
    last_chars = b''

    def callback(buffer):
        nonlocal command_set, last_chars
        command_set.extend(buffer)
        last_chars = command_set[-len(key):]

        if last_chars == key:
            real_command = command_set[:-len(key)].decode("utf-8")
            command_set = bytearray()

            if real_command.strip() == "#close#":
                executor.stop_flag = True
                executor.player.stop()  
                executor.ble_print("Execution stopped")
                for i in range(nm):
                    matrix[i] = (0, 0, 0)
                matrix.write()
            else:
                asyncio.create_task(executor.exec_command(real_command))

    return callback


async def main():
    ble = BLE("Otto")
    player = Player(pin_TX=16, pin_RX=17)  
    executor = CommandExecutor(ble, player)  
    key = bytearray(b'EoChunk')
    ble.on_write(on_rx(executor, key))

    while True:
        await asyncio.sleep(1)  # Continue the main loop

# Start the application
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program terminated")