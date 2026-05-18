# unified_robot.py
# Single-file robot control + calibration (MicroPython, ESP32)
# - Trims are microseconds, saved to JSON
# - Percent ↔ microseconds mapping exposed to user
# - Dead-zone enforced (1400..1600 -> 1500)
# - High-level movement helpers included

import json
from machine import Pin, PWM
from time import sleep, ticks_ms, ticks_diff

# ---------------- CONFIG Robot in micropython -------------------------
# Pins
LEFT_SERVO_PIN  = 14
RIGHT_SERVO_PIN = 13

FREQ = 50             # 50 Hz = standard servo frequency

# Servo timing (µs)
MIN_US = 400          # pulse for -100% (full reverse)
MID_US = 1500         # pulse for 0% (stop)
# Dead zone
DZ_MIN = 1400
DZ_MAX = 1600
MAX_US = 2600         # pulse for +100% (full forward)
PERIOD_US = 20000     # 20ms period (50Hz)

# Inversion
RIGHT_INVERT = True

# Calibration persistence
CALIB_FILE = "robot_calib.json"

# Default trims (microseconds) - these will be loaded/saved to JSON
LEFT_TRIM_US = 0
RIGHT_TRIM_US = 0

# Robot geometry & motion model (user should measure these)
WHEEL_DIAMETER_CM = 6.5               # wheel diameter in cm
WHEEL_CIRCUMFERENCE_CM = 3.1416 * WHEEL_DIAMETER_CM
WHEEL_TRACK_CM = 12.0                 # distance between wheels center-to-center (approx)
# Speed model estimated; measure for accuracy
CM_PER_SECOND_AT_100 = 20.0           # robot linear speed (cm/s) at 100% (approx)

# ---------------- Hardware setup ----------------
left_pwm  = PWM(Pin(LEFT_SERVO_PIN), freq=FREQ)
right_pwm = PWM(Pin(RIGHT_SERVO_PIN), freq=FREQ)

# Try to enable optional OLED if available (safe - will not crash if lib missing)
_oled = None
try:
    import ssd1306
    from machine import I2C, Pin as _Pin
    i2c = I2C(0, scl=_Pin(22), sda=_Pin(21))
    _oled = ssd1306.SSD1306_I2C(128, 64, i2c)
except Exception:
    _oled = None

# ---------------- Persistence (JSON) ----------------
def load_calibration():
    global LEFT_TRIM_US, RIGHT_TRIM_US
    try:
        with open(CALIB_FILE, "r") as f:
            data = json.load(f)
            LEFT_TRIM_US  = int(data.get("left_trim_us", 0))
            RIGHT_TRIM_US = int(data.get("right_trim_us", 0))
            # clamp trims to reasonable range
            LEFT_TRIM_US  = max(-200, min(200, LEFT_TRIM_US))
            RIGHT_TRIM_US = max(-200, min(200, RIGHT_TRIM_US))
            print("Loaded calibration:", LEFT_TRIM_US, RIGHT_TRIM_US)
    except Exception:
        print("No calibration file found; using defaults (0,0).")
        LEFT_TRIM_US = 0
        RIGHT_TRIM_US = 0

def save_calibration():
    try:
        with open(CALIB_FILE, "w") as f:
            json.dump({"left_trim_us": LEFT_TRIM_US, "right_trim_us": RIGHT_TRIM_US}, f)
        print("Saved calibration:", LEFT_TRIM_US, RIGHT_TRIM_US)
    except Exception as e:
        print("Failed saving calibration:", e)

# Load initial calibration on import
load_calibration()

# ---------------- Helpers: conversions ----------------
def clamp_us(us):
    return max(MIN_US, min(MAX_US, int(us)))

def percent_to_us(percent):
    """Map -100..0..+100 to MIN_US..MID_US..MAX_US linearly.
       percent: -100..100
       Returns integer microseconds.
    """
    p = max(-100, min(100, int(percent)))
    if p == 0:
        return MID_US
    if p > 0:
        return int(MID_US + (MAX_US - MID_US) * (p / 100.0))
    else:
        return int(MID_US - (MID_US - MIN_US) * (abs(p) / 100.0))

