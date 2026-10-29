# ottomotors v2.0 17.07.2024
import time
from machine import Pin, PWM

try:
    from esp32 import Servo as espServo
    useServo = True
except ImportError:
    """This version of esp32 doesn't support Servo, use PWM instead"""
    def espServo(_arg):
        print("espServo not defined")
        raise ImportError
    useServo = False

class OttoMotor: #used in web code blocks lacks of calibration offset

    def __init__(self, pin1, pin2):
        self.leftServo = PWM(Pin(pin2))
        self.leftServo.freq(50)
        self.rightServo = PWM(Pin(pin1))
        self.rightServo.freq(50)

    def Move(self, direction, step, speed):
        if(direction == -1):
            if(speed == 1):
                leftSpeed = 60
            elif(speed == 2):
                leftSpeed = 45
            elif(speed == 3):
                leftSpeed = 30

            if(speed == 1):
                rightSpeed = 100
            elif(speed == 2):
                rightSpeed = 115
            elif(speed == 3):
                rightSpeed = 130
        else:
            if(speed == 1):
                rightSpeed = 60
            elif(speed == 2):
                rightSpeed = 45
            elif(speed == 3):
                rightSpeed = 30

            if(speed == 1):
                leftSpeed = 100
            elif(speed == 2):
                leftSpeed = 115
            elif(speed == 3):
                leftSpeed = 130

        self.rightServo.freq(50)
        self.leftServo.freq(50)
        self.rightServo.duty(rightSpeed)
        self.leftServo.duty(leftSpeed)
        time.sleep(step)
        self.rightServo.duty(0)
        self.leftServo.duty(0)

    def Moveloop(self, direction, speed):
        if(direction == -1):
            if(speed == 1):
                leftSpeed = 60
            elif(speed == 2):
                leftSpeed = 45
            elif(speed == 3):
                leftSpeed = 30

            if(speed == 1):
                rightSpeed = 100
            elif(speed == 2):
                rightSpeed = 115
            elif(speed == 3):
                rightSpeed = 130
        else:
            if(speed == 1):
                rightSpeed = 60
            elif(speed == 2):
                rightSpeed = 45
            elif(speed == 3):
                rightSpeed = 30

            if(speed == 1):
                leftSpeed = 100
            elif(speed == 2):
                leftSpeed = 115
            elif(speed == 3):
                leftSpeed = 130

        self.rightServo.freq(50)
        self.leftServo.freq(50)
        self.rightServo.duty(rightSpeed)
        self.leftServo.duty(leftSpeed)

    def Rotate(self, turn):
        if(turn == 0):
            rightSpeed = 45
            leftSpeed = 45
            stepDelay = 0.4
        elif(turn == 1):
            rightSpeed = 115
            leftSpeed = 115
            stepDelay = 0.4
        elif(turn == 2):
            rightSpeed = 45
            leftSpeed = 45
            stepDelay = 0.8

        self.rightServo.freq(50)
        self.leftServo.freq(50)
        self.rightServo.duty(rightSpeed)
        self.leftServo.duty(leftSpeed)
        time.sleep(stepDelay)
        self.rightServo.duty(0)
        self.leftServo.duty(0)

    def Moveleft(self, direction, step, speed):
        if(direction == -1):
            if(speed == 1):
                leftSpeed = 60
            elif(speed == 2):
                leftSpeed = 45
            elif(speed == 3):
                leftSpeed = 30
        else:
            if(speed == 1):
                leftSpeed = 130
            elif(speed == 2):
                leftSpeed = 115
            elif(speed == 3):
                leftSpeed = 100

        self.rightServo.freq(50)
        self.leftServo.freq(50)
        self.leftServo.duty(leftSpeed)
        time.sleep(step)
        self.leftServo.duty(0)

    def Moveleftloop(self, direction, speed):
        if(direction == -1):
            if(speed == 1):
                leftSpeed = 60
            elif(speed == 2):
                leftSpeed = 45
            elif(speed == 3):
                leftSpeed = 30
        else:
            if(speed == 1):
                leftSpeed = 130
            elif(speed == 2):
                leftSpeed = 115
            elif(speed == 3):
                leftSpeed = 100

        self.leftServo.duty(leftSpeed)

    def Moveright(self, direction, step, speed):
        if(direction == -1):
            if(speed == 1):
                rightSpeed = 130
            elif(speed == 2):
                rightSpeed = 115
            elif(speed == 3):
                rightSpeed = 100
        else:
            if(speed == 1):
                rightSpeed = 60
            elif(speed == 2):
                rightSpeed = 45
            elif(speed == 3):
                rightSpeed = 30

        self.rightServo.freq(50)
        self.leftServo.freq(50)
        self.rightServo.duty(rightSpeed)
        time.sleep(step)
        self.rightServo.duty(0)

    def Moverightloop(self, direction, speed):
        if(direction == -1):
            if(speed == 1):
                rightSpeed = 130
            elif(speed == 2):
                rightSpeed = 115
            elif(speed == 3):
                rightSpeed = 100
        else:
            if(speed == 1):
                rightSpeed = 60
            elif(speed == 2):
                rightSpeed = 45
            elif(speed == 3):
                rightSpeed = 30

        self.rightServo.freq(50)
        self.leftServo.freq(50)
        self.rightServo.duty(rightSpeed)

    def Stop(self, motor):
        if(motor == 1):
            self.rightServo.duty(0)
            self.leftServo.duty(0)
        elif(motor ==  2):
            self.leftServo.duty(0)
        elif(motor ==  3):
            self.rightServo.duty(0)

