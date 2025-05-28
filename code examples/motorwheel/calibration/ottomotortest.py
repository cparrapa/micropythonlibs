# ottomotors v3.0 26.05.2025 calibration under TEST
import time
import ujson  # For JSON storage
from machine import Pin, PWM

CALIBRATION_FILE = "calibration.json"  # File to store calibration offsets

def map_range(x, in_min, in_max, out_min, out_max):
    # Convert x from one range to another.
    return out_min + (float(x - in_min) * (out_max - out_min)) / (in_max - in_min)

class Motor:
    def __init__(self, pin, calibration_offset=0):
        # Initialize PWM on the specified pin at 50 Hz.
        self.servo = PWM(Pin(pin), freq=50)
        self.calibration_offset = calibration_offset

    def set_speed_percent(self, speed_percent):
        """
        Sets motor speed based on a percentage (-100 to 100).
        For positive speeds (counter-clockwise): maps 0% -> duty 95, 100% -> duty 130.
        For negative speeds (clockwise): maps 0% -> duty 60, 100% -> duty 30.
        At 0% the motor is stopped (neutral duty 90).
        """
        if speed_percent > 0:
            duty = map_range(speed_percent, 0, 100, 95, 130)
        elif speed_percent < 0:
            duty = map_range(abs(speed_percent), 0, 100, 60, 30)
        else:
            duty = 90  # Neutral (stop)
        duty += self.calibration_offset
        self.servo.duty(int(duty))

    def stop(self):
        # Stops the motor by setting it to the neutral duty.
        self.servo.duty(90)


class OttoMotors:
    # Physical constants – adjust these to match your robot’s configuration.
    WHEEL_DIAMETER_CM = 6.0    # Wheel diameter in centimeters
    ROBOT_WIDTH_CM = 8.0      # Distance between the wheels
    MAX_SPEED_CM_PER_SEC = 5   # At 100% motor command, maximum linear speed (cm/s)

    def __init__(self, left_pin, right_pin):
        # Load calibration offsets and instantiate motors.
        offsets = self.load_offsets()
        left_calibration = offsets.get("left", 0)
        right_calibration = offsets.get("right", 0)
        
        self.left_motor = Motor(left_pin, left_calibration)
        self.right_motor = Motor(right_pin, right_calibration)

    def save_offsets(self, left_offset, right_offset):
        """Save calibration offsets (for left and right motors) to a JSON file."""
        offsets = {"left": left_offset, "right": right_offset}
        with open(CALIBRATION_FILE, "w") as f:
            ujson.dump(offsets, f)
        print("Offsets saved!")

    def load_offsets(self):
        """Load calibration offsets from the JSON file (returns default offsets if not found)."""
        try:
            with open(CALIBRATION_FILE, "r") as f:
                return ujson.load(f)
        except (OSError, ValueError):
            print("No calibration file found, using default offsets.")
            return {"left": 0, "right": 0}

    def calculate_speeds(self, direction, speed_percent):
        """
        Determines left and right motor percentage commands based on the desired direction.
        For a pivot turn ("left" or "right"), one motor runs at half the speed.
        """
        if direction == "forward":
            return speed_percent, speed_percent
        elif direction == "backward":
            return -speed_percent, -speed_percent
        elif direction == "left":
            return speed_percent // 2, speed_percent
        elif direction == "right":
            return speed_percent, speed_percent // 2
        else:
            raise ValueError("Invalid direction specified: " + str(direction))

    def move(self, direction, speed_percent, duration):
        """
        Moves the robot in the specified direction (forward, backward, left, right)
        at a given speed percentage for a given duration (in seconds).
        """
        left_speed, right_speed = self.calculate_speeds(direction, speed_percent)
        self.left_motor.set_speed_percent(left_speed)
        self.right_motor.set_speed_percent(right_speed)
        time.sleep(duration)
        self.stop()

    def rotate(self, angle, speed_percent):
        """
        Rotates the robot by the specified angle in degrees.
          - Positive angle: right turn.
          - Negative angle: left turn.
          
        The effective wheel speed is computed from the percentage and MAX_SPEED_CM_PER_SEC.
        For an in-place rotation using differential drive:
            Angular speed ω = (2*v)/ROBOT_WIDTH,
        so time to rotate (in seconds) is:
            t = (angle in radians * ROBOT_WIDTH)/(2*v)
        """
        effective_speed = (abs(speed_percent) / 100.0) * self.MAX_SPEED_CM_PER_SEC
        if effective_speed == 0:
            print("Speed is zero, cannot rotate.")
            return
        angle_rad = abs(angle) * 3.14 / 180.0
        rotation_time = (angle_rad * self.ROBOT_WIDTH_CM) / (2 * effective_speed)
        if angle > 0:
            # For a right turn: left wheel goes forward, right wheel backward.
            self.left_motor.set_speed_percent(speed_percent)
            self.right_motor.set_speed_percent(-speed_percent)
        elif angle < 0:
            # For a left turn: left wheel goes backward, right wheel forward.
            self.left_motor.set_speed_percent(-speed_percent)
            self.right_motor.set_speed_percent(speed_percent)
        else:
            return
        time.sleep(rotation_time)
        self.stop()
        
    def stop(self):
        # Stop both motors.
        self.left_motor.stop()
        self.right_motor.stop()

    def move_distance(self, distance_cm, speed_percent):
        """
        Moves the robot forward for the specified distance.
        The duration is determined from the effective linear speed.
        """
        effective_speed = (abs(speed_percent) / 100.0) * self.MAX_SPEED_CM_PER_SEC
        if effective_speed == 0:
            print("Speed is zero, cannot move.")
            return
        duration = distance_cm / effective_speed
        self.move("forward", speed_percent, duration)

