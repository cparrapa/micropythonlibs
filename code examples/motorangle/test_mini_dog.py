# Test mini spider with 4 angle motors
# Author: Iván R. Artiles
# Date: October 4, 2024
import machine
import time

class Servo:
    def __init__(self, freq=50, min_us=1000, max_us=2000, max_ang=180):
        self.min_us = min_us
        self.max_us = max_us
        self.freq = freq
        self.max_ang = max_ang
        self.pin = None
        self.pwm = None
        self._attached = False

    def attach(self, pin):
        self.pin = machine.Pin(pin)
        self.pwm = machine.PWM(self.pin, freq=self.freq)
        self._attached = True

    def detach(self):
        self.pwm.deinit()
        self._attached = False

    def attached(self):
        return self._attached

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        duty = int(us / (1000000 / self.freq / 1024))
        self.pwm.duty(duty)

    def write(self, degrees):
        """Move to the specified angle in ``degrees``."""
        degrees = degrees % 360
        if degrees < 0:
            degrees += 360
        if degrees > 180:
            degrees = 180
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.max_ang
        self.write_us(us)

    def __deinit__(self):
        self.pwm.deinit()

# Attach servos to pins
servo1 = Servo()
servo2 = Servo()
servo3 = Servo()
servo4 = Servo()
servo1.attach(13) # Front left leg - Connector 11
servo2.attach(14) # Front right leg - Connector 10
servo3.attach(15) # Back left leg - Connector 9
servo4.attach(27) # Back right leg - Connector 8

def forward():
    # Step 1
    servo1.write(90)
    servo2.write(90)
    time.sleep(0.1)
    servo3.write(90)
    servo4.write(90)
    time.sleep(0.4)
    # Step 2
    servo1.write(60)
    servo4.write(120)
    time.sleep(0.5)
    # Step 3
    servo3.write(120)
    servo2.write(60)
    time.sleep(0.5)
    # Step 4
    servo1.write(90)
    servo4.write(90)
    time.sleep(0.5)
    # Step 5
    servo3.write(60)
    servo2.write(120)
    time.sleep(0.5)
    servo1.write(120)
    servo4.write(60)
    time.sleep(0.5)
    
    forward()
    
forward()