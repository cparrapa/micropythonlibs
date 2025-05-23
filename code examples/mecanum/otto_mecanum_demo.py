
from time import sleep
from otto4wd import OttoMecanum

# Initialize the robot (adjust connector numbers if needed)
robot = OttoMecanum()

# Define a speed value (within -50 to +50)
speed = 30
duration = 2  # seconds

# Move forward
print("Moving forward")
robot.forward(speed)
sleep(duration)

# Move backward
print("Moving backward")
robot.backward(speed)
sleep(duration)

# Turn left
print("Turning left")
robot.turn_left(speed)
sleep(duration)

# Turn right
print("Turning right")
robot.turn_right(speed)
sleep(duration)

# Crab left
print("Crabbing left")
robot.crab_left(speed)
sleep(duration)

# Crab right
print("Crabbing right")
robot.crab_right(speed)
sleep(duration)

# Diagonal left
print("Diagonal left")
robot.diag_left(speed)
sleep(duration)

# Diagonal right
print("Diagonal right")
robot.diag_right(speed)
sleep(duration)

# Stop
print("Stopping")
robot.stop()
sleep(1)
