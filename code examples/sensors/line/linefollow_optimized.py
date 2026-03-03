import time
from machine import Pin, ADC
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor
 
analogL = ADC(Pin(32))
analogR = ADC(Pin(33))
ultrasonic = OttoUltrasonic(18, 19)
motor = OttoMotor(13, 14)
 
def clamp(x, lo, hi):
    if x < lo: return lo
    if x > hi: return hi
    return x
 
# ---- Calibrate these so wheels STOP (critical) ----
L_STOP = 75
R_STOP = 75
 
# Your robot: left forward was higher duty, right forward was lower duty
L_DIR = +1
R_DIR = -1
 
# ---- Speed / authority ----
BASE_SPEED = 0.55      # higher = faster
SPAN = 30              # higher = more motor authority (was 20)
 
# ---- Control ----
KP = 1.2               # gain for NORMALIZED error (NOT raw ADC difference)
KD = 0.0               # start at 0; add later only if needed
 
MAX_STEER = 0.40       # max steering effort (0..1)
DEADBAND = 0.03        # ignore tiny error (reduces jitter)
STEER_SLEW = 0.08      # max change in steer per loop (rate limit)
 
# ---- Filtering / loop ----
ALPHA = 0.35
DT_MS = 15
 
# State
fL = analogL.read()
fR = analogR.read()
prev_err = 0.0
prev_steer = 0.0
 
def set_wheel_speeds(left_speed, right_speed):
    # Forward-only while tuning
    left_speed  = clamp(left_speed,  0.0, 1.0)
    right_speed = clamp(right_speed, 0.0, 1.0)
 
    left_duty  = int(L_STOP + L_DIR * (left_speed  * SPAN))
    right_duty = int(R_STOP + R_DIR * (right_speed * SPAN))
 
    motor.leftServo.duty(clamp(left_duty,  40, 110))
    motor.rightServo.duty(clamp(right_duty, 40, 110))
 
while True:
    t0 = time.ticks_ms()
 
    # Read once
    rawL = analogL.read()
    rawR = analogR.read()
 
    # Smooth sensors
    fL = (1 - ALPHA) * fL + ALPHA * rawL
    fR = (1 - ALPHA) * fR + ALPHA * rawR
 
    # Normalized error in roughly [-1, +1]
    denom = (fL + fR)
    if denom < 1:
        denom = 1
    err = (fL - fR) / denom
 
    # Deadband to suppress jitter on straight
    if -DEADBAND < err < DEADBAND:
        err = 0.0
 
    # Optional: if it steers away from the line, flip sign:
    # err = -err
 
    # PD (D off initially)
    derr = err - prev_err
    prev_err = err
    steer = KP * err + KD * derr
 
    # Clamp steering
    steer = clamp(steer, -MAX_STEER, MAX_STEER)
 
    # Slew-rate limit steering to avoid rapid left-right flips
    steer = clamp(steer, prev_steer - STEER_SLEW, prev_steer + STEER_SLEW)
    prev_steer = steer
 
    # Mix into wheel speeds
    left_speed  = BASE_SPEED - steer
    right_speed = BASE_SPEED + steer
 
    set_wheel_speeds(left_speed, right_speed)
 
    # Fixed loop period
    elapsed = time.ticks_diff(time.ticks_ms(), t0)
    if elapsed < DT_MS:
        time.sleep_ms(DT_MS - elapsed)