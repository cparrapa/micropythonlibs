from ottomotor import OttoMotor
from time import *

__version__ = "1.0.0"

class ottoMotorKB:
    def __init__(self):
        self.motor = OttoMotor(13, 14)
        self.offset = 0

    def set_offset(self, offset):
        self.offset = offset

    def move_step(self, dir, speed, step):
        setting = {
            0: [[95, 60], [109, 43], [127, 29]],
            1: [[60, 95], [43, 109], [29, 127]],
        }
        self.motor.leftServo.freq(50)
        self.motor.rightServo.freq(50)
        self.motor.leftServo.duty(setting[dir][speed][0] - self.offset)
        self.motor.rightServo.duty(setting[dir][speed][1] + self.offset)
        sleep(step)
        self.motor.rightServo.duty(0)
        self.motor.leftServo.duty(0)

    def move(self, dir, speed):
        setting = {
            0: [[95, 60], [109, 43], [127, 29]],
            1: [[60, 95], [43, 109], [29, 127]],
        }
        self.motor.leftServo.duty(setting[dir][speed][0] - self.offset)
        self.motor.rightServo.duty(setting[dir][speed][1] + self.offset)

    def rotate(self, dir, step):
        setting = [[45, 45], [115, 115]]
        self.motor.rightServo.duty(setting[dir][0] + self.offset)
        self.motor.leftServo.duty(setting[dir][1] - self.offset)
        sleep(step)
        self.motor.rightServo.duty(0)
        self.motor.leftServo.duty(0)

    def move_left_step(self, dir, step, speed):
        self.motor.Moveleft(dir, step, speed)

    def move_left(self, dir, speed):
        setting = {
            0: [95, 109, 127],
            1: [60, 43, 29],
        }
        self.motor.leftServo.duty(setting[dir][speed] - self.offset)

    def move_right_step(self, dir, step, speed):
        self.motor.Moveright(dir, step, speed)

    def move_right(self, dir, speed):
        setting = {
            0: [60, 43, 29],
            1: [95, 109, 127],
        }
        self.motor.rightServo.duty(setting[dir][speed] - self.offset)

    def stop(self,index):
        self.motor.Stop(index)
