
from robot_library import Robot
from time import sleep

# Initialize robot with motor pins
robot = Robot(left_pin=14, right_pin=27)

# Calibrate motors
robot.calibrate(left_offset=5, right_offset=0)

# Basic movements
robot.forward(60)
sleep(2)
robot.backward(60)
sleep(2)
robot.turn_left(60)
sleep(1)
robot.turn_right(60)
sleep(1)
robot.stop()

# Move a specific distance
robot.move_distance(30, speed=70)

# Rotate a specific angle
robot.rotate_angle(90, speed=70)

# Fun movements
robot.dance()
robot.joyful_spin()
