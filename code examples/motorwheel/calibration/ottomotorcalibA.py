# ottomotorscalib library with inservo esp32 lib
import machine
import time
from machine import Pin, PWM
from esp32 import Servo as espServo

"""
from ottoangle import Servo
motor=Servo(pin=15)
motor.move(0) 
time.sleep(1)
motor.move(90) 
time.sleep(1)
motor.move(180) 
time.sleep(1)
motor.move(90) 
time.sleep(1)
"""

try:
    useServo = True
except ImportError:
    def espServo(_arg):
        print("espServo not defined")
        raise ImportError
    useServo = False

class Servo:
    """
    Servo class for controlling a single servo motor.
    """
    def __init__(self, freq=50, min_us=500, max_us=2500, max_ang=180, calib=0):
        global useServo
        self.min_us = min_us
        self.max_us = max_us
        self.freq = freq
        self.max_ang = max_ang
        self.pin = None
        self.calib = calib
        if useServo:
            self.servo = None
        else:
            self.pwm = None
        self._attached = False

    def attach(self, pin):
        global useServo
        self.pin = machine.Pin(pin)
        if useServo:
            self.servo = espServo(self.pin)
        else:
            self.pwm = machine.PWM(self.pin, freq=self.freq)
        self._attached = True

    def detach(self):
        global useServo
        if useServo and self.servo:
            self.servo.deinit()
        elif self.pwm:
            self.pwm.deinit()
        self._attached = False

    def attached(self):
        return self._attached

    def write_us(self, us):
        global useServo
        us = max(self.min_us, min(self.max_us, us + self.calib))
        if useServo and self.servo:
            self.servo.duty(us)
        elif self.pwm:
            duty = int(us / (1000000 / self.freq / 1024))
            self.pwm.duty(duty)

    def write(self, degrees):
        degrees = max(0, min(180, degrees))
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.max_ang
        self.write_us(us)

    def __deinit__(self):
        self.detach()


