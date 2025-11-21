import ubluetooth
import uasyncio as asyncio
import os
import gc
import sys
import machine
import util
import rc

FLAG_FILE = "code_stopper"

class BLE:
    def __init__(self):
        self.name = util.get_ble_name()
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self._write_callback = None
        self._code_stopper = None
        self.tx = None
        self.register()
        self.advertiser()
        self.ble.irq(self.ble_irq)

    def connected(self):
        # For implementing events that run on bluetooth connect event
        pass

    def disconnected(self):
        self.advertiser()

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


    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytes([0x02, 0x01, 0x06]) + bytes([len(name) + 1, 0x09]) + name
        self.ble.gap_advertise(100, adv_data)

    def register(self):
        NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_READ)
        BLE_UART = (BLE_NUS, (BLE_TX,))
        SERVICES = (BLE_UART,)
        ((self.tx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        print(data)

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
                    executor.ble_print(real_command)
                    import update_library
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

                    update_library.update_libraries(params[0], params[1], params[2], executor.ble_print)
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
        sys.print_exception(e)
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