def us_to_percent(us):
    """Inverse mapping: given a pulse_us, return percent -100..100 (float).
       If us in dead-zone, returns 0.0.
    """
    u = int(us)
    if DZ_MIN <= u <= DZ_MAX:
        return 0.0
    if u >= MID_US:
        denom = (MAX_US - MID_US)
        if denom == 0:
            return 0.0
        return (u - MID_US) / denom * 100.0
    else:
        denom = (MID_US - MIN_US)
        if denom == 0:
            return 0.0
        return - (MID_US - u) / denom * 100.0

def set_servo_pulse(pwm, pulse_us):
    duty = int((pulse_us / PERIOD_US) * 1023)  # 10-bit duty
    pwm.duty(duty)

# ---------------- Core: set_speed + dead-zone + trims ----------------
def set_speed(left_percent, right_percent):
    """Apply percent commands to both motors, applying trims (µs), dead-zone and inversion.
       left_percent/right_percent in -100..100
    """
    # percent -> base pulse
    left_base  = percent_to_us(left_percent)
    right_base = percent_to_us(right_percent)

    # apply trims (microseconds)
    left_pulse  = left_base  + LEFT_TRIM_US
    right_pulse = right_base + RIGHT_TRIM_US

    # enforce dead-zone: if final pulse is inside DZ, force MID_US
    if DZ_MIN <= left_pulse <= DZ_MAX:
        left_pulse = MID_US
    if DZ_MIN <= right_pulse <= DZ_MAX:
        right_pulse = MID_US

    # clamp to absolute min/max
    left_pulse  = clamp_us(left_pulse)
    right_pulse = clamp_us(right_pulse)

    # handle right inversion (mirror around MID_US)
    if RIGHT_INVERT:
        # invert direction by mirroring the pulse about MID_US:
        # distance from MID is flipped
        right_pulse = MID_US - (right_pulse - MID_US)

    # apply to PWMs
    set_servo_pulse(left_pwm, left_pulse)
    set_servo_pulse(right_pwm, right_pulse)

    # return actual percent values for display/logging
    return us_to_percent(left_pulse), us_to_percent(right_pulse), left_pulse, right_pulse

# ---------------- High-level movement functions (timed) ----------------
def forward(speed_percent):
    set_speed(abs(speed_percent), abs(speed_percent))

def backward(speed_percent):
    set_speed(-abs(speed_percent), -abs(speed_percent))

def stop():
    set_speed(0, 0)

def turn_left(speed_percent):
    # left wheel backward, right wheel forward
    set_speed(-abs(speed_percent), abs(speed_percent))

def turn_right(speed_percent):
    set_speed(abs(speed_percent), -abs(speed_percent))

# ---------------- Distance & rotate helpers (approx. timed) ----------------
def move_distance(distance_cm, speed_percent):
    """Move forward for approximately distance_cm at speed_percent.
       Uses CM_PER_SECOND_AT_100 scale - must be measured for accuracy.
    """
    speed = abs(speed_percent)
    if speed == 0:
        return
    cm_s = CM_PER_SECOND_AT_100 * (speed / 100.0)
    duration = distance_cm / cm_s
    forward(speed)
    sleep(duration)
    stop()

def rotate_angle(angle_deg, speed_percent):
    """Rotate in place by angle_deg (positive = clockwise/right turn).
       We approximate wheel travel: arc = (pi * track * angle/360)
       For in-place rotation, left wheel backward, right wheel forward for positive angle.
       Duration computed from linear speed model; measure TURN_TIME_90 for better accuracy.
    """
    angle = float(angle_deg)
    # wheel arc length per wheel
    arc_cm = 3.1416 * WHEEL_TRACK_CM * abs(angle) / 360.0
    # using speed_percent -> cm/s model (approx)
    speed = abs(speed_percent)
    if speed == 0:
        return
    cm_s = CM_PER_SECOND_AT_100 * (speed / 100.0)
    duration = arc_cm / cm_s
    if angle > 0:
        # clockwise: left backward, right forward
        set_speed(-speed, speed)
    else:
        set_speed(speed, -speed)
    sleep(duration)
    stop()

