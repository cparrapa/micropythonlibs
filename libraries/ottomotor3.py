# ottomotor.py v0.1.5 2.10.2026
# HP Robots servo / motor library for ESP32
import time
import json
from machine import Pin, PWM

CALIBRATION_FILE = "otto_cal.json"

# Use MicroPython PWM directly for every servo channel.
# This gives each GPIO its own PWM object and avoids shared-state behavior
# that can occur with the esp32.Servo helper when several servos are attached.
useServo = False


class HPServo:
    """Single servo channel with angle or continuous-rotation control."""

    def __init__(self, pin=None, mode='angle', freq=50, min_us=400, max_us=2600,
                 center_us=1500, max_ang=180, reverse=False, auto_attach=False):
        if mode not in ('angle', 'continuous'):
            raise ValueError('mode must be angle or continuous')
        if max_us <= min_us:
            raise ValueError('max_us must be greater than min_us')

        self.pin_number = pin
        self.mode = mode
        self.freq = int(freq)
        self.min_us = int(min_us)
        self.max_us = int(max_us)
        self.center_us = int(center_us)
        self.max_ang = int(max_ang)
        self.reverse = bool(reverse)
        self.pwm = None
        self._attached = False
        self.current_us = self.center_us

        if auto_attach and pin is not None:
            self.attach(pin)

    def attach(self, pin=None):
        if pin is not None:
            self.pin_number = pin
        if self.pin_number is None:
            raise ValueError('No servo pin specified')
        if self._attached:
            return

        p = Pin(self.pin_number)
        # Always use a dedicated PWM object for this GPIO.
        self.pwm = PWM(p, freq=self.freq)

        self._attached = True
        self._write_us(self.current_us)

    def detach(self):
        if not self._attached:
            return

        try:
            self.pwm.duty_u16(0)
        except AttributeError:
            self.pwm.duty(0)
        self.pwm.deinit()
        self.pwm = None

        self._attached = False

    release = detach

    def off(self):
        """Stop the PWM signal without destroying the PWM channel.

        This is the preferred way for OttoRobot to temporarily disable a
        servo. Keeping the PWM object alive prevents ESP32 LEDC channels /
        timers from being reallocated and disturbing other servos.
        """
        if not self._attached:
            return
        try:
            self.pwm.duty_u16(0)
        except AttributeError:
            self.pwm.duty(0)

    def attached(self):
        return self._attached

    def calibrate(self, min_us=None, max_us=None, center_us=None, reverse=None):
        if min_us is not None:
            self.min_us = int(min_us)
        if max_us is not None:
            self.max_us = int(max_us)
        if center_us is not None:
            self.center_us = int(center_us)
        if reverse is not None:
            self.reverse = bool(reverse)

        if self.max_us <= self.min_us:
            raise ValueError('max_us must be greater than min_us')

    def _clamp(self, us):
        return int(max(self.min_us, min(self.max_us, int(us))))

    def _write_us(self, us):
        us = self._clamp(us)
        if not self._attached:
            self.attach()

        period = 1000000 // self.freq
        duty = int(us * 65535 / period)
        try:
            self.pwm.duty_u16(duty)
        except AttributeError:
            self.pwm.duty(int(us / (1000000 / self.freq / 1024)))

        self.current_us = us

    def write_us(self, us):
        """Write pulse width in microseconds. 0 disables the servo signal."""
        if int(us) == 0:
            self.detach()
        else:
            self._write_us(us)

    # Alias kept for compatibility with earlier HPServo versions.
    pulse = write_us

    def _angle_to_us(self, degrees):
        degrees = max(0, min(self.max_ang, float(degrees)))
        if self.reverse:
            degrees = self.max_ang - degrees
        return int(self.min_us + (self.max_us - self.min_us) * degrees / self.max_ang)

    def write(self, degrees):
        if self.mode == 'angle':
            self._write_us(self._angle_to_us(degrees))
        else:
            self._write_us(self._speed_to_us((float(degrees) - 90) * 100 / 90))

    def angle(self, degrees):
        if self.mode != 'angle':
            raise ValueError('angle() requires an angle servo')
        self.write(degrees)

    def _speed_to_us(self, percent):
        percent = max(-100, min(100, float(percent)))
        if self.reverse:
            percent = -percent

        if percent >= 0:
            return int(self.center_us + (self.max_us - self.center_us) * percent / 100)
        return int(self.center_us + (self.min_us - self.center_us) * (-percent) / 100)

    def speed(self, percent):
        if self.mode != 'continuous':
            raise ValueError('speed() requires a continuous servo')
        self._write_us(self._speed_to_us(percent))

    def _move_smooth(self, target, duration_ms=500, steps=None):
        if not self._attached:
            self.attach()

        target = self._clamp(target)
        start = self.current_us
        if start == target:
            return

        duration_ms = max(0, int(duration_ms))
        if duration_ms == 0:
            self._write_us(target)
            return

        if steps is None:
            steps = max(1, duration_ms // 20)
        steps = max(1, int(steps))
        delay = max(1, duration_ms // steps)

        for i in range(1, steps + 1):
            self._write_us(start + (target - start) * i // steps)
            time.sleep_ms(delay)

    def angle_smooth(self, degrees, duration_ms=500, hold=True):
        if self.mode != 'angle':
            raise ValueError('angle_smooth() requires an angle servo')
        self._move_smooth(self._angle_to_us(degrees), duration_ms)
        if not hold:
            self.detach()

    def speed_smooth(self, percent, duration_ms=400):
        if self.mode != 'continuous':
            raise ValueError('speed_smooth() requires a continuous servo')
        self._move_smooth(self._speed_to_us(percent), duration_ms)

    def center(self, hold=True):
        if self.mode == 'angle':
            self.angle_smooth(self.max_ang / 2, 400, hold)
        else:
            self.speed(0)
            if not hold:
                self.detach()

    def hold(self):
        self.attach()

    def hold_for(self, milliseconds):
        self.attach()
        time.sleep_ms(max(0, int(milliseconds)))
        self.detach()

    def stop(self, smooth=False, duration_ms=300, release=False):
        if self.mode != 'continuous':
            raise ValueError('stop() requires a continuous servo')
        if smooth:
            self.speed_smooth(0, duration_ms)
        else:
            self.speed(0)
        if release:
            self.detach()

    def __deinit__(self):
        self.detach()


class Servo(HPServo):
    """Backward-compatible Servo API from the previous library."""

    def __init__(self, freq=50, min_us=1000, max_us=2000, max_ang=180,
                 center_us=1500, reverse=False):
        super().__init__(None, 'angle', freq, min_us, max_us,
                         center_us, max_ang, reverse, False)


class OttoMotor:
    """Backward-compatible two-wheel API.

    pin1 = right wheel GPIO, pin2 = left wheel GPIO.
    """

    def __init__(self, pin1, pin2, left_cal=None, right_cal=None):
        d = {'min_us': 400, 'max_us': 2600, 'center_us': 1500, 'reverse': False}
        l = d.copy()
        r = d.copy()
        l.update(left_cal or {})
        r.update(right_cal or {})
        self.leftServo = HPServo(pin2, 'continuous', **l)
        self.rightServo = HPServo(pin1, 'continuous', **r)

    @staticmethod
    def _validate_motion(direction, speed):
        if direction not in (-1, 1):
            raise ValueError('Invalid direction')
        if speed not in (1, 2, 3):
            raise ValueError('Invalid speed')

    @staticmethod
    def _speed_values(direction, speed):
        vals = {1: (60, 100), 2: (45, 115), 3: (30, 130)}
        a, b = vals[speed]
        if direction == -1:
            left, right = a, b
        else:
            left, right = b, a
        return int(left * 20000 / 1024), int(right * 20000 / 1024)

    def Move(self, direction, step, speed):
        self._validate_motion(direction, speed)
        l, r = self._speed_values(direction, speed)
        self.leftServo.write_us(l)
        self.rightServo.write_us(r)
        time.sleep(step)
        self.Stop(1)

    def Moveloop(self, direction, speed):
        self._validate_motion(direction, speed)
        l, r = self._speed_values(direction, speed)
        self.leftServo.write_us(l)
        self.rightServo.write_us(r)

    def Rotate(self, turn):
        if turn not in (0, 1, 2):
            raise ValueError('Invalid turn')
        if turn == 0:
            pulse = int(45 * 20000 / 1024)
            delay = 0.4
        elif turn == 1:
            pulse = int(115 * 20000 / 1024)
            delay = 0.4
        else:
            pulse = int(45 * 20000 / 1024)
            delay = 0.8
        self.leftServo.write_us(pulse)
        self.rightServo.write_us(pulse)
        time.sleep(delay)
        self.Stop(1)

    def Moveleft(self, direction, step, speed):
        self._validate_motion(direction, speed)
        l, _ = self._speed_values(direction, speed)
        self.leftServo.write_us(l)
        time.sleep(step)
        self.Stop(2)

    def Moveleftloop(self, direction, speed):
        self._validate_motion(direction, speed)
        l, _ = self._speed_values(direction, speed)
        self.leftServo.write_us(l)

    def Moveright(self, direction, step, speed):
        self._validate_motion(direction, speed)
        _, r = self._speed_values(direction, speed)
        self.rightServo.write_us(r)
        time.sleep(step)
        self.Stop(3)

    def Moverightloop(self, direction, speed):
        self._validate_motion(direction, speed)
        _, r = self._speed_values(direction, speed)
        self.rightServo.write_us(r)

    def Stop(self, motor):
        if motor == 1:
            self.leftServo.detach()
            self.rightServo.detach()
        elif motor == 2:
            self.leftServo.detach()
        elif motor == 3:
            self.rightServo.detach()
        else:
            raise ValueError('Invalid motor')


class OttoRobot:
    """Four-servo HP robot with persistent independent PWM channels.

    GPIO pins are supplied by the user's program. Wheel calibration is kept
    separately from servo calibration and can be saved explicitly to the
    ESP32 flash as JSON. The file is written only when save_calibration() is
    called, so normal driving does not cause flash wear.
    """

    def __init__(self, left_angle_pin, right_angle_pin, left_wheel_pin, right_wheel_pin,
                 left_angle_cal=None, right_angle_cal=None,
                 left_wheel_cal=None, right_wheel_cal=None,
                 calibration_file=CALIBRATION_FILE, load_calibration=True):
        d = {'min_us': 400, 'max_us': 2600, 'center_us': 1500, 'reverse': False}

        def c(x):
            q = d.copy()
            q.update(x or {})
            return q

        self.calibration_file = calibration_file
        # IMPORTANT: create all four PWM channels up front, just like the
        # proven raw-PWM test. Do not dynamically attach/deinit these during
        # normal robot operation.
        self.left_angle = HPServo(left_angle_pin, 'angle', **c(left_angle_cal))
        self.right_angle = HPServo(right_angle_pin, 'angle', **c(right_angle_cal))
        self.left_wheel = HPServo(left_wheel_pin, 'continuous', **c(left_wheel_cal))
        self.right_wheel = HPServo(right_wheel_pin, 'continuous', **c(right_wheel_cal))

        # Robot-level wheel calibration. These values are deliberately
        # separate from the servo's electrical center/reverse calibration.
        self.left_trim = 1.0
        self.right_trim = 1.0
        self.turn_90_ms = 400
        self.turn_speed = 50

        if load_calibration:
            self.load_calibration()

        # Create all four PWM channels up front and keep them allocated.
        self.left_angle.attach()
        self.right_angle.attach()
        self.left_wheel.attach()
        self.right_wheel.attach()

        # Start every output at its safe neutral/center command.
        self.left_angle._write_us(self.left_angle.current_us)
        self.right_angle._write_us(self.right_angle.current_us)
        self.left_wheel._write_us(self.left_wheel.center_us)
        self.right_wheel._write_us(self.right_wheel.center_us)

    # -------------------------
    # Persistent calibration
    # -------------------------

    def calibration(self):
        """Return the current robot-level calibration values."""
        return {
            'left_trim': self.left_trim,
            'right_trim': self.right_trim,
            'turn_90_ms': self.turn_90_ms,
            'turn_speed': self.turn_speed,
        }

    def set_calibration(self, left_trim=None, right_trim=None,
                        turn_90_ms=None, turn_speed=None):
        """Change robot-level calibration without writing flash."""
        if left_trim is not None:
            self.left_trim = max(0.5, min(1.5, float(left_trim)))
        if right_trim is not None:
            self.right_trim = max(0.5, min(1.5, float(right_trim)))
        if turn_90_ms is not None:
            self.turn_90_ms = max(1, int(turn_90_ms))
        if turn_speed is not None:
            self.turn_speed = max(1, min(100, float(turn_speed)))

    def save_calibration(self):
        """Save robot calibration to ESP32 flash.

        Call this only when calibration has changed. Do not call on every
        movement because flash has a finite write endurance.
        """
        data = self.calibration()
        with open(self.calibration_file, 'w') as f:
            json.dump(data, f)
        print('Calibration saved:', data)

    def load_calibration(self):
        """Load saved robot calibration. Returns True if found."""
        try:
            with open(self.calibration_file, 'r') as f:
                data = json.load(f)
            self.set_calibration(
                data.get('left_trim'),
                data.get('right_trim'),
                data.get('turn_90_ms'),
                data.get('turn_speed'))
            print('Calibration loaded:', self.calibration())
            return True
        except (OSError, ValueError, TypeError):
            print('No saved robot calibration found. Using defaults.')
            return False

    def reset_calibration(self, save=False):
        self.left_trim = 1.0
        self.right_trim = 1.0
        self.turn_90_ms = 400
        self.turn_speed = 50
        if save:
            self.save_calibration()

    # -------------------------
    # Wheel calibration helpers
    # -------------------------

    def wheel_test(self, speed=50, duration_ms=2000):
        """Drive both wheels with calibration applied for testing straightness."""
        self.set_wheels(speed, speed, False)
        time.sleep_ms(max(0, int(duration_ms)))
        self.stop()

    def _calibrated_speed(self, speed, trim):
        speed = float(speed)
        return max(-100, min(100, speed * trim))

    def set_wheels(self, left_speed, right_speed, smooth=False, duration_ms=400):
        # Apply independent wheel trim. This is the main straight-line
        # calibration: if the robot veers left, reduce left trim or increase
        # right trim; if it veers right, do the opposite.
        left_speed = self._calibrated_speed(left_speed, self.left_trim)
        right_speed = self._calibrated_speed(right_speed, self.right_trim)

        lt = self.left_wheel._speed_to_us(left_speed)
        rt = self.right_wheel._speed_to_us(right_speed)

        if not smooth:
            self.left_wheel._write_us(lt)
            self.right_wheel._write_us(rt)
            return

        ls = self.left_wheel.current_us
        rs = self.right_wheel.current_us
        duration_ms = max(0, int(duration_ms))

        if duration_ms == 0:
            self.left_wheel._write_us(lt)
            self.right_wheel._write_us(rt)
            return

        steps = max(1, duration_ms // 20)
        delay = max(1, duration_ms // steps)
        for i in range(1, steps + 1):
            self.left_wheel._write_us(ls + (lt - ls) * i // steps)
            self.right_wheel._write_us(rs + (rt - rs) * i // steps)
            time.sleep_ms(delay)

    def forward(self, speed, smooth=False, duration_ms=400):
        self.set_wheels(abs(speed), abs(speed), smooth, duration_ms)

    def backward(self, speed, smooth=False, duration_ms=400):
        self.set_wheels(-abs(speed), -abs(speed), smooth, duration_ms)

    def drive(self, speed, smooth=False, duration_ms=400):
        self.forward(speed, smooth, duration_ms)

    def turn_left(self, speed, smooth=False, duration_ms=None):
        speed = abs(speed)
        if duration_ms is None:
            duration_ms = self.turn_duration(speed)
        self.set_wheels(-speed, speed, smooth, duration_ms)

    def turn_right(self, speed, smooth=False, duration_ms=None):
        speed = abs(speed)
        if duration_ms is None:
            duration_ms = self.turn_duration(speed)
        self.set_wheels(speed, -speed, smooth, duration_ms)

    def turn_duration(self, speed):
        """Estimate duration for a 90-degree turn from the calibrated speed."""
        speed = max(1, min(100, abs(float(speed))))
        return max(1, int(self.turn_90_ms * self.turn_speed / speed))

    def turn_left_90(self, speed=None, smooth=False):
        if speed is None:
            speed = self.turn_speed
        self.turn_left(speed, smooth, self.turn_duration(speed))

    def turn_right_90(self, speed=None, smooth=False):
        if speed is None:
            speed = self.turn_speed
        self.turn_right(speed, smooth, self.turn_duration(speed))

    def stop(self, smooth=False, duration_ms=300, release=False):
        self.set_wheels(0, 0, smooth, duration_ms)
        if release:
            self.left_wheel.off()
            self.right_wheel.off()

    def release_wheels(self):
        """Disable wheel pulses while keeping their PWM channels allocated."""
        self.left_wheel.off()
        self.right_wheel.off()

    def release_angles(self):
        """Disable angle-servo pulses while keeping PWM channels allocated."""
        self.left_angle.off()
        self.right_angle.off()

    def release_all(self):
        """Disable all servo signals without deinitializing PWM channels."""
        self.left_angle.off()
        self.right_angle.off()
        self.left_wheel.off()
        self.right_wheel.off()

    def deinit(self):
        """Fully release all PWM resources when the robot is no longer used."""
        self.left_angle.detach()
        self.right_angle.detach()
        self.left_wheel.detach()
        self.right_wheel.detach()


def create_robot(left_angle_pin, right_angle_pin, left_wheel_pin, right_wheel_pin,
                 left_angle_cal=None, right_angle_cal=None,
                 left_wheel_cal=None, right_wheel_cal=None):
    """Convenience factory. GPIO pins must be supplied by the user's code."""
    return OttoRobot(left_angle_pin, right_angle_pin, left_wheel_pin, right_wheel_pin,
                     left_angle_cal, right_angle_cal, left_wheel_cal, right_wheel_cal)
