"""
unified_robot_with_wizard.py

Single-file MicroPython robot controller with:
 - Two continuous-rotation servos (LEFT=GPIO14, RIGHT=GPIO13)
 - Speed percent <-> microseconds mapping
 - Trims stored in JSON (microseconds)
 - Dead-zone enforcement (1400..1600 -> 1500)
 - Live potentiometer trimming (two pots) and a save button
 - Automatic calibration wizard:
     * Trim calibration (user-driven visual feedback)
     * Linear speed calibration (drive known distance to compute cm/s)
     * Rotation calibration (turn and measure angle)
 - OLED optional debug display

Pins and behavior by default (adjust at top):
  SPEED_POT = 32        # main speed pot (also used as left trim if you choose)
  TRIM_LEFT_POT = 33    # left trim pot (optional)
  TRIM_RIGHT_POT = None # if None, mirrored trim is used
  SAVE_BUTTON = 26      # button to save trims when held

If you prefer a different mapping of pins, edit the constants below.
"""

import json
from machine import Pin, PWM, ADC, I2C
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
PERIOD_US = 20000
# Inversion
RIGHT_INVERT = True

# Calibration persistence
CALIB_FILE = "robot_calib.json"

# Default trims (microseconds) - will be loaded/saved
LEFT_TRIM_US = 0
RIGHT_TRIM_US = 0

# ---------------- POT and BUTTON PINS (from user)
SPEED_POT_PIN = 32         # main speed pot
TRIM_LEFT_POT_PIN = 33     # left trim pot
TRIM_RIGHT_POT_PIN = None  # if None, use mirrored trim or single-pot mode
SAVE_BUTTON_PIN = 26       # hold to save trims

# ---------------- Robot geometry & motion model (user measure) --------
WHEEL_DIAMETER_CM = 6.5
WHEEL_CIRCUMFERENCE_CM = 3.1416 * WHEEL_DIAMETER_CM
WHEEL_TRACK_CM = 12.0
CM_PER_SECOND_AT_100 = 20.0

# ---------------- Hardware setup -------------------------------------
left_pwm  = PWM(Pin(LEFT_SERVO_PIN), freq=FREQ)
right_pwm = PWM(Pin(RIGHT_SERVO_PIN), freq=FREQ)

# ADCs
pot_speed = ADC(Pin(SPEED_POT_PIN))
pot_speed.width(ADC.WIDTH_12BIT)
pot_speed.atten(ADC.ATTN_11DB)

pot_trim_left = ADC(Pin(TRIM_LEFT_POT_PIN))
pot_trim_left.width(ADC.WIDTH_12BIT)
pot_trim_left.atten(ADC.ATTN_11DB)

pot_trim_right = None
if TRIM_RIGHT_POT_PIN is not None:
    pot_trim_right = ADC(Pin(TRIM_RIGHT_POT_PIN))
    pot_trim_right.width(ADC.WIDTH_12BIT)
    pot_trim_right.atten(ADC.ATTN_11DB)

