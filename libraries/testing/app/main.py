import ubluetooth
import uasyncio as asyncio
import os
import gc
import machine
import util
import rc
import ubinascii
import ujson
from binascii import a2b_base64

FLAG_FILE = "code_stopper"

class BLE:
    def __init__(self):
        self.name = util.get_ble_name()
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=self.name[:26]) # Set GAP_NAME (ak PLATFORM NAME)
        self._write_callback = None
        self._code_stopper = None
        self.tx = None
        self.register()
        self.advertiser()
        self.ble.irq(self.ble_irq)

    def connected(self):
        # Turn off advertisting after successfull connect
        self.ble.gap_advertise(None)

    def disconnected(self):
        asyncio.create_task(self.re_advertise())

    def code_stopper_func(self, callback):
        self._code_stopper = callback

    def on_write(self, callback):
        self._write_callback = callback

    def ble_irq(self, event, data):
        if event == 1:
            self.connected()
        elif event == 2:
            self.disconnected()
        elif event == 3:
            buffer = self.ble.gatts_read(self.tx)

            if buffer.decode("utf-8") == "":
                if self._code_stopper:
                    self._code_stopper() # calls machine reset
            elif self._write_callback:
                self._write_callback(buffer)

    async def re_advertise(self):
        await asyncio.sleep_ms(500)
        self.advertiser()

    def advertiser(self):
        # Turn off advertising before starting new
        try:
            self.ble.gap_advertise(None)
        except:
            pass

        name = bytes(self.name, 'UTF-8')
        # Take only first 26 bytes of name, if it is longer
        if len(name) > 26:
            name = name[:26]

        nus_uuid = ubluetooth.UUID('6e400001-b5a3-f393-e0a9-e50e24dcca9e')
        uuid_bytes = bytes(nus_uuid)

        adv_data = bytearray()
        adv_data += bytes([0x02, 0x01, 0x06])
        adv_data += bytes([len(uuid_bytes) + 1, 0x07]) + uuid_bytes
        resp_data = bytes([len(name) + 1, 0x09]) + name

        self.ble.gap_advertise(100, adv_data, resp_data=resp_data)

    def register(self):
        NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_READ)
        BLE_UART = (BLE_NUS, (BLE_TX,))
        SERVICES = (BLE_UART,)
        ((self.tx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.ble.gatts_notify(0, self.tx, data)


class CommandExecutor:
    def __init__(self, ble):
        self.ble = ble
        self.stop_flag = False

    async def exec_command(self, command):
        self.stop_flag = False
        gc.collect()

        try:
            exec_globals = {
                'print': self.ble_print,
                'rc': rc,
                'stop_flag': lambda: self.stop_flag
            }

            exec(command, exec_globals)
        except Exception as e:
            self.ble_print(f"Error: {e}")

    def ble_print(self, *args, **kwargs):
        message = " ".join(map(str, args))
        self.ble.send(message)

def on_rx(executor, key):
    command_set = bytearray()
    last_chars = b''

    def callback(buffer):
        executor.stop_flag = True

        # Remote control is not executed through python code but through short keys
        # That start with @, so that we can recognize them here
        if buffer.decode("utf-8")[0] == "@":
            code = buffer.decode("utf-8")
            rc.remote_control(code[1:], executor.ble_print)
            return

        # This piece takes care of the usual python code executed through the blocks section
        nonlocal command_set, last_chars
        command_set.extend(buffer)
        last_chars = command_set[-len(key):]

        if last_chars == key:
            real_command = command_set[:-len(key)].decode("utf-8")
            command_set = bytearray()

            if real_command.strip() == "#close#":
                executor.ble_print("Execution stopped")
            else:
                if "update_firmware" in real_command:
                    import update_library
                    manager = update_library.UpdateLibraryManager(executor.ble_print)
                    params = []
                    in_quotes = False
                    current_param = ""

                    for char in real_command:
                        if char == '"':
                            if in_quotes:  # End of a parameter
                                params.append(current_param)
                                current_param = ""
                            in_quotes = not in_quotes
                        elif in_quotes:
                            current_param += char

                    manager.trigger_update_libraries(params[0], params[1], params[2], params[3])
                elif "update(" in real_command:
                    import update_library
                    manager = update_library.UpdateLibraryManager(executor.ble_print)
                    json_data = ujson.loads(ubinascii.a2b_base64(real_command.split("(")[1].split(")")[0]).decode())
                    manager.trigger_update_libraries(json_data["ssid"], json_data["pass"], json_data["id"], json_data["url"])
                elif "set_ble_name" in real_command:
                    import util
                    params = []
                    in_quotes = False
                    current_param = ""

                    for char in real_command:
                        if char == '"':
                            if in_quotes:  # End of a parameter
                                params.append(current_param)
                                current_param = ""
                            in_quotes = not in_quotes
                        elif in_quotes:
                            current_param += char
                    util.set_ble_name(params[0])
                else:
                    asyncio.create_task(executor.exec_command(real_command))

    return callback


def run_usercode():
    exists = "usercode.py" in os.listdir()

    if not exists:
        return False

    try:
        with open("usercode.py", "r") as f:
            code = f.read()

        exec(code)
        return
    except Exception as e:
        print(e)
        return


async def ble_operation_task():
    ble = BLE()
    executor = CommandExecutor(ble)
    key = bytearray(b'~')
    ble.on_write(on_rx(executor, key))

    while True:
        await asyncio.sleep(1)


def should_run_usercode():
    exists = "usercode.py" in os.listdir()
    if not exists:
        return False

    try:
        os.stat(FLAG_FILE)
        return False
    except:
        return True


async def main():
    if should_run_usercode():
        ble = BLE()

        def ble_interrupt_callback():
            try:
                with open(FLAG_FILE, 'w') as f:
                    f.write('1')
            except:
                pass
            machine.reset()

        ble.code_stopper_func(ble_interrupt_callback)

        run_usercode()

        await ble_operation_task()
    else:
        try:
            os.remove(FLAG_FILE)
        except:
            pass

        await ble_operation_task()

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Program terminated")
