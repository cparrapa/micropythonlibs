"""
robot_movement.py

A simple library that wraps your calibrated servo logic
into easy movement functions:

    from robot_movement import Robot
    bot = Robot()
    bot.forward(50)
    bot.turn_left(30)
    bot.stop()

This library:
 - Loads saved trim from NVS
 - Performs correct right‑servo inversion
 - Applies dead‑zone and clamping
 - Exposes high‑level movement functions
 - Allows optional live trim injection if needed

You still run a separate small main script to read pots
or to drive the robot.
"""

from machine import Pin, PWM
import esp32

# ------------------- SERVO CONSTANTS -------------------
MIN_US = 500
MID_US = 1500
MAX_US = 2500
PERIOD_US = 20000
FREQ = 50

# Dead zone
DZ_MIN = 1400
DZ_MAX = 1600

# Pins
LEFT_SERVO_PIN  = 14
RIGHT_SERVO_PIN = 13

# Inversion
RIGHT_INVERT = True

class Robot:
    def __init__(self):
        # Init servos
        self.left_pwm  = PWM(Pin(LEFT_SERVO_PIN),  freq=FREQ)
        self.right_pwm = PWM(Pin(RIGHT_SERVO_PIN), freq=FREQ)

        # Load trim
        try:
            nvs = esp32.NVS("robot")
            self.trim_us = nvs.get_i32("trim_us")
        except Exception:
            self.trim_us = 0

    # ----------------------------------------------------
    def _apply_deadzone(self, us):
        if DZ_MIN <= us <= DZ_MAX:
            return MID_US
        return us

    def _clamp(self, us):
        return max(MIN_US, min(MAX_US, us))

    def _set_servo_pulse(self, pwm, pulse_us):
        duty = int((pulse_us / PERIOD_US) * 1023)
        pwm.duty(duty)

    def _percent_to_us(self, pct):
        if pct < -100: pct = -100
        if pct >  100: pct = 100
        if pct == 0:
            return MID_US
        if pct > 0:
            return int(MID_US + (MAX_US - MID_US) * (pct/100))
        else:
            return int(MID_US - (MID_US - MIN_US) * (abs(pct)/100))

    # ----------------------------------------------------
    def drive(self, speed_percent, trim_live=0):
        """
        General movement function.
        speed_percent: -100 to +100
        trim_live: optional additional trim from pot, range small (e.g. ±20)
        """
        base = self._percent_to_us(speed_percent)

        # Add trims
        left  = base + self.trim_us + trim_live
        right = base - (self.trim_us + trim_live)

        # Dead zone
        left  = self._apply_deadzone(left)
        right = self._apply_deadzone(right)

        # Clamp
        left  = self._clamp(left)
        right = self._clamp(right)

        # Invert right if needed
        if RIGHT_INVERT:
            right = MID_US - (right - MID_US)

        # Apply
        self._set_servo_pulse(self.left_pwm,  left)
        self._set_servo_pulse(self.right_pwm, right)

    # ---------------- HIGH‑LEVEL COMMANDS ----------------
    def forward(self, speed=50):
        self.drive(abs(speed))

    def backward(self, speed=50):
        self.drive(-abs(speed))

    def turn_left(self, speed=40):
        # Left wheel backward, right wheel forward
        self.drive(0)  # base neutral
        left  = self._percent_to_us(-abs(speed))
        right = self._percent_to_us(abs(speed))

        left  = self._apply_deadzone(left)
        right = self._apply_deadzone(right)

        left  = self._clamp(left)
        right = self._clamp(right)

        if RIGHT_INVERT:
            right = MID_US - (right - MID_US)

        self._set_servo_pulse(self.left_pwm,  left)
        self._set_servo_pulse(self.right_pwm, right)

    def turn_right(self, speed=40):
        left  = self._percent_to_us(abs(speed))
        right = self._percent_to_us(-abs(speed))

        left  = self._apply_deadzone(left)
        right = self._apply_deadzone(right)

        left  = self._clamp(left)
        right = self._clamp(right)

        if RIGHT_INVERT:
            right = MID_US - (right - MID_US)

        self._set_servo_pulse(self.left_pwm,  left)
        self._set_servo_pulse(self.right_pwm, right)

    def stop(self):
        self.drive(0)
