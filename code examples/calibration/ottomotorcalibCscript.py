
from ottomotorcalibC import Robot
import time

# Initialize the robot with motor pins
robot = Robot(left_motor_pin=14, right_motor_pin=12)

# Calibrate the robot
robot.calibrate(1.0)

# Test basic movements
robot.forward(512)
time.sleep(2)
robot.backward(512)
time.sleep(2)
robot.turn_left(512)
time.sleep(2)
robot.turn_right(512)
time.sleep(2)
robot.stop()

# Test calibration and precision movements
robot.move_distance(10, 512)
robot.rotate_angle(90, 512)

# Test fun movements
robot.dance()
robot.joyful_spin()
