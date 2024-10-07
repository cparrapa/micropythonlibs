# ottomotors v2.0 17.07.2024
import machine, time
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
    def __init__(self, freq=50, min_us=1000, max_us=2000, max_ang=180):
        global useServo
        self.min_us = min_us
        self.max_us = max_us
        self.freq = freq
        self.max_ang = max_ang
        self.pin = None
        if useServo:
            self.servo = None
        else:
            self.pwm = None
        self._attached = False

    def attach(self, pin):
        global useServo
        self.pin = machine.Pin(pin)
        if useServo:
            self.servo = espServo(self.pin)
        else:
            self.pwm = machine.PWM(self.pin, freq=self.freq)
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
        global useServo
        if useServo:
            self.servo.deinit()
        else:
            self.pwm.deinit()

class Motors: #used in web control main lacks of calibration offset, default pins need to move out of the library
    def __init__(self, right_motor_pin=13, left_motor_pin=14):
        self.right_motor = Servo()
        self.left_motor = Servo()
        self.right_motor_pin = right_motor_pin
        self.left_motor_pin = left_motor_pin

    def move(self, right_speed, left_speed, direction, t=None):
        self.right_motor.attach(self.right_motor_pin)
        self.left_motor.attach(self.left_motor_pin)

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
        self.right_motor.attach(self.right_motor_pin)
        self.left_motor.attach(self.left_motor_pin)
        self.right_motor.write(90)
        self.left_motor.write(90)
