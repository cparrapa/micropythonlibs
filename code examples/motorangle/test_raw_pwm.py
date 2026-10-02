# test_raw_pwm.py
# Direct ESP32 PWM test - does NOT use ottomotor.py

import time
from machine import Pin, PWM

LEFT_ANGLE_PIN = 27
RIGHT_ANGLE_PIN = 15
LEFT_WHEEL_PIN = 14
RIGHT_WHEEL_PIN = 13

FREQ = 50


def us_to_duty(us):
    # 50 Hz = 20,000 us period
    return int(us * 65535 / 20000)


print("\n==============================")
print(" RAW ESP32 PWM TEST")
print("==============================")

# Create ALL four PWM channels at the same time
left_angle = PWM(Pin(LEFT_ANGLE_PIN), freq=FREQ)
right_angle = PWM(Pin(RIGHT_ANGLE_PIN), freq=FREQ)
left_wheel = PWM(Pin(LEFT_WHEEL_PIN), freq=FREQ)
right_wheel = PWM(Pin(RIGHT_WHEEL_PIN), freq=FREQ)

# Start everything at neutral/center
left_angle.duty_u16(us_to_duty(1500))
right_angle.duty_u16(us_to_duty(1500))
left_wheel.duty_u16(us_to_duty(1500))
right_wheel.duty_u16(us_to_duty(1500))

print("All four initialized at 1500 us")
time.sleep(2)


print("\n1. LEFT ANGLE ONLY")
print("GPIO 27 -> 1000 us")
left_angle.duty_u16(us_to_duty(1000))
time.sleep(2)

print("GPIO 27 -> 2000 us")
left_angle.duty_u16(us_to_duty(2000))
time.sleep(2)

print("GPIO 27 -> 1500 us")
left_angle.duty_u16(us_to_duty(1500))
time.sleep(1)


print("\n2. RIGHT ANGLE ONLY")
print("GPIO 15 -> 1000 us")
right_angle.duty_u16(us_to_duty(1000))
time.sleep(2)

print("GPIO 15 -> 2000 us")
right_angle.duty_u16(us_to_duty(2000))
time.sleep(2)

print("GPIO 15 -> 1500 us")
right_angle.duty_u16(us_to_duty(1500))
time.sleep(1)


print("\n3. LEFT WHEEL ONLY")
print("GPIO 14 -> 1200 us")
left_wheel.duty_u16(us_to_duty(1200))
time.sleep(2)

print("GPIO 14 -> 1500 us")
left_wheel.duty_u16(us_to_duty(1500))
time.sleep(1)


print("\n4. RIGHT WHEEL ONLY")
print("GPIO 13 -> 1800 us")
right_wheel.duty_u16(us_to_duty(1800))
time.sleep(2)

print("GPIO 13 -> 1500 us")
right_wheel.duty_u16(us_to_duty(1500))
time.sleep(1)


print("\n5. CROSS-CHECK")
print("Only GPIO 27 should move now.")
left_angle.duty_u16(us_to_duty(1100))
time.sleep(2)
left_angle.duty_u16(us_to_duty(1900))
time.sleep(2)
left_angle.duty_u16(us_to_duty(1500))

print("\nOnly GPIO 15 should move now.")
right_angle.duty_u16(us_to_duty(1100))
time.sleep(2)
right_angle.duty_u16(us_to_duty(1900))
time.sleep(2)
right_angle.duty_u16(us_to_duty(1500))


print("\nReleasing all PWM")

left_angle.deinit()
right_angle.deinit()
left_wheel.deinit()
right_wheel.deinit()

print("TEST COMPLETE")