# Save button
save_button = Pin(SAVE_BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Optional OLED
_oled = None
try:
    import ssd1306
    i2c = I2C(0, scl=Pin(22), sda=Pin(21))
    _oled = ssd1306.SSD1306_I2C(128, 64, i2c)
except Exception:
    _oled = None

# ---------------- Persistence (JSON) ----------------
def load_calibration():
    global LEFT_TRIM_US, RIGHT_TRIM_US, CM_PER_SECOND_AT_100
    try:
        with open(CALIB_FILE, "r") as f:
            data = json.load(f)
            LEFT_TRIM_US  = int(data.get("left_trim_us", 0))
            RIGHT_TRIM_US = int(data.get("right_trim_us", 0))
            CM_PER_SECOND_AT_100 = float(data.get("cm_per_s_100", CM_PER_SECOND_AT_100))
            print("Loaded calibration:", LEFT_TRIM_US, RIGHT_TRIM_US, "cm/s@100=", CM_PER_SECOND_AT_100)
    except Exception:
        print("No calibration file found; using defaults (0,0).")


def save_calibration():
    try:
        with open(CALIB_FILE, "w") as f:
            json.dump({
                "left_trim_us": LEFT_TRIM_US,
                "right_trim_us": RIGHT_TRIM_US,
                "cm_per_s_100": CM_PER_SECOND_AT_100
            }, f)
        print("Saved calibration:", LEFT_TRIM_US, RIGHT_TRIM_US, CM_PER_SECOND_AT_100)
    except Exception as e:
        print("Failed saving calibration:", e)

# load at start
load_calibration()

# ---------------- Helpers: conversions ----------------
def clamp_us(us):
    return max(MIN_US, min(MAX_US, int(us)))


def percent_to_us(percent):
    p = max(-100, min(100, int(percent)))
    if p == 0:
        return MID_US
    if p > 0:
        return int(MID_US + (MAX_US - MID_US) * (p / 100.0))
    else:
        return int(MID_US - (MID_US - MIN_US) * (abs(p) / 100.0))


def us_to_percent(us):
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
    duty = int((pulse_us / PERIOD_US) * 1023)
    pwm.duty(duty)

# ---------------- Core: set_speed + dead-zone + trims ----------------
def set_speed(left_percent, right_percent):
    global LEFT_TRIM_US, RIGHT_TRIM_US
    left_base  = percent_to_us(left_percent)
    right_base = percent_to_us(right_percent)

    # apply trims (microseconds)
    left_pulse  = left_base  + LEFT_TRIM_US
    right_pulse = right_base + RIGHT_TRIM_US

    # enforce dead-zone
    if DZ_MIN <= left_pulse <= DZ_MAX:
        left_pulse = MID_US
    if DZ_MIN <= right_pulse <= DZ_MAX:
        right_pulse = MID_US

    # clamp
    left_pulse  = clamp_us(left_pulse)
    right_pulse = clamp_us(right_pulse)

    # handle inversion
    if RIGHT_INVERT:
        right_pulse = MID_US - (right_pulse - MID_US)

    set_servo_pulse(left_pwm, left_pulse)
    set_servo_pulse(right_pwm, right_pulse)

    return us_to_percent(left_pulse), us_to_percent(right_pulse), left_pulse, right_pulse

# ---------------- High-level movement functions (timed) ----------------
def forward(speed_percent):
    set_speed(abs(speed_percent), abs(speed_percent))


def backward(speed_percent):
    set_speed(-abs(speed_percent), -abs(speed_percent))


def stop():
    set_speed(0, 0)


def turn_left(speed_percent):
    set_speed(-abs(speed_percent), abs(speed_percent))


def turn_right(speed_percent):
    set_speed(abs(speed_percent), -abs(speed_percent))

# ---------------- Distance & rotate helpers (approx. timed) ----------------
def move_distance(distance_cm, speed_percent):
    speed = abs(speed_percent)
    if speed == 0:
        return
    cm_s = CM_PER_SECOND_AT_100 * (speed / 100.0)
    duration = distance_cm / cm_s
    forward(speed)
    sleep(duration)
    stop()


def rotate_angle(angle_deg, speed_percent):
    angle = float(angle_deg)
    arc_cm = 3.1416 * WHEEL_TRACK_CM * abs(angle) / 360.0
    speed = abs(speed_percent)
    if speed == 0:
        return
    cm_s = CM_PER_SECOND_AT_100 * (speed / 100.0)
    duration = arc_cm / cm_s
    if angle > 0:
        set_speed(-speed, speed)
    else:
        set_speed(speed, -speed)
    sleep(duration)
    stop()

# ---------------- Trim API / live pots ----------------
TRIM_EXTERNAL_RANGE_US = 200  # range for live pot mapping (±200us) - adjustable


def read_pots():
    """Read speed pot and trim pots. Returns (speed_percent, trim_left_us, trim_right_us_or_None)"""
    raw_speed = pot_speed.read()  # 0..4095
    speed = int((raw_speed / 4095.0) * 200 - 100)  # -100..100

    raw_tl = pot_trim_left.read()
    trim_left = int((raw_tl / 4095.0) * 2 * TRIM_EXTERNAL_RANGE_US - TRIM_EXTERNAL_RANGE_US)

    trim_right = None
    if pot_trim_right is not None:
        raw_tr = pot_trim_right.read()
        trim_right = int((raw_tr / 4095.0) * 2 * TRIM_EXTERNAL_RANGE_US - TRIM_EXTERNAL_RANGE_US)

    return speed, trim_left, trim_right


def apply_live_trims(use_live=True, persist=False):
    """Read trim pots and apply to current in-memory trims. Optionally persist."""
    global LEFT_TRIM_US, RIGHT_TRIM_US
    speed, tl, tr = read_pots()
    if TRIM_RIGHT_POT_PIN is None:
        # single-pot mirrored mode: left=+x right=-x
        LEFT_TRIM_US = tl
        RIGHT_TRIM_US = -tl
    else:
        LEFT_TRIM_US = tl
        RIGHT_TRIM_US = tr
    if persist:
        save_calibration()

# ---------------- Calibration wizard ----------------
def calibration_wizard():
    """Guided auto calibration. Uses serial prompts for user input.

    Steps:
      1) Trim calibration: drive forward several times and accept user feedback (l/r/ok)
      2) Speed calibration: drive known distance and ask user to input measured distance
      3) Rotation calibration: rotate 90deg nominally and ask user to input measured angle
    """
    global LEFT_TRIM_US, RIGHT_TRIM_US, CM_PER_SECOND_AT_100

    print("=== Calibration wizard ===")
    print("Current trims (us)", LEFT_TRIM_US, RIGHT_TRIM_US)

    # 1) Trim calibration
    print("\nTrim calibration: robot will drive forward for short bursts. Indicate drift with 'l' or 'r' or enter when OK.")
    for i in range(5):
        print("Run", i+1)
        forward(35)
        sleep(1.2)
        stop()
        resp = input("Drift? (l=left, r=right, enter=good): ")
        if resp == 'l':
            LEFT_TRIM_US -= 2
            RIGHT_TRIM_US += 2
            print("Adjusted trims:", LEFT_TRIM_US, RIGHT_TRIM_US)
        elif resp == 'r':
            LEFT_TRIM_US += 2
            RIGHT_TRIM_US -= 2
            print("Adjusted trims:", LEFT_TRIM_US, RIGHT_TRIM_US)
        else:
            print("No change.")

    # 2) Speed calibration
    print("\nSpeed calibration: you must mark a ground distance (e.g., 100 cm).")
    dist = float(input("Enter measured distance in cm to run for test (e.g. 100): "))
    test_speed = int(input("Enter test speed percent (recommended 50): ") or 50)
    print("Starting speed test...")
    forward(test_speed)
    # run for a fixed time (user can stop earlier), we choose 5s test
    sleep(5)
    stop()
    measured = float(input("After the run, enter the actual distance the robot traveled (cm): "))
    if measured > 0:
        # calculate cm/s at this percent
        cm_s = measured / 5.0
        CM_PER_SECOND_AT_100 = cm_s * (100.0 / test_speed)
        print("Calibrated CM_PER_SECOND_AT_100 =", CM_PER_SECOND_AT_100)

    # 3) Rotation calibration
    print("\nRotation calibration: robot will attempt a 90deg turn. Place a marker and measure angle.")
    test_turn_speed = int(input("Enter turn speed percent (recommended 40): ") or 40)
    print("Rotating...")
    turn_right( test_turn_speed )
    sleep(1.0)
    stop()
    measured_angle = float(input("Enter measured rotation degrees (positive): "))
    if measured_angle > 0:
        # compute scale: duration used was 1.0s; compute arc and set a helper constant
        # we will adjust WHEEL_TRACK_CM effectively by scaling rotation durations in rotate_angle
        scale = 90.0 / measured_angle
        print("Rotation scale factor (90/measured):", scale)
        # store scale in calibration file by adjusting WHEEL_TRACK_CM accordingly
        # For simplicity we store a rotation_scale in the file
        try:
            with open(CALIB_FILE, "r") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}
        cfg['rotation_scale'] = scale
        try:
            with open(CALIB_FILE, "w") as f:
                json.dump(cfg, f)
            print("Saved rotation scale to calibration file.")
        except Exception as e:
            print("Failed saving rotation scale:", e)

    # Save trims and speed
    save_calibration()
    print("Calibration wizard finished.")

