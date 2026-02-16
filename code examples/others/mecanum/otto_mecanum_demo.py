from time import sleep
from otto4wd import OttoMecanum
from ottoneopixel import OttoNeoPixel
from ottoneopixel import OttoUltrasonic

ring = OttoNeoPixel(4, 13)  
ultrasonic = OttoUltrasonic(18, 19)

# Initialize the robot (adjust connector numbers if needed)
robot = OttoMecanum()

# Define a speed value (within -50 to +50)
speed = 30
duration = 2  # seconds

# Move forward
print("Moving forward")
ring.fillAllRing(0, 0, 255)
ultrasonic.ultrasonicRGB2(0, 0, 255)
robot.forward(speed)
sleep(duration)

# Move backward
print("Moving backward")
ring.fillAllRing(255, 0, 255)
ultrasonic.ultrasonicRGB2(255, 0, 255)
robot.backward(speed)
sleep(duration)

# Turn left
print("Turning left")
ring.fillAllRing(255, 0, 0)
ultrasonic.ultrasonicRGB2(255, 0, 0)
robot.turn_left(speed)
sleep(duration)

# Turn right
print("Turning right")
ring.fillAllRing(255, 255, 0)
ultrasonic.ultrasonicRGB2(255, 255, 0)
robot.turn_right(speed)
sleep(duration)

# Crab left
print("Crabbing left")
ring.fillAllRing(0, 255, 0)
ultrasonic.ultrasonicRGB2(0, 255, 0)
robot.crab_left(speed)
sleep(duration)

# Crab right
print("Crabbing right")
ring.fillAllRing(0, 255, 255)
ultrasonic.ultrasonicRGB2(0, 255, 255)
robot.crab_right(speed)
sleep(duration)

# Diagonal left
print("Diagonal left")
ring.fillAllRing(255, 255, 255)
ultrasonic.ultrasonicRGB2(255, 255, 255)
robot.diag_left(speed)
sleep(duration)

# Diagonal right
print("Diagonal right")
ring.fillAllRing(50, 50, 50)
ultrasonic.ultrasonicRGB2(50, 50, 50)
robot.diag_right(speed)
sleep(duration)

# Stop
print("Stopping")
ring.fillAllRing(0, 0, 0)
ultrasonic.ultrasonicRGB2(0, 0, 0)
robot.stop()
sleep(1)


