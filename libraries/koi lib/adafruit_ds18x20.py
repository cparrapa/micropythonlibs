__version__ = "1.0.0"

import onewireio
from micropython import const
from board_map import usePin, saveObj

try:
    from typing import Optional, List, Tuple
    from circuitpython_typing import ReadableBuffer, WriteableBuffer
    from microcontroller import Pin
except ImportError:
    pass

_SEARCH_ROM = const(0xF0)
_MATCH_ROM = const(0x55)
_SKIP_ROM = const(0xCC)
_MAX_DEV = const(10)


class OneWireError(Exception):
    """A class to represent a 1-Wire exception."""


class OneWireAddress:
    """A class to represent a 1-Wire address."""

    def __init__(self, rom: bytearray) -> None:
        self._rom = rom

    @property
    def rom(self) -> bytearray:
        """The unique 64 bit ROM code."""
        return self._rom

    @property
    def crc(self) -> int:
        """The 8 bit CRC."""
        return self._rom[7]

    @property
    def serial_number(self) -> bytearray:
        """The 48 bit serial number."""
        return self._rom[1:7]

    @property
    def family_code(self) -> int:
        """The 8 bit family code."""
        return self._rom[0]


class OneWireBus:
    """A class to represent a 1-Wire bus."""

    def __init__(self, pin: Pin) -> None:
        # pylint: disable=no-member
        self._ow = onewireio.OneWire(pin)
        self._readbit = self._ow.read_bit
        self._writebit = self._ow.write_bit
        self._maximum_devices = _MAX_DEV

    @property
    def maximum_devices(self) -> int:
        """The maximum number of devices the bus will scan for. Valid range is 1 to 255.
        It is an error to have more devices on the bus than this number. Having less is OK.
        """
        return self._maximum_devices

    @maximum_devices.setter
    def maximum_devices(self, count: int) -> None:
        if not isinstance(count, int):
            raise ValueError("Maximum must be an integer value 1 - 255.")
        if count < 1 or count > 0xFF:
            raise ValueError("Maximum must be an integer value 1 - 255.")
        self._maximum_devices = count

    def reset(self, required: bool = False) -> bool:
        """
        Perform a reset and check for presence pulse.

        :param bool required: require presence pulse
        """
        reset = self._ow.reset()
        if required and reset:
            raise OneWireError("No presence pulse found. Check devices and wiring.")
        return not reset

    def readinto(
        self, buf: WriteableBuffer, *, start: int = 0, end: Optional[int] = None
    ) -> None:
        """
        Read into ``buf`` from the device. The number of bytes read will be the
        length of ``buf``.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buf[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.

        :param ~WriteableBuffer buf: Buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include
        """
        if end is None:
            end = len(buf)
        for i in range(start, end):
            buf[i] = self._readbyte()

    def write(
        self, buf: ReadableBuffer, *, start: int = 0, end: Optional[int] = None
    ) -> None:
        """
        Write the bytes from ``buf`` to the device.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.

        :param ReadableBuffer buf: Buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include
        """
        if end is None:
            end = len(buf)
        for i in range(start, end):
            self._writebyte(buf[i])

    def scan(self) -> List[OneWireAddress]:
        """Scan for devices on the bus and return a list of addresses."""
        devices = []
        diff = 65
        rom = None
        count = 0
        for _ in range(0xFF):
            rom, diff = self._search_rom(rom, diff)
            if rom:
                count += 1
                if count > self.maximum_devices:
                    raise RuntimeError(
                        "Maximum device count of {} exceeded.".format(
                            self.maximum_devices
                        )
                    )
                devices.append(OneWireAddress(rom))
            if diff == 0:
                break
        return devices

    def _readbyte(self) -> int:
        val = 0
        for i in range(8):
            val |= self._ow.read_bit() << i
        return val

    def _writebyte(self, value: int) -> None:
        for i in range(8):
            bit = (value >> i) & 0x1
            self._ow.write_bit(bit)

    def _search_rom(
        self, l_rom: Optional[ReadableBuffer], diff: int
    ) -> Tuple[bytearray, int]:
        if not self.reset():
            return None, 0
        self._writebyte(_SEARCH_ROM)
        if not l_rom:
            l_rom = bytearray(8)
        rom = bytearray(8)
        next_diff = 0
        i = 64
        for byte in range(8):
            r_b = 0
            for bit in range(8):
                b = self._readbit()
                if self._readbit():
                    if b:  # there are no devices or there is an error on the bus
                        return None, 0
                else:
                    if not b:  # collision, two devices with different bit meaning
                        if diff > i or ((l_rom[byte] & (1 << bit)) and diff != i):
                            b = 1
                            next_diff = i
                self._writebit(b)
                r_b |= b << bit
                i -= 1
            rom[byte] = r_b
        return rom, next_diff

    @staticmethod
    def crc8(data: ReadableBuffer) -> int:
        """
        Perform the 1-Wire CRC check on the provided data.

        :param ReadableBuffer data: 8 byte array representing 64 bit ROM code
        """
        crc = 0

        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x01:
                    crc = (crc >> 1) ^ 0x8C
                else:
                    crc >>= 1
                crc &= 0xFF
        return crc

try:
    from typing import Optional, Type
    from circuitpython_typing import ReadableBuffer, WriteableBuffer
    from types import TracebackType
except ImportError:
    pass


