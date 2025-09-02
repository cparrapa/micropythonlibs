from machine import Pin
from time import sleep
from ottoneopixel import OttoNeoPixel, OttoUltrasonic
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
import network, espnow, machine

# ===== Config / tuning =====
DEADZONE = 0.12        # ignore small stick noise
NEUTRAL  = 64          # CR servo neutral in Otto lib
SCALE    = 60          # how much joystick -> speed
TRIM_STEP = 0.5          # L/R change per press

# Optional quick flips if your robot wiring needs it
INVERT_FWD  = True    # set True if forward/back feels reversed
INVERT_TURN = False    # set True if left/right feels reversed

# ===== ESP-NOW =====
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

esp = espnow.ESPNow()
esp.active(True)

# ===== Hardware =====
led_pin = machine.Pin(2, machine.Pin.OUT)
buzzer = OttoBuzzer(25)
motor = OttoMotor(13, 14)             # left, right continuous servos
motor.leftServo.freq(50)
motor.rightServo.freq(50)
ring = OttoNeoPixel(4, 13)
ultrasonic = OttoUltrasonic(18, 19)
ring.fillAllRing(0, 255, 255)
ultrasonic.ultrasonicRGB2(0, 255, 255)

offset = 0   # L/R trim to go straight; L decrements, R increments

def clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def stop_motors():
    motor.leftServo.duty(0)
    motor.rightServo.duty(0)

def set_motors_from_arcade(forward, turn):
    """
    forward, turn in [-1..+1]
    Convert to left/right, apply trim, map to duty.
    """
    # deadzone
    if abs(forward) < DEADZONE: forward = 0
    if abs(turn)    < DEADZONE: turn    = 0

    # if centered, do a hard stop (duty=0) so wheels fully stop
    if forward == 0 and turn == 0:
        stop_motors()
        return

    # mix: arcade drive
    left  = clamp(forward + turn, -1, 1)
    right = clamp(forward - turn, -1, 1)

    # map to servo duty (neutral=64). Add trim: left gets -offset, right +offset
    left_duty  = int(round(NEUTRAL + SCALE * left  - offset))
    right_duty = int(round(NEUTRAL + SCALE * right + offset))

    # clamp valid range (keep 0 available as a "stop" command we send explicitly)
    left_duty  = clamp(left_duty,  1, 127)
    right_duty = clamp(right_duty, 1, 127)

    motor.leftServo.duty(left_duty)
    motor.rightServo.duty(right_duty)

while True:
    _, msg = esp.recv()
    if not msg:
        continue

    # Expect "x;y;A,L" from the sender
    try:
        s = msg.decode()
        parts = s.split(";")
        rx_x = float(parts[0])
        rx_y = float(parts[1])
        buttons = parts[2].split(",") if len(parts) > 2 and parts[2] else []
    except Exception as e:
        print("Bad message:", msg, e)
        continue

    # === Axes mapping (fix) ===
    # Sender: x = left/right, y = forward/back (normalized)
    # Your observation: x moved forward/back, y turned → swap here:
    forward = rx_x
    turn    = rx_y

    if INVERT_FWD:  forward = -forward
    if INVERT_TURN: turn    = -turn

    # === Apply movement ===
    set_motors_from_arcade(forward, turn)

    # === L/R trim for straight driving ===
    if "L" in buttons:
        offset -= TRIM_STEP
        buzzer.playNote(220, 80)
        print("Trim offset:", offset)
    if "R" in buttons:
        offset += TRIM_STEP
        buzzer.playNote(440, 80)
        print("Trim offset:", offset)

    # === A/B/C/D feedback ===
    if "A" in buttons:
        ring.fillAllRing(255, 255, 0);   buzzer.playNote(261, 100)
    elif "B" in buttons:
        ring.fillAllRing(0, 0, 255);   buzzer.playNote(293, 100)
    elif "C" in buttons:
        ring.fillAllRing(255, 0, 0);   buzzer.playNote(329, 100)
    elif "D" in buttons:
        ring.fillAllRing(0, 255, 0); buzzer.playNote(349, 100)
    else:
        ring.fillAllRing(0, 0, 0)

    sleep(0.04)
