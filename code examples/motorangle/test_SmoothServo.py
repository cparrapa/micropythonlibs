"""
test_SmoothServo.py

Servo setup for the robot:

    GPIO 27 = left/first 180-degree servo
    GPIO 15 = right/second 180-degree servo
    GPIO 14 = left continuous wheel
    GPIO 13 = right continuous wheel

Change reverse=True on individual servos if their physical direction
is opposite to what you want.

Start with conservative tests before using the full range.
"""

from SmoothServo import SmoothServo, ServoPair
import time


# ---------------------------------------------------------
# Positional servos
# ---------------------------------------------------------

head = SmoothServo(
    27,
    mode="angle",
    min_us=400,
    max_us=2600,
    center_us=1500,
)

arm = SmoothServo(
    15,
    mode="angle",
    min_us=400,
    max_us=2600,
    center_us=1500,
)


# ---------------------------------------------------------
# Continuous rotation wheels
# ---------------------------------------------------------

left_wheel = SmoothServo(
    14,
    mode="continuous",
    min_us=400,
    max_us=2600,
    center_us=1500,
)

right_wheel = SmoothServo(
    13,
    mode="continuous",
    min_us=400,
    max_us=2600,
    center_us=1500,
    reverse=True,       # change/remove if needed
)

wheels = ServoPair(left_wheel, right_wheel)


# ---------------------------------------------------------
# TEST 1: independent positional servos
# ---------------------------------------------------------

print("Moving GPIO 27 only...")
head.angle_smooth(30, 800)

time.sleep_ms(500)

print("Moving GPIO 27 back...")
head.angle_smooth(90, 800)

time.sleep_ms(500)

print("Now moving GPIO 15 only...")
arm.angle_smooth(150, 800)

time.sleep_ms(500)

print("Moving GPIO 15 back...")
arm.angle_smooth(90, 800)

time.sleep_ms(500)


# ---------------------------------------------------------
# TEST 2: wheel speed
# ---------------------------------------------------------

print("Wheels forward slowly")
wheels.drive(30, smooth=True, duration_ms=800)

time.sleep_ms(1500)

print("Stop")
wheels.stop(smooth=True, duration_ms=500)

time.sleep_ms(500)


# ---------------------------------------------------------
# TEST 3: turn
# ---------------------------------------------------------

print("Turn right")
wheels.turn(35, smooth=True, duration_ms=800)

time.sleep_ms(1000)

print("Stop")
wheels.stop(smooth=True, duration_ms=500)

time.sleep_ms(500)


# ---------------------------------------------------------
# TEST 4: release positional servo
# ---------------------------------------------------------

print("Move head to 120 degrees")
head.angle_smooth(120, 700)

time.sleep_ms(500)

print("Release head - PWM OFF")
head.release()

print("The servo should no longer actively hold position.")
time.sleep_ms(2000)

print("Re-attach and center")
head.attach()
head.angle_smooth(90, 700)


# ---------------------------------------------------------
# IMPORTANT:
# Do not leave positional servos holding force unnecessarily.
# Example:
#
# head.angle_smooth(90, 500)
# time.sleep_ms(300)
# head.release()
#
# If the mechanism needs to maintain a physical position,
# keep PWM enabled, but some servo heating is normal because
# the motor continuously corrects its position.
# ---------------------------------------------------------

print("Test complete.")
