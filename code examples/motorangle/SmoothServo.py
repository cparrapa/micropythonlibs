"""
SmoothServo.py
Small, independent servo-control library for MicroPython / ESP32.

Designed for:
- 180-degree positional servos
- Continuous-rotation wheel servos
- Independent PWM per GPIO
- Microsecond pulse calibration
- Smooth speed-controlled movement
- Optional release/detach to reduce servo heating

Typical servo frequency: 50 Hz.

Example hardware configuration:
    Angle servos: GPIO 27, GPIO 15
    Left wheel:   GPIO 14
    Right wheel:  GPIO 13

NOTE:
Servos should normally be powered from a suitable external 5 V supply.
Connect ESP32 GND and servo-supply GND together.
Do not power multiple servos from the ESP32 5 V/3.3 V pin.
"""

from machine import Pin, PWM
import time


class SmoothServo:
    """
    One independent servo on one GPIO.

    mode:
        "angle"      = 0..180 degree positional servo
        "continuous" = -100..100 speed control

    pulse calibration:
        min_us / max_us are the physical pulse limits.
        For the user's typical servos:
            angle:      400..2600 us
            continuous: 400..2600 us
    """

    def __init__(
        self,
        pin,
        mode="angle",
        freq=50,
        min_us=400,
        max_us=2600,
        center_us=1500,
        reverse=False,
        start=True,
    ):
        self.pin_number = pin
        self.mode = mode
        self.freq = freq
        self.min_us = min_us
        self.max_us = max_us
        self.center_us = center_us
        self.reverse = reverse

        self.pwm = PWM(Pin(pin), freq=freq)

        self.current_us = center_us
        self.target_us = center_us
        self._attached = False

        if start:
            self.attach()
            self._write_us(center_us)

    # ---------------------------------------------------------
    # Low-level PWM
    # ---------------------------------------------------------

    def _us_to_duty_u16(self, us):
        # One PWM period in microseconds.
        period_us = 1_000_000 // self.freq
        us = max(0, min(period_us, int(us)))
        return int((us * 65535) / period_us)

    def _write_us(self, us):
        us = int(max(self.min_us, min(self.max_us, us)))
        self.pwm.duty_u16(self._us_to_duty_u16(us))
        self.current_us = us

    def attach(self):
        """Enable PWM output."""
        if not self._attached:
            self.pwm = PWM(Pin(self.pin_number), freq=self.freq)
            self._attached = True

    def detach(self):
        """
        Stop PWM output.

        Useful for positional servos when they do not need to hold
        their position. This can dramatically reduce heating/current.
        """
        if self._attached:
            self.pwm.duty_u16(0)
            self.pwm.deinit()
            self._attached = False

    def release(self):
        """Alias for detach()."""
        self.detach()

    # ---------------------------------------------------------
    # Pulse control
    # ---------------------------------------------------------

    def pulse(self, us):
        """Directly set a pulse width in microseconds."""
        if not self._attached:
            self.attach()
        self._write_us(us)

    def pulse_smooth(self, target_us, duration_ms=500, steps=None):
        """
        Smoothly move from the current pulse to target_us.

        duration_ms controls movement speed.
        """
        if not self._attached:
            self.attach()

        target_us = int(max(self.min_us, min(self.max_us, target_us)))
        start_us = self.current_us

        if start_us == target_us:
            return

        distance = abs(target_us - start_us)

        if steps is None:
            # About 50 updates/sec is smooth enough for most servos.
            steps = max(1, int(duration_ms / 20))

        step_delay = max(1, int(duration_ms / steps))

        for i in range(1, steps + 1):
            # Linear interpolation.
            us = start_us + ((target_us - start_us) * i // steps)
            self._write_us(us)
            time.sleep_ms(step_delay)

    # ---------------------------------------------------------
    # Positional servo
    # ---------------------------------------------------------

    def angle(self, degrees):
        """
        Move positional servo immediately to an angle.

        0 degrees = min_us
        180 degrees = max_us
        """
        if self.mode != "angle":
            raise ValueError("angle() requires mode='angle'")

        degrees = max(0, min(180, degrees))

        if self.reverse:
            degrees = 180 - degrees

        us = self.min_us + (
            (self.max_us - self.min_us) * degrees // 180
        )

        self.pulse(us)

    def angle_smooth(self, degrees, duration_ms=500):
        """Smoothly move to an angle over duration_ms."""
        if self.mode != "angle":
            raise ValueError("angle_smooth() requires mode='angle'")

        degrees = max(0, min(180, degrees))

        if self.reverse:
            degrees = 180 - degrees

        target_us = self.min_us + (
            (self.max_us - self.min_us) * degrees // 180
        )

        self.pulse_smooth(target_us, duration_ms)

    # ---------------------------------------------------------
    # Continuous rotation servo
    # ---------------------------------------------------------

    def speed(self, percent):
        """
        Set continuous-rotation speed.

        -100 = full speed one direction
           0 = stop
        +100 = full speed opposite direction

        The direction depends on the servo calibration.
        """
        if self.mode != "continuous":
            raise ValueError("speed() requires mode='continuous'")

        percent = max(-100, min(100, percent))

        if self.reverse:
            percent = -percent

        if percent >= 0:
            us = self.center_us + (
                (self.max_us - self.center_us) * percent // 100
            )
        else:
            us = self.center_us + (
                (self.min_us - self.center_us) * (-percent) // 100
            )

        self.pulse(us)

    def speed_smooth(self, percent, duration_ms=500):
        """Smoothly change continuous-rotation speed."""
        if self.mode != "continuous":
            raise ValueError("speed_smooth() requires mode='continuous'")

        percent = max(-100, min(100, percent))

        if self.reverse:
            percent = -percent

        if percent >= 0:
            target_us = self.center_us + (
                (self.max_us - self.center_us) * percent // 100
            )
        else:
            target_us = self.center_us + (
                (self.min_us - self.center_us) * (-percent) // 100
            )

        self.pulse_smooth(target_us, duration_ms)

    def stop(self, smooth=False, duration_ms=300, release=False):
        """
        Stop a continuous servo.

        smooth=True gently reduces speed to zero.
        release=True disables PWM after stopping.
        """
        if self.mode == "continuous":
            if smooth:
                self.speed_smooth(0, duration_ms)
            else:
                self.speed(0)

        if release:
            self.detach()

    # ---------------------------------------------------------
    # Convenience
    # ---------------------------------------------------------

    def center(self):
        """Move to the calibrated center pulse."""
        self.pulse(self.center_us)

    def is_attached(self):
        return self._attached


class ServoPair:
    """Convenience class for a left/right continuous servo pair."""

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def drive(self, speed, smooth=False, duration_ms=300):
        """Both wheels forward/backward at the same speed."""
        if smooth:
            self.left.speed_smooth(speed, duration_ms)
            self.right.speed_smooth(speed, duration_ms)
        else:
            self.left.speed(speed)
            self.right.speed(speed)

    def stop(self, smooth=False, duration_ms=300, release=False):
        self.left.stop(smooth, duration_ms, release)
        self.right.stop(smooth, duration_ms, release)

    def turn(self, speed, smooth=False, duration_ms=300):
        """
        Rotate in place.

        Positive speed = left forward / right backward.
        Negative speed = left backward / right forward.
        """
        if smooth:
            self.left.speed_smooth(speed, duration_ms)
            self.right.speed_smooth(-speed, duration_ms)
        else:
            self.left.speed(speed)
            self.right.speed(-speed)
