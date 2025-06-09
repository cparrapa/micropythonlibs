from robot import Robot
import time

bot = Robot(left_pin=14, right_pin=13, left_dir=1, right_dir=-1,
            wheel_diameter_mm=52, wheel_base_mm=84)  # Adjust base if needed


# Set trim in percent (+/-10% typical)
bot.set_trim(left_trim_pct=2, right_trim_pct=-2)

bot.set_trim(left_trim_pct=0, right_trim_pct=0)

# Measure this rotation
print("Testing 1 second turn at 100% speed")
bot.turn_right(100, 1)
bot.stop()

# Measure the degrees rotated manually, then update this:
bot.rotation_speed_deg_per_s = 135  # ← Update based on your measurement

# Now try:
print("Testing calibrated 90° rotation")
bot.rotate_angle(90, speed=100)

print("Testing calibrated -90° rotation")
bot.rotate_angle(-90, speed=100)

bot.stop()

print("Testing forward")
bot.forward(speed=60, duration=2)

print("Testing backward")
bot.backward(speed=60, duration=2)

print("Testing turn right")
bot.turn_right(speed=60, duration=1.5)

print("Testing turn left")
bot.turn_left(speed=60, duration=1.5)

print("Testing move precise distance (20 cm)")
bot.move_distance(20, speed=70)


print("Testing rotate precise angle (90 deg)")
bot.rotate_angle(90, speed=70)

print("Dance time!")
bot.dance()

print("Joyful spin!")
bot.joyful_spin()

bot.stop()
print("Test completed.")
