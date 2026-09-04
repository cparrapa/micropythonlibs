# main.py v0.1.5 4.9.26 added intro animation
import gc
import os
import sys
from binascii import a2b_base64
from time import sleep_ms

import machine
from machine import Pin
import uasyncio as asyncio
import ubinascii
import ubluetooth
import ujson
import uselect
import util
from ottobuzzer import OttoBuzzer
from neopixel import NeoPixel
ring = NeoPixel(Pin(4), 13)  #Connector 5
# Bytes that signal a standard MicroPython REPL client (e.g. Thonny, mpremote)
# is trying to talk to us. The Otto protocol never sends these.
#   0x01 = Ctrl+A (raw REPL)
#   0x02 = Ctrl+B (friendly REPL)
#   0x04 = Ctrl+D (soft reset)
#   0x05 = Ctrl+E (paste mode)
_REPL_HANDSHAKE_BYTES = (0x01, 0x02, 0x04, 0x05)


def _poll_for_repl_handshake(timeout_ms):
    try:
        poll = uselect.poll()
        poll.register(sys.stdin, uselect.POLLIN)
        if not poll.poll(timeout_ms):
            return False
        first = sys.stdin.read(1)
        return bool(first) and ord(first) in _REPL_HANDSHAKE_BYTES
    except Exception:
        return False

_buzzer = None

def _get_buzzer():
    global _buzzer
    if _buzzer is None:
        _buzzer = OttoBuzzer(25)
    return _buzzer

def _restore_motors():
    try:
        rc = sys.modules['rc']
        rc.motor.leftServo.freq(50)
        rc.motor.leftServo.duty(0)
        rc.motor.rightServo.freq(50)
        rc.motor.rightServo.duty(0)
    except (KeyError, AttributeError):
        pass

class BLE:
    def __init__(self):
        self.name = util.get_ble_name()
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self._advertising_animation = None
        self._connected = False
        self.ble.config(gap_name=self.name[:26])  # Set GAP_NAME (ak PLATFORM NAME)
        self._write_callback = None
        self._code_stopper = None
        self.rx = None
        self.tx = None
        self.register()
        self.advertiser()
        self.ble.irq(self.ble_irq)

    async def _waiting_animation(self):
        """Breathing blue ring while waiting for BLE connection."""
        brightness = 0
        direction = 10

        while not self._connected:
            for i in range(13):
                ring[i] = (0, 0, brightness)

            ring.write()

            brightness += direction

            if brightness >= 80:
                brightness = 80
                direction = -10
            elif brightness <= 0:
                brightness = 0
                direction = 10

            await asyncio.sleep_ms(50)

        ring.fill((0, 0, 0))
        ring.write()

    def _start_waiting_animation(self):
        if self._advertising_animation is None:
            self._connected = False
            buzzer = _get_buzzer()
            buzzer.play_emoji("button")
            buzzer.clear_buzzer()
            ring.fill((255, 0, 0))
            ring.write()
            sleep_ms(500)
            ring.fill((0, 255, 0))
            ring.write()
            sleep_ms(500)
            self._advertising_animation = asyncio.create_task(
                self._waiting_animation()
            )

    def _stop_waiting_animation(self):
        self._connected = True
        ring.fill((0,255,0))
        ring.write()
        self._advertising_animation = None
        
    def connected(self):
        # Turn off advertisting after successfull connect
        self._stop_waiting_animation()
        self.ble.gap_advertise(None)
        asyncio.create_task(self._buzz_connect())

    def disconnected(self):
        asyncio.create_task(self._buzz_disconnect())
        asyncio.create_task(self.re_advertise())

    async def _buzz_connect(self):
        buzzer = _get_buzzer()
        buzzer.play_emoji("connect")
        buzzer.clear_buzzer()
        _restore_motors()

    async def _buzz_disconnect(self):
        buzzer = _get_buzzer()
        buzzer.play_emoji("disconnect")
        buzzer.clear_buzzer()
        _restore_motors()

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
            conn_handle, attr_handle = data
            buffer = self.ble.gatts_read(attr_handle)

            if attr_handle == self.tx:
                self.ble.gatts_write(self.tx, b'')

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

        self._start_waiting_animation()

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
        RX_UUID = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
        TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_READ)
        BLE_UART = (BLE_NUS, (BLE_RX, BLE_TX,))
        SERVICES = (BLE_UART,)
        ((self.rx, self.tx,),) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.ble.gatts_notify(0, self.tx, data)


BLOCK_RESET_FLAG = "block_reset"


