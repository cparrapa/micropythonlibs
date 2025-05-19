import machine, time
import ujson  # For JSON storage
from machine import Pin, PWM

# File to store calibration offsets
CALIBRATION_FILE = "calibration.json"

class Motor:
    def _init_(self, pin, calibration_offset=0):
        self.servo = PWM(Pin(pin), freq=50)
        self.calibration_offset = calibration_offset

    def set_speed(self, speed):
        # Adjust speed with calibration offset
        neutral_pwm = 90  # Neutral point at 90 degrees (1.5 ms)
        adjusted_speed = neutral_pwm + speed + self.calibration_offset
        self.servo.duty(int(adjusted_speed))

    def stop(self):
        self.servo.duty(90)  # Stop at neutral point
        
     WHEEL_DIAMETER_CM = 6.5  # Adjust based on your robot's wheel diameter
    ROBOT_WIDTH_CM = 12.0  # Adjust based on your robot's width (wheel-to-wheel distance)

    def rotate(self, angle, speed):
        # Calculate duration for the rotation based on the robot's width and wheel diameter
        rotation_time = (self.ROBOT_WIDTH_CM * 3.14 * angle / 360) / (self.WHEEL_DIAMETER_CM * 3.14 * speed)
        if angle > 0:  # Positive angle for right turn
            self.left_motor.set_speed(speed)
            self.right_motor.set_speed(-speed)
        else:  # Negative angle for left turn
            self.left_motor.set_speed(-speed)
            self.right_motor.set_speed(speed)

        time.sleep(abs(rotation_time))
        self.stop()

    def move_distance(self, distance_cm, speed):
        # Calculate duration for the movement
        rotation_time = distance_cm / (self.WHEEL_DIAMETER_CM * 3.14 * speed)
        self.move("forward", speed, rotation_time)


class OttoMotors:
    def _init_(self, left_pin, right_pin):
        # Load calibration offsets
        offsets = self.load_offsets()
        left_calibration = offsets.get("left", 0)
        right_calibration = offsets.get("right", 0)

        self.left_motor = Motor(left_pin, left_calibration)
        self.right_motor = Motor(right_pin, right_calibration)

    def save_offsets(self, left_offset, right_offset):
        """Save calibration offsets to file."""
        offsets = {
            "left": left_offset,
            "right": right_offset
        }
        with open(CALIBRATION_FILE, "w") as f:
            ujson.dump(offsets, f)
        print("Offsets saved!")

    def load_offsets(self):
        """Load calibration offsets from file."""
        try:
            with open(CALIBRATION_FILE, "r") as f:
                return ujson.load(f)
        except (OSError, ValueError):
            print("No calibration file found, using default offsets.")
            return {"left": 0, "right": 0}

    def move(self, direction, speed, duration):
        left_speed, right_speed = self.calculate_speeds(direction, speed)
        self.left_motor.set_speed(left_speed)
        self.right_motor.set_speed(right_speed)
        time.sleep(duration)
        self.stop()

    def calculate_speeds(self, direction, speed):
        if direction == "forward":
            return speed, speed
        elif direction == "backward":
            return -speed, -speed
        elif direction == "left":
            return speed // 2, speed
        elif direction == "right":
            return speed, speed // 2
        else:
            raise ValueError("Invalid direction")

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()