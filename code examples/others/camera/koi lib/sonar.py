import re
import digitalio
import time
from board_map import usePin, saveObj

__version__ = "1.0.1"


class MeowSonar:
    def __init__(self, pin, timeout=100000000):
        self.pin = pin
        self.s = digitalio.DigitalInOut(usePin(self.pin))
        saveObj(self.pin,self.s)
        self._timeout = timeout

    def checkdist(self):
        self.s.direction = digitalio.Direction.OUTPUT
        self.s.value = False
        time.sleep(0.00002)  # 10 micro seconds 10/1000/1000
        self.s.value = True
        time.sleep(0.00001)  # 20 micro seconds 10/1000/1000
        self.s.value = False

        self.s.direction = digitalio.Direction.INPUT
        
        timestamp = time.monotonic_ns()
        while not self.s.value:
            if time.monotonic_ns() - timestamp > self._timeout:
                # raise RuntimeError("Timed out")
                return 999
        timestamp = time.monotonic_ns()
        while self.s.value:
            if time.monotonic_ns() - timestamp > self._timeout:
                # raise RuntimeError("Timed out")
                return 999
        pulselen = time.monotonic_ns() - timestamp
        pulselen *= 0.001  # convert to us to match pulseio
        if pulselen >= 65535:
            # raise RuntimeError("Timed out")
            return 999

        self.s.direction = digitalio.Direction.OUTPUT
        self.s.value = False
        time.sleep(0.01)
        # positive pulse time, in seconds, times 340 meters/sec, then
        # divided by 2 gives meters.
        # 1/1000000 s/ns * 340 m/s * 1000 mm/m * 2 = 0.017  (有误差)
        result = round(pulselen * 0.017)+1
        result = 999 if result > 310 else result
        return result