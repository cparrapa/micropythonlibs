import time
import urandom # type: ignore
from servo_lib import NeutralPositions

class RobotMoves:
    def __init__(self, servos, LF, RF, LL, RL, LA, RA):
        self.servos = servos
        self.LF = LF
        self.RF = RF
        self.LL = LL
        self.RL = RL
        self.LA = LA
        self.RA = RA
        self.npos = NeutralPositions()

    def return_to_neutral(self):
        self.servos.set_speeds(self.LF, self.npos.LFN, self.RF, self.npos.RFN) # Stop 360° servos
        self.servos.move_to_angles(self.LL, self.npos.LLN, self.RL, self.npos.RLN)
        self.servos.move_to_angles(self.LA, self.npos.LAN, self.RA, self.npos.RAN)

    def tilt_right(self):
        self.servos.move_to_angles(self.LL, self.npos.LLTR, self.RL, self.npos.RLTR)
        time.sleep(0.05)

    def tilt_left(self):
        self.servos.move_to_angles(self.LL, self.npos.LLTL, self.RL, self.npos.RLTL)
        time.sleep(0.05)

    def ride_position(self):
        self.servos.move_to_angles(self.LL, self.npos.LLR, self.RL, self.npos.RLR, step=10, delay=0.02)
        time.sleep(0.5)

    def left_forward(self):
        self.tilt_right()
        self.servos.set_speed(self.RF, self.npos.RFF)

    def right_forward(self):
        self.tilt_left()
        self.servos.set_speed(self.LF, self.npos.LFF)

    def left_back(self):
        self.tilt_right()
        self.servos.set_speed(self.RF, self.npos.RFB)

    def right_back(self):
        self.tilt_left()
        self.servos.set_speed(self.LF, self.npos.LFB)

    def wave(self, delay=0.1):
        self.tilt_right()
        self.servos.move_to_angles(self.LL, 60, step=5, delay=0.02)
        time.sleep(delay)
        self.servos.move_to_angles(self.LL, 20, step=5, delay=0.02)
        time.sleep(delay)
        self.tilt_left()
        self.servos.move_to_angles(self.RL, 120, step=5, delay=0.02)
        time.sleep(delay)
        self.servos.move_to_angles(self.RL, 160, step=5, delay=0.02)
        time.sleep(delay)
        self.return_to_neutral()

    def steps(self, delay=0.1):
        for i in range(2):
            self.servos.move_to_angles(self.LL, 80, self.RL, 170, step=4, delay=0.02)
            time.sleep(delay)
            self.servos.move_to_angles(self.LL, 10, self.RL, 100, step=4, delay=0.02)
            time.sleep(delay)
        self.return_to_neutral()

    def tilt(self, delay=0.1):
        for i in range(2):
            self.servos.move_to_angles(self.LL, 85, self.RL, 140)
            time.sleep(delay)
            self.servos.move_to_angles(self.LL, 40, self.RL, 95)
            time.sleep(delay)
        self.return_to_neutral()

    def weird(self, iterations=3):
        for _ in range(iterations):
            lf_speed = urandom.randint(5, 10) if urandom.randint(0, 1) else urandom.randint(-10, -5)
            rf_speed = urandom.randint(5, 10) if urandom.randint(0, 1) else urandom.randint(-10, -5)
            self.servos.set_speeds(self.LF, lf_speed, self.RF, rf_speed)
            time.sleep(1)
        self.return_to_neutral()

    def arms(self):
        for i in range(3):
            self.servos.move_to_angles(self.LA, 60, self.RA, 60)
            time.sleep(0.1)
            self.servos.move_to_angles(self.LA, 120, self.RA, 120)
            time.sleep(0.1)
        self.return_to_neutral()

    def balerina(self):
        self.tilt_left()
        time.sleep(0.2)
        self.servos.set_speed(self.LF, self.npos.LFF)

        for i in range(3):
            self.servos.move_to_angles(self.RL, 120, step=6, delay=0.02)
            self.servos.move_to_angles(self.RL, 170, step=6, delay=0.02)
        self.return_to_neutral()
        time.sleep(0.2)

        self.tilt_right()
        time.sleep(0.2)
        self.servos.set_speed(self.RF, self.npos.RFB)

        for i in range(3):
            self.servos.move_to_angles(self.LL, 60, step=6, delay=0.02)
            self.servos.move_to_angles(self.LL, 10, step=6, delay=0.02)
        self.return_to_neutral()
        time.sleep(0.2)

    def boogie(self):
        self.left_forward()
        time.sleep(0.3)
        self.return_to_neutral()
        self.right_back()
        time.sleep(0.3)
        self.return_to_neutral()
        self.left_back()
        time.sleep(0.3)
        self.return_to_neutral()
        self.right_forward()
        time.sleep(0.3)
        self.return_to_neutral()

    def spin(self):
        self.ride_position()
        self.servos.set_speed(self.LF, 5)
        self.servos.set_speed(self.RF, 5)
        time.sleep(2)
        self.servos.set_speeds(self.LF, 0, self.RF, 0)
        time.sleep(0.5)
        self.servos.move_to_angles(self.LL, self.npos.LLN, self.RL, self.npos.RLN, step=10, delay=0.02)

    def toes(self):
        self.servos.move_to_angles(self.LL, 80, self.RL, 100)
        time.sleep(0.2)
        self.return_to_neutral()

    def step_right(self):
        for i in range(3):
            self.servos.move_to_angles(self.RL, 100)
            self.return_to_neutral()

    def step_left(self):
        for i in range(3):
            self.servos.move_to_angles(self.LL, 80)
            self.return_to_neutral()

    def circles(self):
        self.ride_position()
        self.servos.set_speeds(self.LF, 3, self.RF, -8)
        time.sleep(2)
        self.servos.set_speeds(self.LF, 7, self.RF, -3)
        time.sleep(2)
        self.servos.set_speeds(self.LF, 0, self.RF, 0)
        time.sleep(0.5)
        self.servos.move_to_angles(self.LL, self.npos.LLN, self.RL, self.npos.RLN, step=10, delay=0.02)
