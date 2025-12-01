# D complex  library for calibration under TEST
from machine import Pin, PWM
import time
import math

class Robot:
    def __init__(self, left_pin=13, right_pin=14, freq=50, left_dir=1, right_dir=1,
                 wheel_diameter_mm=52, wheel_base_mm=100):
        self.left_pwm = PWM(Pin(left_pin), freq=freq)
        self.right_pwm = PWM(Pin(right_pin), freq=freq)

        self.left_dir = left_dir
        self.right_dir = right_dir

        self.neutral = 77  # Adjust as needed for your servos (77 is ~1.5ms on 10-bit duty for ESP32)
        self.max_offset = 26  # full speed offset from neutral  Max duty offset from neutral (forward or backward)
        
        # Calibration offsets (you can tweak these)
        self.left_trim_pct = 0  # percent, easier to reason about
        self.right_trim_pct = 0

        self.wheel_diameter = wheel_diameter_mm
        self.wheel_circumference = math.pi * self.wheel_diameter
        self.wheel_base = wheel_base_mm  # Distance between wheels (left <--> right)

        self.base_speed_cm_s = 8  # Measured speed at 100% (default estimate)
        self.rotation_speed_deg_per_s = 180  # Placeholder value to be calibrated

    def _percent_to_duty(self, percent, trim_percent, direction):
        effective_percent = percent + trim_percent
        effective_percent = max(-100, min(100, effective_percent))
        return self.neutral + int((effective_percent / 100.0) * self.max_offset * direction)

    def set_pwm(self, pwm, speed_percent, trim_percent, direction):
        # speed: -1.0 (full reverse) to 1.0 (full forward)
        duty = self._percent_to_duty(speed_percent, trim_percent, direction)
        duty = max(40, min(115, duty))  # Clamp for safety
        pwm.duty(duty)

    def stop(self):
        self.left_pwm.duty(self.neutral)
        self.right_pwm.duty(self.neutral)

    def forward(self, speed=50, duration=0):
        self.set_pwm(self.left_pwm, speed, self.left_trim_pct, self.left_dir)
        self.set_pwm(self.right_pwm, speed, self.right_trim_pct, self.right_dir)
        if duration:
            time.sleep(duration)
            self.stop()

    def backward(self, speed=50, duration=0):
        self.set_pwm(self.left_pwm, -speed, self.left_trim_pct, self.left_dir)
        self.set_pwm(self.right_pwm, -speed, self.right_trim_pct, self.right_dir)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, speed=50, duration=0):
        self.set_pwm(self.left_pwm, -speed, self.left_trim_pct, self.left_dir)
        self.set_pwm(self.right_pwm, speed, self.right_trim_pct, self.right_dir)
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_right(self, speed=50, duration=0):
        self.set_pwm(self.left_pwm, speed, self.left_trim_pct, self.left_dir)
        self.set_pwm(self.right_pwm, -speed, self.right_trim_pct, self.right_dir)
        if duration:
            time.sleep(duration)
            self.stop()

    def set_trim(self, left_trim_pct, right_trim_pct):
        self.left_trim_pct = left_trim_pct
        self.right_trim_pct = right_trim_pct

    def move_distance(self, distance_cm, speed=50):
        # Estimate speed based on percent
        # You'll need to calibrate time per cm empirically Example: 8 cm/s at speed=0.5
        speed_cm_s = self.base_speed_cm_s * (speed / 100.0)
        if speed_cm_s <= 0:
            return
        duration = abs(distance_cm) / speed_cm_s
        if distance_cm > 0:
            self.forward(speed, duration)
        else:
            self.backward(speed, duration)

    def rotate_angle(self, angle_deg, speed=50):
        # Angle in degrees → arc length = angle / 360 * wheel_base * π
        # For in-place turning: both wheels spin in opposite directions
        # So actual rotation speed is doubled (both wheels contribute)
        # Duration based on empirically measured rotation speed
        abs_angle = abs(angle_deg)
        effective_speed = (speed / 100.0) * self.rotation_speed_deg_per_s
        if effective_speed <= 0:
            return
        duration = abs_angle / effective_speed

        if angle_deg > 0:
            self.turn_right(speed, duration)
        else:
            self.turn_left(speed, duration)

    def dance(self):
        for _ in range(3):
            self.turn_left(70, 0.3)
            self.turn_right(70, 0.3)
            self.forward(60, 0.2)
            self.backward(60, 0.2)

    def joyful_spin(self):
        for _ in range(2):
            self.turn_right(100, 1)
            self.turn_left(100, 1)
