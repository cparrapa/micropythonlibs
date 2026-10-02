# test_ottomotor.py
# Basic hardware test for HP Robots / OttoMotor library.
# Run this on the ESP32 with ottomotor.py in the same directory.

import time
from ottomotor import create_robot

# ------------------------------------------------------------
# HARDWARE CONFIGURATION
# Change ONLY these values for your board/wiring.
# ------------------------------------------------------------
LEFT_ANGLE_PIN = 27
RIGHT_ANGLE_PIN = 15
LEFT_WHEEL_PIN = 14
RIGHT_WHEEL_PIN = 13

# ------------------------------------------------------------
# CALIBRATION
# Start with these defaults. Adjust after testing each servo.
# reverse=True flips the direction of that individual servo.
# ------------------------------------------------------------
LEFT_ANGLE_CAL = {
    'min_us': 400,
    'max_us': 2600,
    'center_us': 1500,
    'reverse': False,
}

RIGHT_ANGLE_CAL = {
    'min_us': 400,
    'max_us': 2600,
    'center_us': 1500,
    'reverse': False,
}

LEFT_WHEEL_CAL = {
    'min_us': 400,
    'max_us': 2600,
    'center_us': 1500,
    'reverse': False,
}

RIGHT_WHEEL_CAL = {
    'min_us': 400,
    'max_us': 2600,
    'center_us': 1500,
    'reverse': False,
}


print('\n========================================')
print(' HP ROBOTS OTTOMOTOR TEST')
print('========================================')
print('Pins:')
print('  left_angle  =', LEFT_ANGLE_PIN)
print('  right_angle =', RIGHT_ANGLE_PIN)
print('  left_wheel  =', LEFT_WHEEL_PIN)
print('  right_wheel =', RIGHT_WHEEL_PIN)

robot = create_robot(
    LEFT_ANGLE_PIN,
    RIGHT_ANGLE_PIN,
    LEFT_WHEEL_PIN,
    RIGHT_WHEEL_PIN,
    LEFT_ANGLE_CAL,
    RIGHT_ANGLE_CAL,
    LEFT_WHEEL_CAL,
    RIGHT_WHEEL_CAL,
)


def pause(seconds=1):
    time.sleep(seconds)


def section(name):
    print('\n----------------------------------------')
    print(name)
    print('----------------------------------------')


# ------------------------------------------------------------
# 1. ATTACH / CENTER ANGLE SERVOS
# ------------------------------------------------------------
section('1. ANGLE SERVOS: center')
print('Moving both angle servos to 90 degrees...')
robot.left_angle.angle_smooth(90, 500, hold=True)
robot.right_angle.angle_smooth(90, 500, hold=True)
print('Both angle servos should now be centered and holding.')
pause(1)


# ------------------------------------------------------------
# 2. ANGLE SERVO MOVEMENT
# ------------------------------------------------------------
section('2. ANGLE SERVOS: 0 -> 90 -> 180 -> 90')
for angle in (0, 90, 180, 90):
    print('Angle:', angle)
    robot.left_angle.angle_smooth(angle, 500, hold=True)
    robot.right_angle.angle_smooth(angle, 500, hold=True)
    pause(0.3)


# ------------------------------------------------------------
# 3. RELEASE ANGLE SERVOS
# Useful to confirm PWM can be disabled so a servo does not
# continuously hold torque and heat up when it is not needed.
# ------------------------------------------------------------
section('3. ANGLE SERVOS: release')
print('Moving to 90 degrees and releasing PWM...')
robot.left_angle.angle_smooth(90, 400, hold=False)
robot.right_angle.angle_smooth(90, 400, hold=False)
print('Angle servos released.')
pause(1)


# ------------------------------------------------------------
# 4. INDIVIDUAL ANGLE SERVO TEST
# ------------------------------------------------------------
section('4. INDIVIDUAL ANGLE SERVO TEST')
print('Left angle: 45 degrees')
robot.left_angle.angle_smooth(45, 400, hold=True)
pause(0.5)
print('Right angle: 135 degrees')
robot.right_angle.angle_smooth(135, 400, hold=True)
pause(0.5)
print('Returning both to 90 degrees')
robot.left_angle.angle_smooth(90, 400, hold=False)
robot.right_angle.angle_smooth(90, 400, hold=False)
pause(1)


# ------------------------------------------------------------
# 5. WHEELS: NEUTRAL
# IMPORTANT: Lift the robot off the table before wheel tests.
# At 0% the wheels should be stopped.
# ------------------------------------------------------------
section('5. WHEELS: neutral / stop')
print('Setting both wheels to 0%...')
robot.set_wheels(0, 0)
pause(1)
print('If a wheel creeps, adjust its center_us calibration.')


# ------------------------------------------------------------
# 6. WHEELS: INDIVIDUAL SPEEDS
# ------------------------------------------------------------
section('6. WHEELS: individual speed test')
print('Left wheel +25%, right wheel 0%')
robot.set_wheels(25, 0)
pause(1)
robot.stop(release=True)
pause(0.5)

