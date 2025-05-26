from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
import machine, time                       #importing machine and time libraries
from ottomotortest import OttoMotors

def test_otto_motors():
    # Instantiate OttoMotors with designated pins.
    motors = OttoMotors(left_pin=15, right_pin=16)
    
    print("=== Testing move forward at 50% ===")
    motors.move("forward", speed_percent=50, duration=2)  # Move forward at 50% for 2 seconds
    time.sleep(1)
    
    print("=== Testing move backward at 50% ===")
    motors.move("backward", speed_percent=50, duration=2)  # Move backward at 50% for 2 seconds
    time.sleep(1)
    
    print("=== Testing turn left (pivot) at 50% ===")
    motors.move("left", speed_percent=50, duration=2)  # Pivot left
    time.sleep(1)
    
    print("=== Testing turn right (pivot) at 50% ===")
    motors.move("right", speed_percent=50, duration=2)  # Pivot right
    time.sleep(1)
    
    print("=== Testing rotate 90° to right at 50% ===")
    motors.rotate(angle=90, speed_percent=50)  # Rotate 90 degrees right
    time.sleep(1)
    
    print("=== Testing rotate 90° to left at 50% ===")
    motors.rotate(angle=-90, speed_percent=50)  # Rotate 90 degrees left
    time.sleep(1)
    
    print("=== Testing move forward 50 cm at 50% speed ===")
    motors.move_distance(distance_cm=50, speed_percent=50)  # Move 50 cm forward
    time.sleep(1)
    
    print("=== Testing calibration storage ===")
    motors.save_offsets(left_offset=5, right_offset=-5)
    offsets = motors.load_offsets()
    print("Loaded Offsets:", offsets)
    
    print("=== Testing stop functionality ===")
    motors.stop()  # Ensure motors are stopped
    
    print("=== All tests completed successfully ===")

if __name__ == "__main__":
    test_otto_motors()
