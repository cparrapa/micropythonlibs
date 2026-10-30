
from machine import Pin, PWM
from time import sleep

class Robot:
    def __init__(self, left_pin, right_pin, wheel_diameter_cm=6.5, wheel_base_cm=12.0):
        self.left_motor = PWM(Pin(left_pin), freq=50)
        self.right_motor = PWM(Pin(right_pin), freq=50)
        self.wheel_diameter = wheel_diameter_cm
        self.wheel_base = wheel_base_cm
        self.left_calibration = 0
        self.right_calibration = 0

    def set_speed(self, left_speed, right_speed):
        left_duty = self._map_speed(left_speed + self.left_calibration)
        right_duty = self._map_speed(right_speed + self.right_calibration)
        self.left_motor.duty(left_duty)
        self.right_motor.duty(right_duty)

    def _map_speed(self, speed):
        # Map speed from -100 to 100 to duty cycle range 0 to 1023
        speed = max(-100, min(100, speed))
        if speed > 0:
            return int(77 + (speed / 100) * (1023 - 77))  # Forward
        elif speed < 0:
            return int(77 - (abs(speed) / 100) * 77)      # Reverse
        else:
            return 77  # Stop

    def stop(self):
        self.set_speed(0, 0)

    def forward(self, speed=50):
        self.set_speed(speed, speed)

    def backward(self, speed=50):
        self.set_speed(-speed, -speed)

    def turn_left(self, speed=50):
        self.set_speed(-speed, speed)

    def turn_right(self, speed=50):
        self.set_speed(speed, -speed)

    def calibrate(self, left_offset=0, right_offset=0):
        self.left_calibration = left_offset
        self.right_calibration = right_offset

    def move_distance(self, distance_cm, speed=50):
        # Calculate time to move based on wheel circumference
        circumference = 3.1416 * self.wheel_diameter
        rotations = distance_cm / circumference
        time_sec = rotations * 1.2  # Adjust time factor as needed
        self.forward(speed)
        sleep(time_sec)
        self.stop()

    def rotate_angle(self, angle_deg, speed=50):
        # Calculate time to rotate based on wheel base
        arc_length = (3.1416 * self.wheel_base) * (angle_deg / 360)
        circumference = 3.1416 * self.wheel_diameter
        rotations = arc_length / circumference
        time_sec = rotations * 1.2  # Adjust time factor as needed
        self.turn_right(speed)
        sleep(time_sec)
        self.stop()

    def dance(self):
        for _ in range(2):
            self.turn_left(80)
            sleep(0.5)
            self.turn_right(80)
            sleep(0.5)
        self.stop()

    def joyful_spin(self):
        self.set_speed(100, 100)
        sleep(1)
        self.set_speed(-100, -100)
        sleep(1)
        self.stop()