print('Right wheel +25%, left wheel 0%')
robot.set_wheels(0, 25)
pause(1)
robot.stop(release=True)
pause(0.5)


# ------------------------------------------------------------
# 7. SYNCHRONIZED FORWARD / BACKWARD
# ------------------------------------------------------------
section('7. WHEELS: synchronized movement')
print('Forward 30%, smooth ramp')
robot.forward(30, smooth=True, duration_ms=600)
pause(1)
print('Stop')
robot.stop(smooth=True, duration_ms=500, release=True)
pause(0.5)

print('Backward 30%, smooth ramp')
robot.backward(30, smooth=True, duration_ms=600)
pause(1)
print('Stop')
robot.stop(smooth=True, duration_ms=500, release=True)
pause(0.5)


# ------------------------------------------------------------
# 8. TURNING
# ------------------------------------------------------------
section('8. WHEELS: turning')
print('Turn left: left -30%, right +30%')
robot.turn_left(30, smooth=True, duration_ms=600)
pause(1)
robot.stop(release=True)
pause(0.5)

print('Turn right: left +30%, right -30%')
robot.turn_right(30, smooth=True, duration_ms=600)
pause(1)
robot.stop(release=True)
pause(0.5)


# ------------------------------------------------------------
# 9. SMOOTH SPEED SWEEP
# ------------------------------------------------------------
section('9. INDIVIDUAL WHEEL SPEED SWEEP')
print('Left wheel: 0 -> +20 -> +40 -> +60 -> 0')
robot.left_wheel.speed_smooth(20, 300)
pause(0.3)
robot.left_wheel.speed_smooth(40, 300)
pause(0.3)
robot.left_wheel.speed_smooth(60, 300)
pause(0.3)
robot.left_wheel.speed_smooth(0, 500)
robot.left_wheel.detach()
pause(0.5)

print('Right wheel: 0 -> +20 -> +40 -> +60 -> 0')
robot.right_wheel.speed_smooth(20, 300)
pause(0.3)
robot.right_wheel.speed_smooth(40, 300)
pause(0.3)
robot.right_wheel.speed_smooth(60, 300)
pause(0.3)
robot.right_wheel.speed_smooth(0, 500)
robot.right_wheel.detach()
pause(0.5)


# ------------------------------------------------------------
# 10. HOLD / HOLD_FOR
# ------------------------------------------------------------
section('10. HOLD / HOLD_FOR')
print('Left angle -> 60 degrees, hold for 1 second, release')
robot.left_angle.angle_smooth(60, 400, hold=True)
robot.left_angle.hold_for(1000)
print('Left angle released.')


# ------------------------------------------------------------
# 11. CALIBRATION API CHECK
# This only changes the in-memory calibration.
# ------------------------------------------------------------
section('11. CALIBRATION API')
print('Changing left wheel center to 1500us, reverse=False')
robot.left_wheel.calibrate(center_us=1500, reverse=False)
print('Current left wheel calibration:')
print('  min_us   =', robot.left_wheel.min_us)
print('  max_us   =', robot.left_wheel.max_us)
print('  center_us =', robot.left_wheel.center_us)
print('  reverse  =', robot.left_wheel.reverse)


# ------------------------------------------------------------
# 12. FINAL SAFE STOP
# ------------------------------------------------------------
section('12. FINAL STOP')
robot.stop(release=True)
robot.left_angle.detach()
robot.right_angle.detach()
print('All wheel and angle outputs released.')
print('\n========================================')
print(' TEST COMPLETE')
print('========================================\n')

# ------------------------------------------------------------
# 13. BACKWARD-COMPATIBLE OttoMotor API
# This verifies the old Move / Moveloop / Moveleft* /
# Moveright* / Rotate / Stop names still work.
# ------------------------------------------------------------
section('13. LEGACY OttoMotor API')
from ottomotor import OttoMotor

legacy = OttoMotor(
    RIGHT_WHEEL_PIN,
    LEFT_WHEEL_PIN,
    left_cal=LEFT_WHEEL_CAL,
    right_cal=RIGHT_WHEEL_CAL,
)

print('Move(direction=1, step=0.5, speed=1)')
legacy.Move(1, 0.5, 1)
print('Move completed and stopped.')

print('Moveleftloop(direction=1, speed=1)')
legacy.Moveleftloop(1, 1)
pause(0.5)
legacy.Stop(2)
print('Left wheel stopped.')

print('Moverightloop(direction=1, speed=1)')
legacy.Moverightloop(1, 1)
pause(0.5)
legacy.Stop(3)
print('Right wheel stopped.')

print('Rotate(turn=0)')
legacy.Rotate(0)
print('Rotate completed and stopped.')
print('Legacy API test complete.')

# ------------------------------------------------------------
# FINAL CLEANUP AGAIN
# ------------------------------------------------------------
section('FINAL CLEANUP')
robot.stop(release=True)
robot.left_angle.detach()
robot.right_angle.detach()
legacy.Stop(1)
print('All servo outputs released.')
print('\n========================================')
print(' ALL TESTS COMPLETE')
print('========================================\n')

