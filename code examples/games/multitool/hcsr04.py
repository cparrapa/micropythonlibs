# hcsr04.py — MicroPython driver for HC-SR04 / US-100 (ESP32/ESP8266)
# Works with machine.time_pulse_us and includes a small compatibility layer.
# Exposes: HCSR04(trigger_pin, echo_pin, echo_timeout_us=30000)
#          .distance_cm() -> float or None
#          .last_pulse_us  (None or int): last echo HIGH width in microseconds
#
# Note: Many HC-SR04 modules output 5V on ECHO. Use a resistor divider to ~3.3V
# before feeding the ESP32 input. Common GND required.

from machine import Pin
import machine, time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=30000):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.echo_timeout_us = echo_timeout_us
        self.last_pulse_us = None
        self.trigger.off()

    def _send_pulse_and_wait(self):
        """Send a 10µs trigger pulse and wait for echo HIGH.
        Returns pulse length in µs, or negative on timeout/err."""
        self.last_pulse_us = None

        # settle
        self.trigger.off()
        time.sleep_us(2)

        # 10 µs pulse
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()

        try:
            dur = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            # dur < 0 means timeout or invalid on some ports
            self.last_pulse_us = dur if dur >= 0 else None
            return dur
        except OSError as ex:
            # On some ports ETIMEDOUT -> errno 110
            self.last_pulse_us = None
            return -2

    def distance_cm(self):
        """Return distance in centimeters, or None if no valid echo."""
        dur = self._send_pulse_and_wait()
        if dur is None or dur < 0:
            return None
        # Convert microseconds of round-trip to one-way cm
        cm = (dur * 0.0343) / 2.0
        # sanity range for HC-SR04
        if 1.0 <= cm <= 400.0:
            return cm
        return None