# ---------------- Live mode: potentiometer + button ----------------
def live_trim_loop(show_oled=True):
    """Continuously apply live trims from pots. Hold SAVE button to persist trims."""
    print("Entering live trim mode. Turn pots to adjust. Hold button to save and exit.")
    try:
        while True:
            speed, tl, tr = read_pots()
            if TRIM_RIGHT_POT_PIN is None:
                LEFT_TRIM_US = tl
                RIGHT_TRIM_US = -tl
            else:
                LEFT_TRIM_US = tl
                RIGHT_TRIM_US = tr

            # optionally apply speed too (preview)
            set_speed(0, 0)
            # display
            if _oled and show_oled:
                try:
                    _oled.fill(0)
                    _oled.text("Ltrim:%+dus" % LEFT_TRIM_US, 0, 0)
                    _oled.text("Rtrim:%+dus" % RIGHT_TRIM_US, 0, 12)
                    _oled.text("PotSpeed:%d" % speed, 0, 24)
                    _oled.show()
                except Exception:
                    pass

            # save if button pressed (active low)
            if not save_button.value():
                print("Save button pressed — saving trims.")
                save_calibration()
                sleep(0.8)  # debounce & allow release
                break

            sleep(0.05)
    except KeyboardInterrupt:
        print("Live trim loop interrupted.")

# ---------------- Simple CLI -------------------------------------
if __name__ == "__main__":
    print("Unified robot controller with wizard")
    print("Commands:\n  calib  - run calibration wizard\n  live   - live pot trim mode\n  f/b/tl/tr/stop\n  move/rot\n  show/save/quit")
    while True:
        cmd = input("cmd> ").strip().lower()
        if cmd in ("q", "quit", "exit"):
            stop()
            break
        if cmd == "calib":
            calibration_wizard()
        elif cmd == "live":
            live_trim_loop()
        elif cmd in ("f", "forward"):
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
        elif cmd in ("show", "showtrims"):
            print("Trims:", LEFT_TRIM_US, RIGHT_TRIM_US)
        elif cmd in ("save",):
            save_calibration()
        else:
            print("Unknown command. type 'calib' or 'live' or 'f' etc.")