class UsercodeManager:
    FLAG_FILE = "code_stopper"

    @staticmethod
    def should_run():
        if "usercode.py" not in os.listdir():
            return False
        try:
            os.stat(UsercodeManager.FLAG_FILE)
            return False
        except:
            return True

    @staticmethod
    def run():
        if "usercode.py" not in os.listdir():
            return
        sleep_ms(1000)
        try:
            with open("usercode.py", "r") as f:
                code = f.read()
            exec(code)
        except Exception as e:
            print(e)

    @staticmethod
    def create_interrupt_callback():
        def callback():
            try:
                with open(UsercodeManager.FLAG_FILE, 'w') as f:
                    f.write('1')
            except:
                pass
            machine.reset()
        return callback

    @staticmethod
    def clear_flag():
        try:
            os.remove(UsercodeManager.FLAG_FILE)
        except:
            pass


class CommandRouter:
    def __init__(self, ble):
        self.ble = ble
        self.stop_flag = False
        self.exec_running = False
        self._command_set = bytearray()
        self._serial_command_set = bytearray()
        self._key = bytearray(b'~')

    def on_rx(self, buffer):
        self.stop_flag = True

        # Remote control is not executed through python code but through short keys
        # That start with @, so that we can recognize them here
        if buffer.decode("utf-8")[0] == "@":
            code = buffer.decode("utf-8")
            rc = __import__("rc")
            rc.remote_control(code[1:], self.ble_print, self.exec_running)
            return

        # This piece takes care of the usual python code executed through the blocks section
        self._command_set.extend(buffer)
        last_chars = self._command_set[-len(self._key):]

        if last_chars == self._key:
            command = self._command_set[:-len(self._key)].decode("utf-8")
            self._command_set = bytearray()
            self._route_command(command, self.ble_print, self.ble_print_async)

    def on_serial_line(self, line):
        self.stop_flag = True

        if len(self._serial_command_set) == 0 and line.startswith("@"):
            rc = __import__("rc")
            rc.remote_control(line[1:], self.serial_print, self.exec_running)
            return

        if line == "~":
            command = self._serial_command_set.decode("utf-8")
            self._serial_command_set = bytearray()
            self._route_command(command, self.serial_print, self.serial_print_async)
            return

        if len(self._serial_command_set) > 0:
            self._serial_command_set.extend(b'\n')
        self._serial_command_set.extend(line.encode("utf-8"))

    def _route_command(self, command, output_fn, output_fn_async):
        stripped_command = command.strip()
        if stripped_command == "#close#":
            output_fn("Execution stopped")
        elif stripped_command.startswith("update_firmware("):
            self._handle_update_firmware(command, output_fn)
        elif stripped_command.startswith("update("):
            self._handle_update(command, output_fn)
        elif stripped_command.startswith("usercode_save("):
            self._handle_usercode_save(command, output_fn)
        elif stripped_command == "usercode_remove":
            self._handle_usercode_remove(output_fn)
        elif stripped_command.startswith("set_ble_name("):
            self._handle_set_ble_name(command, output_fn)
        else:
            self._handle_exec(command, output_fn, output_fn_async)

    def _handle_update_firmware(self, command, output_fn):
        import update_library
        manager = update_library.UpdateLibraryManager(output_fn)
        params = self._parse_quoted_params(command)
        manager.trigger_update_libraries(params[0], params[1], params[2], params[3])

    def _handle_update(self, command, output_fn):
        import update_library
        manager = update_library.UpdateLibraryManager(output_fn)
        json_data = ujson.loads(ubinascii.a2b_base64(command.split("(")[1].split(")")[0]).decode())
        manager.trigger_update_libraries(json_data["ssid"], json_data["pass"], json_data["id"], json_data["url"])

    def _handle_usercode_save(self, command, output_fn):
        try:
            b64_data = command.split("(")[1].split(")")[0]
            code = a2b_base64(b64_data).decode("utf-8")
            with open("usercode.py", "w") as f:
                f.write(code)
            UsercodeManager.clear_flag()
            output_fn("s:usercode_saved")
        except Exception as e:
            output_fn(f"u:{e}")

    def _handle_usercode_remove(self, output_fn):
        try:
            os.remove("usercode.py")
        except:
            pass
        UsercodeManager.clear_flag()
        output_fn("s:usercode_removed")

    def _handle_set_ble_name(self, command, output_fn):
        params = self._parse_quoted_params(command)

        async def set_name_async(name):
            util.set_ble_name(name)
            output_fn(f"n:{name}")

        asyncio.create_task(set_name_async(params[0]))

    def _handle_exec(self, command, output_fn, output_fn_async):
        asyncio.create_task(self._exec_command(command, output_fn, output_fn_async))

    async def _exec_command(self, command, output_fn, output_fn_async):
        self.stop_flag = False
        gc.collect()

        try:
            rc = __import__("rc")

            def exec_print(*args, **kwargs):
                separator = kwargs.get("sep", " ")
                output_fn_async("b:" + separator.join(map(str, args)))

            exec_globals = {
                'print': exec_print,
                'rc': rc,
                'stop_flag': lambda: self.stop_flag
            }

            self.exec_running = True
            exec(command, exec_globals)
        except Exception as e:
            output_fn(f"u:{e}")
        finally:
            self.exec_running = False

    @staticmethod
    def _parse_quoted_params(text):
        params = []
        in_quotes = False
        current_param = ""

        for char in text:
            if char == '"':
                if in_quotes:
                    params.append(current_param)
                    current_param = ""
                in_quotes = not in_quotes
            elif in_quotes:
                current_param += char

        return params

    def ble_print_async(self, *args, **kwargs):
        sleep_ms(10)
        message = " ".join(map(str, args))
        self.ble.send(message)

    def ble_print(self, *args, **kwargs):
        message = " ".join(map(str, args))
        self.ble.send(message)

    def serial_print(self, *args, **kwargs):
        message = " ".join(map(str, args))
        print(message)

    def serial_print_async(self, *args, **kwargs):
        sleep_ms(10)
        message = " ".join(map(str, args))
        print(message)