class OttoMotors:
    """
    OttoMotors controls two motors (left and right) using either PWM or Servo.
    Supports calibration offsets and multiple movement methods.
    mode: "pwm" or "servo"
    """
    def __init__(self, right_pin=13, left_pin=14, right_calib=0, left_calib=0, mode="servo"):
        self.mode = mode
        self.right_calib = right_calib
        self.left_calib = left_calib
        self.right_pin = right_pin
        self.left_pin = left_pin

        if self.mode == "pwm":
            self.right = PWM(Pin(right_pin))
            self.right.freq(50)
            self.left = PWM(Pin(left_pin))
            self.left.freq(50)
        else:
            self.right = Servo(calib=right_calib)
            self.left = Servo(calib=left_calib)

    def _calibrated_speed(self, speed, calib):
        return max(0, min(1023, speed + calib))

    def move(self, right_speed, left_speed, direction, t=None):
        if self.mode == "pwm":
            # PWM mode: right_speed and left_speed are PWM duty values (0-1023)
            right_speed = self._calibrated_speed(right_speed, self.right_calib)
            left_speed = self._calibrated_speed(left_speed, self.left_calib)
            if direction == "forward":
                self.right.duty(right_speed)
                self.left.duty(left_speed)
            elif direction == "backward":
                self.right.duty(left_speed)
                self.left.duty(right_speed)
            elif direction == "right":
                self.right.duty(right_speed)
                self.left.duty(0)
            elif direction == "left":
                self.right.duty(0)
                self.left.duty(left_speed)
            else:
                raise ValueError("Invalid direction")
            if t is not None:
                time.sleep(t)
                self.stop()
        else:
            # Servo mode: right_speed and left_speed are angles (0-90)
            self.right.attach(self.right_pin)
            self.left.attach(self.left_pin)
            if direction == "forward":
                self.right.write(90 - right_speed)
                self.left.write(left_speed + 90)
            elif direction == "backward":
                self.right.write(right_speed + 90)
                self.left.write(90 - left_speed)
            elif direction == "right":
                self.right.write(right_speed + 90)
                self.left.write(left_speed + 90)
            elif direction == "left":
                self.right.write(90 - right_speed)
                self.left.write(90 - left_speed)
            else:
                raise ValueError("Invalid direction")
            if t is not None:
                time.sleep(t)
                self.stop()

    def move_loop(self, direction, speed):
        # Only for PWM mode, for continuous movement
        if self.mode == "pwm":
            speed_map = {1: 60, 2: 45, 3: 30}
            rev_speed_map = {1: 100, 2: 115, 3: 130}
            if direction == -1:
                left_speed = speed_map.get(speed, 60)
                right_speed = rev_speed_map.get(speed, 100)
            else:
                right_speed = speed_map.get(speed, 60)
                left_speed = rev_speed_map.get(speed, 100)
            right_speed = self._calibrated_speed(right_speed, self.right_calib)
            left_speed = self._calibrated_speed(left_speed, self.left_calib)
            self.right.duty(right_speed)
            self.left.duty(left_speed)

    def rotate(self, turn):
        # Only for PWM mode
        if self.mode == "pwm":
            if turn == 0:
                speed = 45
                delay = 0.4
            elif turn == 1:
                speed = 115
                delay = 0.4
            elif turn == 2:
                speed = 45
                delay = 0.8
            else:
                speed = 45
                delay = 0.4
            right_speed = self._calibrated_speed(speed, self.right_calib)
            left_speed = self._calibrated_speed(speed, self.left_calib)
            self.right.duty(right_speed)
            self.left.duty(left_speed)
            time.sleep(delay)
            self.stop()

    def move_left(self, direction, duration, speed):
        if self.mode == "pwm":
            speed_map = {1: 60, 2: 45, 3: 30}
            rev_speed_map = {1: 130, 2: 115, 3: 100}
            if direction == -1:
                left_speed = speed_map.get(speed, 60)
            else:
                left_speed = rev_speed_map.get(speed, 130)
            left_speed = self._calibrated_speed(left_speed, self.left_calib)
            self.left.duty(left_speed)
            time.sleep(duration)
            self.left.duty(0)

    def move_left_loop(self, direction, speed):
        if self.mode == "pwm":
            speed_map = {1: 60, 2: 45, 3: 30}
            rev_speed_map = {1: 130, 2: 115, 3: 100}
            if direction == -1:
                left_speed = speed_map.get(speed, 60)
            else:
                left_speed = rev_speed_map.get(speed, 130)
            left_speed = self._calibrated_speed(left_speed, self.left_calib)
            self.left.duty(left_speed)

    def move_right(self, direction, duration, speed):
        if self.mode == "pwm":
            rev_speed_map = {1: 130, 2: 115, 3: 100}
            speed_map = {1: 60, 2: 45, 3: 30}
            if direction == -1:
                right_speed = rev_speed_map.get(speed, 130)
            else:
                right_speed = speed_map.get(speed, 60)
            right_speed = self._calibrated_speed(right_speed, self.right_calib)
            self.right.duty(right_speed)
            time.sleep(duration)
            self.right.duty(0)

    def move_right_loop(self, direction, speed):
        if self.mode == "pwm":
            rev_speed_map = {1: 130, 2: 115, 3: 100}
            speed_map = {1: 60, 2: 45, 3: 30}
            if direction == -1:
                right_speed = rev_speed_map.get(speed, 130)
            else:
                right_speed = speed_map.get(speed, 60)
            right_speed = self._calibrated_speed(right_speed, self.right_calib)
            self.right.duty(right_speed)

    def stop(self):
        if self.mode == "pwm":
            self.right.duty(0)
            self.left.duty(0)
        else:
            self.right.attach(self.right_pin)
            self.left.attach(self.left_pin)
            self.right.write(90)
            self.left.write(90)