class OneWireDevice:
    """A class to represent a single device on the 1-Wire bus."""

    def __init__(self, bus: OneWireBus, address: OneWireAddress):
        self._bus = bus
        self._address = address

    def __enter__(self) -> "OneWireDevice":
        self._select_rom()
        return self

    def __exit__(
        self,
        exception_type: Optional[Type[type]],
        exception_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> bool:
        return False

    def readinto(
        self, buf: WriteableBuffer, *, start: int = 0, end: Optional[int] = None
    ) -> None:
        """
        Read into ``buf`` from the device. The number of bytes read will be the
        length of ``buf``.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buf[start:end]``. This will not cause an allocation like
        ``buf[start:end]`` will so it saves memory.

        :param WriteableBuffer buf: Buffer to write into
        :param int start: Index to start writing at
        :param int end: Index to write up to but not include
        """
        self._bus.readinto(buf, start=start, end=end)
        if start == 0 and end is None and len(buf) >= 8:
            if self._bus.crc8(buf):
                raise RuntimeError("CRC error.")

    def write(
        self, buf: ReadableBuffer, *, start: int = 0, end: Optional[int] = None
    ) -> None:
        """
        Write the bytes from ``buf`` to the device.

        If ``start`` or ``end`` is provided, then the buffer will be sliced
        as if ``buffer[start:end]``. This will not cause an allocation like
        ``buffer[start:end]`` will so it saves memory.

        :param ReadableBuffer buf: buffer containing the bytes to write
        :param int start: Index to start writing from
        :param int end: Index to read up to but not include
        """
        return self._bus.write(buf, start=start, end=end)

    def _select_rom(self) -> None:
        self._bus.reset()
        self.write(b'\x55')
        self.write(self._address.rom)

import time
from micropython import const

try:
    import typing  # pylint: disable=unused-import
    from typing_extensions import Literal
    from circuitpython_typing import WriteableBuffer
except ImportError:
    pass

_CONVERT = b"\x44"
_RD_SCRATCH = b"\xBE"
_WR_SCRATCH = b"\x4E"
_CONVERSION_TIMEOUT = const(1)
RESOLUTION = (9, 10, 11, 12)
# Maximum conversion delay in seconds, from DS18B20 datasheet.
_CONVERSION_DELAY = {9: 0.09375, 10: 0.1875, 11: 0.375, 12: 0.750}


class DS18X20:

    def __init__(self,pin) -> None:
        ow_bus = OneWireBus(usePin(pin))
        saveObj(pin,ow_bus._ow)
        self.historyValue = 0

        address = ow_bus.scan()[0]
        if address.family_code in (0x10, 0x28):
            self._address = address
            self._device = OneWireDevice(ow_bus, address)
            self._buf = bytearray(9)
            self._conv_delay = _CONVERSION_DELAY[12]  # pessimistic default
        else:
            raise ValueError("Incorrect family code in device address.")

    @property
    def temperature(self):
        """The temperature in degrees Celsius."""
        self._convert_temp()
        try:
            value = round(self._read_temp(),2)
            self.historyValue = value
            return value
        except RuntimeError:
            return self.historyValue

    @property
    def resolution(self) -> Literal[9, 10, 11, 12]:
        """The programmable resolution. 9, 10, 11, or 12 bits."""
        return RESOLUTION[self._read_scratch()[4] >> 5 & 0x03]

    @resolution.setter
    def resolution(self, bits: Literal[9, 10, 11, 12]) -> None:
        if bits not in RESOLUTION:
            raise ValueError("Incorrect resolution. Must be 9, 10, 11, or 12.")
        self._buf[0] = 0  # TH register
        self._buf[1] = 0  # TL register
        self._buf[2] = RESOLUTION.index(bits) << 5 | 0x1F  # configuration register
        self._write_scratch(self._buf)

    def _convert_temp(self, timeout: int = _CONVERSION_TIMEOUT) -> float:
        with self._device as dev:
            dev.write(_CONVERT)
            start_time = time.monotonic()
            if timeout > 0:
                dev.readinto(self._buf, end=1)
                # 0 = conversion in progress, 1 = conversion done
                while self._buf[0] == 0x00:
                    if time.monotonic() - start_time > timeout:
                        raise RuntimeError(
                            "Timeout waiting for conversion to complete."
                        )
                    dev.readinto(self._buf, end=1)
        return time.monotonic() - start_time

    def _read_temp(self) -> float:
        # pylint: disable=invalid-name
        buf = self._read_scratch()
        if self._address.family_code == 0x10:
            if buf[1]:
                t = buf[0] >> 1 | 0x80
                t = -((~t + 1) & 0xFF)
            else:
                t = buf[0] >> 1
            return t - 0.25 + (buf[7] - buf[6]) / buf[7]
        t = buf[1] << 8 | buf[0]
        if t & 0x8000:  # sign bit set
            t = -((t ^ 0xFFFF) + 1)
        return t / 16

    def _read_scratch(self) -> bytearray:
        with self._device as dev:
            dev.write(_RD_SCRATCH)
            dev.readinto(self._buf)
        return self._buf

    def _write_scratch(self, buf: WriteableBuffer) -> None:
        with self._device as dev:
            dev.write(_WR_SCRATCH)
            dev.write(buf, end=3)

    def start_temperature_read(self) -> float:
        """Start asynchronous conversion, returns immediately.
        Returns maximum conversion delay [seconds] based on resolution."""
        with self._device as dev:
            dev.write(_CONVERT)
        return _CONVERSION_DELAY[self.resolution]

    def read_temperature(self) -> float:
        """Read the temperature. No polling of the conversion busy bit
        (assumes that the conversion has completed)."""
        return self._read_temp()