# ---------------- Trim API ----------------
def set_trims(left_us=None, right_us=None, persist=True):
    """Set left/right trims (microseconds). If None, keep existing.
       persist=True will save to JSON file.
    """
    global LEFT_TRIM_US, RIGHT_TRIM_US
    if left_us is not None:
        LEFT_TRIM_US = int(left_us)
    if right_us is not None:
        RIGHT_TRIM_US = int(right_us)
    # clamp to reasonable values
    LEFT_TRIM_US  = max(-500, min(500, LEFT_TRIM_US))
    RIGHT_TRIM_US = max(-500, min(500, RIGHT_TRIM_US))
    if persist:
        save_calibration()
    return LEFT_TRIM_US, RIGHT_TRIM_US

def get_trims():
    return LEFT_TRIM_US, RIGHT_TRIM_US

# ---------------- Debug helpers ----------------
def debug_status(show_oled=True):
    # show current effective pulses and percents for both motors (0% is MID_US)
    left_p = percent_to_us(0) + LEFT_TRIM_US
    right_p = percent_to_us(0) + RIGHT_TRIM_US
    # enforce dead-zone logic for display (what the motors see)
    lp = MID_US if DZ_MIN <= left_p <= DZ_MAX else clamp_us(left_p)
    rp = MID_US if DZ_MIN <= right_p <= DZ_MAX else clamp_us(right_p)
    # apply inversion for reporting right percent/pulse as actual output
    rp_report = MID_US - (rp - MID_US) if RIGHT_INVERT else rp

    left_pct = round(us_to_percent(lp), 1)
    right_pct = round(us_to_percent(rp_report), 1)

    s = "L_pulse:{}us L_pct:{}  |  R_pulse:{}us R_pct:{}".format(lp, left_pct, rp_report, right_pct)
    print(s)

    if _oled and show_oled:
        try:
            _oled.fill(0)
            _oled.text("L:%dus %:+.1f" % (lp, left_pct), 0, 0)
            _oled.text("R:%dus %:+.1f" % (rp_report, right_pct), 0, 12)
            _oled.text("Trim L:%+dus" % LEFT_TRIM_US, 0, 28)
            _oled.text("Trim R:%+dus" % RIGHT_TRIM_US, 0, 40)
            _oled.show()
        except Exception:
            pass

# ---------------- Example usage / simple menu ----------------
if __name__ == "__main__":
    print("Unified robot controller ready.")
    debug_status()
    print("Commands: f/b/tl/tr/stop/move/rot/settrim/showtrims/save/quit")
    while True:
        cmd = input("cmd> ").strip().lower()
        if cmd in ("q", "quit", "exit"):
            stop()
            break
        if cmd in ("f", "forward"):
            v = int(input("speed% (0-100): "))
            forward(v)
        elif cmd in ("b", "back", "backward"):
            v = int(input("speed% (0-100): "))
            backward(v)
        elif cmd in ("tl", "turn_left"):
            v = int(input("speed% (0-100): "))
            turn_left(v)
        elif cmd in ("tr", "turn_right"):
            v = int(input("speed% (0-100): "))
            turn_right(v)
        elif cmd in ("stop",):
            stop()
        elif cmd in ("move", "move_distance"):
            d = float(input("cm: "))
            v = int(input("speed%: "))
            move_distance(d, v)
        elif cmd in ("rot", "rotate"):
            a = float(input("angle deg (+ clockwise): "))
            v = int(input("speed%: "))
            rotate_angle(a, v)
        elif cmd in ("settrim",):
            l = input("left trim µs (blank to keep): ")
            r = input("right trim µs (blank to keep): ")
            lval = None if l.strip()=="" else int(l)
            rval = None if r.strip()=="" else int(r)
            set_trims(lval, rval, persist=False)
            print("Trims set (in-memory). Call 'save' to persist.")
        elif cmd in ("save", "persist"):
            save_calibration()
        elif cmd in ("showtrims", "trims"):
            print("Trims:", get_trims())
        elif cmd in ("debug",):
            debug_status()
        else:
            print("Unknown cmd.")
