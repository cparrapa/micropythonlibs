# calibrate_ottomotor.py
# Interactive wheel calibration for HP Robots / OttoRobot
#
# Run this once on the robot to tune:
#   1. wheel neutral / direction (done in the normal robot setup)
#   2. left/right wheel trim for straight driving
#   3. 90-degree turn timing
#
# The final values are saved to ESP32 flash by robot.save_calibration().
# They are loaded automatically by OttoRobot on the next boot.

import time
from ottomotor import create_robot

# ============================================================
# HARDWARE CONFIGURATION
# ============================================================

LEFT_ANGLE_PIN = 27
RIGHT_ANGLE_PIN = 15
LEFT_WHEEL_PIN = 14
RIGHT_WHEEL_PIN = 13

# Servo-specific calibration.
# Keep your known-good values here.
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

# Angle calibration is included because create_robot() needs all four pins.
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


def show_calibration():
    print('\nCURRENT ROBOT CALIBRATION')
    print('--------------------------')
    print('Left trim :', robot.left_trim)
    print('Right trim:', robot.right_trim)
    print('Turn speed :', robot.turn_speed)
    print('90 deg time:', robot.turn_90_ms, 'ms')


def pause():
    time.sleep(1)


print('\n=====================================')
print(' HP ROBOTS WHEEL CALIBRATION')
print('=====================================')
print('Calibration is loaded automatically if saved.')
show_calibration()


# ============================================================
# 1. STRAIGHT-LINE CALIBRATION
# ============================================================

print('\n-------------------------------------')
print('1. STRAIGHT-LINE CALIBRATION')
print('-------------------------------------')
print('Place the robot on the floor.')
print('Use a long straight line if possible.')
print('')
print('The robot will drive forward for 2 seconds.')
print('If it veers LEFT : increase left_trim OR decrease right_trim.')
print('If it veers RIGHT: decrease left_trim OR increase right_trim.')
print('')

input('Press ENTER to run the current straight test...')
robot.forward(50, smooth=True, duration_ms=500)
time.sleep_ms(2000)
robot.stop(smooth=True, duration_ms=500)
pause()

print('\nCurrent values:')
show_calibration()

print('\nAdjust using these commands in the REPL if needed:')
print("robot.set_calibration(left_trim=1.02)")
print("robot.set_calibration(right_trim=0.98)")
print('Then run: robot.wheel_test(50, 2000)')
print('')
print('Typical changes should be small, e.g. 1.00 -> 1.01 -> 1.02.')


# ============================================================
# 2. 90-DEGREE TURN CALIBRATION
# ============================================================

print('\n-------------------------------------')
print('2. 90-DEGREE TURN CALIBRATION')
print('-------------------------------------')
print('Place the robot in a clear area.')
print('Mark its starting heading if useful.')
print('')
print('The default calibration speed is', robot.turn_speed, '%')
print('The default 90-degree duration is', robot.turn_90_ms, 'ms.')
print('')

input('Press ENTER to perform a RIGHT 90-degree test...')
robot.turn_right_90()
robot.stop()
time.sleep(1)

print('\nDid the robot turn exactly 90 degrees?')
print('If it turned LESS than 90: increase turn_90_ms.')
print('If it turned MORE than 90: decrease turn_90_ms.')
print('')
print('Example:')
print("robot.set_calibration(turn_90_ms=450)")
print("robot.set_calibration(turn_90_ms=380)")
print('')


# ============================================================
# 3. SAVE
# ============================================================

print('\n-------------------------------------')
print('3. SAVE CALIBRATION')
print('-------------------------------------')
show_calibration()
print('')

save = input('Save these values to ESP32 flash? (y/n): ')

if save.lower() == 'y':
    robot.save_calibration()
    print('Calibration saved.')
    print('These values will be loaded automatically next time.')
else:
    print('Calibration NOT saved.')


# ============================================================
# 4. FINAL TEST
# ============================================================

print('\n-------------------------------------')
print('4. FINAL TEST')
print('-------------------------------------')
show_calibration()
print('')
print('Testing forward...')
robot.forward(50, smooth=True, duration_ms=500)
time.sleep_ms(1500)
robot.stop(smooth=True, duration_ms=500)
time.sleep(1)

print('Testing right 90 degrees...')
robot.turn_right_90()
robot.stop()
time.sleep(1)

robot.release_all()
print('\nCalibration test complete.')