async def serial_reader_task(router):
    # Read one char at a time so we can detect REPL handshake bytes
    # (Ctrl+A/B/D/E) and hand the serial channel back to MicroPython's
    # built-in REPL when a tool like Thonny connects.
    # Note: on MicroPython sys.stdin is a text stream, so reads return str.
    sreader = asyncio.StreamReader(sys.stdin)
    buf = []
    while True:
        chunk = await sreader.read(1)
        if not chunk:
            continue
        ch = chunk[0]
        b = ord(ch)
        if b in _REPL_HANDSHAKE_BYTES:
            return
        if b == 0x0D:
            continue
        if b == 0x0A:
            router.on_serial_line("".join(buf))
            buf = []
        else:
            buf.append(ch)


async def ble_operation_task(ble=None):
    if ble is None:
        ble = BLE()
    router = CommandRouter(ble)
    ble.on_write(router.on_rx)
    serial_task = asyncio.create_task(serial_reader_task(router))

    # Check if this boot follows a block reset (Ctrl+C interrupt)
    try:
        os.stat(BLOCK_RESET_FLAG)
        os.remove(BLOCK_RESET_FLAG)
        # Wait for serial to stabilize, then notify frontend
        await asyncio.sleep(1)
        router.serial_print("r:f")
        try:
            router.ble_print("r:f")
        except:
            pass
    except OSError:
        pass

    while True:
        await asyncio.sleep_ms(200)
        # serial_reader_task returns when it detects a REPL handshake byte
        # (Ctrl+A/B/D/E). Unwind so main() exits and the built-in REPL runs.
        if serial_task.done():
            return


async def main():
    if UsercodeManager.should_run():
        ble = BLE()
        ble.code_stopper_func(UsercodeManager.create_interrupt_callback())
        UsercodeManager.run()
        await ble_operation_task(ble)
    else:
        UsercodeManager.clear_flag()
        await ble_operation_task()

def _clear_hardware():
    try:
        rc = sys.modules['rc']
        rc.buzzer.clear_buzzer()
        rc.ring.clearRGB()
        rc.ultrasonic.clearultrasonicRGB()
        rc.motor.Stop(1)
    except (KeyError, AttributeError):
        pass

while True:
    try:
        asyncio.run(main())
        # main() returned cleanly because the serial reader saw a
        # REPL handshake byte. Drop out and let MicroPython's REPL take over.
        break
    except KeyboardInterrupt:
        _clear_hardware()
        try:
            with open("code_stopper", "w") as f:
                f.write("1")
            with open(BLOCK_RESET_FLAG, "w") as f:
                f.write("1")
        except:
            pass
        # Thonny opens with Ctrl+C before its Ctrl+B handshake. If a REPL
        # handshake byte arrives right after the interrupt, exit to REPL
        # instead of looping back into the Otto protocol.
        if _poll_for_repl_handshake(300):
            break
