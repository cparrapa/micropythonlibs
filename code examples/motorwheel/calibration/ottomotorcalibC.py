# C simplified library for calibration under TEST
import time
from machine import Pin, PWM

class Robot:
    def __init__(self, left_motor_pin, right_motor_pin):
        self.left_motor = PWM(Pin(left_motor_pin))
        self.right_motor = PWM(Pin(right_motor_pin))
        self.left_motor.freq(50)
        self.right_motor.freq(50)
        self.calibration = 1.0

    def set_speed(self, left_speed, right_speed):
        self.left_motor.duty(left_speed)
        self.right_motor.duty(right_speed)

    def forward(self, speed=512):
        self.set_speed(speed, speed)

    def backward(self, speed=512):
        self.set_speed(-speed, -speed)

    def turn_left(self, speed=512):
        self.set_speed(-speed, speed)

    def turn_right(self, speed=512):
        self.set_speed(speed, -speed)

    def stop(self):
        self.set_speed(0, 0)

    def calibrate(self, calibration_factor):
        self.calibration = calibration_factor

    def move_distance(self, distance, speed=512):
        time_to_move = distance / self.calibration
        self.forward(speed)
        time.sleep(time_to_move)
        self.stop()

    def rotate_angle(self, angle, speed=512):
        time_to_rotate = angle / self.calibration
        self.turn_right(speed)
        time.sleep(time_to_rotate)
        self.stop()

    def dance(self):
        self.turn_left(512)
        time.sleep(1)
        self.turn_right(512)
        time.sleep(1)
        self.forward(512)
        time.sleep(1)
        self.backward(512)
        time.sleep(1)
        self.stop()

    def joyful_spin(self):
        self.turn_right(512)
        time.sleep(2)
        self.stop()