class Servo: #used in web control main lacks of calibration offset.

    # Degrees/second used by moveTo() to sweep instead of jumping straight
    # to the target - this avoids the current spike a servo draws when it's
    # asked to slew its full range in one instant.
    DEFAULT_SPEED = 180

    # How long moveTo() holds the target position before cutting power.
    # Standard hobby servos keep drawing holding current for as long as
    # they're powered, so if they're left attached indefinitely (e.g.
    # fighting gravity or a mechanical stop) they can overheat; releasing
    # them once they've settled avoids that.
    RELEASE_DELAY = 0.3

    def __init__(self, freq=50, min_us=1000, max_us=2000, max_ang=180):
        global useServo
        self.min_us = min_us
        self.max_us = max_us
        self.freq = freq
        self.max_ang = max_ang
        self.pin = None
        self._pin_num = None
        self.current_angle = None
        if useServo:
            self.servo = None
        else:
            self.pwm = None
        self._attached = False

    def attach(self, pin):
        global useServo
        self._pin_num = pin
        self.pin = Pin(pin)
        if useServo:
            self.servo = espServo(self.pin)
        else:
            self.pwm = PWM(self.pin, freq=self.freq)
        self._attached = True

    def detach(self):
        global useServo
        if useServo:
            self.servo.deinit()
        else:
            self.pwm.deinit()
        self._attached = False

    def attached(self):
        return self._attached

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        global useServo
        if useServo:
            self.servo.duty(us)
        else:
            """PWM uses duty as a value from 0-1024"""
            duty = int(us / (1000000 / self.freq / 1024))
            self.pwm.duty(duty)

    def write(self, degrees):
        """Jump straight to ``degrees`` and keep holding torque there.
        No sweep, no auto-release - used internally for choreographed
        movements (walking/rolling gaits) that need tight, predictable
        timing. For a one-off move that shouldn't leave the servo
        overheating while idle, use moveTo() instead."""
        degrees = self._clamp(degrees)
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.max_ang
        self.write_us(us)
        self.current_angle = degrees

    def _clamp(self, degrees):
        if degrees < 0:
            return 0
        if degrees > 180:
            return 180
        return degrees

    def moveTo(self, target, speed=None, release=True):
        """Smoothly sweep to ``target`` degrees instead of jumping there,
        then (by default) release the servo so it stops drawing holding
        current once it's settled. Use for one-off/standalone positioning;
        gait code that needs precise timing should keep using write()."""
        if speed is None:
            speed = self.DEFAULT_SPEED
        if not self._attached:
            self.attach(self._pin_num)

        target = self._clamp(target)
        start = self.current_angle if self.current_angle is not None else target
        distance = abs(target - start)

        if distance == 0:
            self.write(target)
        else:
            steps = max(1, int(distance / 3))
            step_delay = (distance / speed) / steps
            for i in range(1, steps + 1):
                self.write(start + (target - start) * i // steps)
                time.sleep(step_delay)

        if release:
            time.sleep(self.RELEASE_DELAY)
            self.detach()

    def __deinit__(self):
        global useServo
        if useServo:
            self.servo.deinit()
        else:
            self.pwm.deinit()

class Motors: #used in web control main lacks of calibration offset, default pins need to move out of the library
    def __init__(self, right_motor_pin=13, left_motor_pin=14):
        self.right_motor = Servo()
        self.left_motor = Servo()
        self.right_motor.attach(right_motor_pin)
        self.left_motor.attach(left_motor_pin)

    def move(self, right_speed, left_speed, direction, t=None):
        if direction == "forward":
            self.right_motor.write(90 - right_speed)
            self.left_motor.write(left_speed + 90)
        elif direction == "backward":
            self.right_motor.write(right_speed + 90)
            self.left_motor.write(90 - left_speed)
        elif direction == "right":
            self.right_motor.write(right_speed + 90)
            self.left_motor.write(left_speed + 90)
        elif direction == "left":
            self.right_motor.write(90 - right_speed)
            self.left_motor.write(90 - left_speed)
        else:
            raise ValueError("Invalid direction")

        if t is not None:
            time.sleep(t)
            self.stop()

    def stop(self):
        self.right_motor.write(90)
        self.left_motor.write(90)
