from DIYables_MicroPython_Servo import Servo
import utime

# Create a Servo object
servo = Servo(26) # The ESP32 pin GPIO26 connected to the servo motor

# Define the start and stop angles and the duration for the movement
start_angle = 30
stop_angle = 90
moving_time = 3000  # Duration in milliseconds

# Function to map the progress to an angle
def map_value(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Initial setup with timer
move_start_time = utime.ticks_ms()

# Main loop
while True:
    progress = utime.ticks_diff(utime.ticks_ms(), move_start_time)  # Calculate elapsed time since start

    if progress <= moving_time:
        # Calculate intermediate servo angle
        angle = map_value(progress, 0, moving_time, start_angle, stop_angle)
        servo.move_to_angle(angle)  # Set servo position to calculated angle
    else:
        # Optionally, restart the motion or break the loop
        move_start_time = utime.ticks_ms()  # Reset the timer to start the motion again