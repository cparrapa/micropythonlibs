"""
robot_trim_calibration.py

This MicroPython script for ESP32 implements:
- Two continuous-rotation servos (left GPIO14, right GPIO13)
- Speed control by Pot #1 (GPIO32) mapped -100%..+100%
- Trim control by Pot #2 (GPIO33) applied in microseconds (medium = +/-20us)
- Dead-zone enforcement: any pulse between 1400..1600us is forced to 1500us
- Trims saved to Flash (NVS) and loaded on boot
- OLED (SSD1306) debug output (I2C SDA=21, SCL=22)

How it works (brief):
 1) Speed % -> pulse_us (linear map between 500..2500)
 2) trim_us (from pot2) added to pulse_us
 3) If resulting pulse in [1400..1600] -> forced to 1500 (dead zone)
 4) Pulses applied to servos and displayed on OLED + serial

Wiring reminder:
 - Left servo signal -> GPIO14
 - Right servo signal -> GPIO13
 - Pot1 (speed) -> GPIO32 (ADC)
 - Pot2 (trim)  -> GPIO33 (ADC)
 - OLED SDA -> GPIO21, SCL -> GPIO22 (SSD1306 I2C)

"""

from machine import Pin, ADC, PWM, I2C
from time import sleep
import esp32
import ssd1306

# --------------------------- HARDWARE PINS ---------------------------
LEFT_SERVO_PIN  = 14
RIGHT_SERVO_PIN = 13
POT_SPEED_PIN   = 32
POT_TRIM_PIN    = 33

I2C_SDA = 21
I2C_SCL = 22

# --------------------------- SERVO TIMING ---------------------------
MIN_US = 500     # -100% -> 500us
MID_US = 1500    # stop
MAX_US = 2500    # +100% -> 2500us
PERIOD_US = 20000  # 20ms period for 50Hz

# --------------------------- TRIM / RANGES ---------------------------
TRIM_RANGE_US = 20   # medium = +/-20 microseconds

# --------------------------- ADC / PWM SETUP -------------------------
FREQ = 50

left_pwm  = PWM(Pin(LEFT_SERVO_PIN),  freq=FREQ)
right_pwm = PWM(Pin(RIGHT_SERVO_PIN), freq=FREQ)

pot_speed = ADC(Pin(POT_SPEED_PIN))
pot_speed.width(ADC.WIDTH_12BIT)
pot_speed.atten(ADC.ATTN_11DB)

pot_trim = ADC(Pin(POT_TRIM_PIN))
pot_trim.width(ADC.WIDTH_12BIT)
pot_trim.atten(ADC.ATTN_11DB)

# OLED
i2c = I2C(0, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --------------------------- NVS (persist trims) --------------------
try:
    nvs = esp32.NVS("robot")
    loaded = True
except Exception:
    nvs = None
    loaded = False

# Load saved trim (single trim_us value; positive trims shift left pulse up, right down)
try:
    if loaded:
        saved_trim_us = nvs.get_i32("trim_us")
    else:
        raise Exception()
except Exception:
    saved_trim_us = 0

# --------------------------- HELPERS --------------------------------
def map_int(x, in_min, in_max, out_min, out_max):
    # safe integer mapping
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def percent_to_pulse_us(percent):
    """Map -100..100 percent to 500..2500 us linearly with 0% -> MID_US"""
    # clamp
    if percent < -100:
        percent = -100
    if percent > 100:
        percent = 100

    if percent == 0:
        return MID_US
    elif percent > 0:
        # 0..100 -> MID_US..MAX_US
        return int(MID_US + (MAX_US - MID_US) * (percent / 100.0))
    else:
        # -100..0 -> MIN_US..MID_US
        return int(MID_US - (MID_US - MIN_US) * (abs(percent) / 100.0))


def set_servo_pulse(pwm, pulse_us):
    duty = int((pulse_us / PERIOD_US) * 1023)
    pwm.duty(duty)

def save_trim_us(trim_val):
    global nvs
    if not loaded:
        print("NVS not available; cannot save trims")
        return
    try:
        nvs.set_i32("trim_us", int(trim_val))
        nvs.commit()
        print("Saved trim_us =", int(trim_val))
    except Exception as e:
        print("Error saving trim:", e)

# --------------------------- MAIN LOOP -------------------------------

# Invert right wheel if your mechanical mounting needs it (mirror)
RIGHT_INVERT = True

last_left_pulse = MID_US
last_right_pulse = MID_US

print("Starting calibration. Loaded saved_trim_us=", saved_trim_us)

while True:
    # READ POTS
    raw_speed = pot_speed.read()   # 0..4095
    raw_trim  = pot_trim.read()    # 0..4095

    # SPEED -> percent
    speed_percent = map_int(raw_speed, 0, 4095, -100, 100)

    # TRIM -> microseconds (medium)
    trim_us_live = map_int(raw_trim, 0, 4095, -TRIM_RANGE_US, TRIM_RANGE_US)

    # Use saved trim as base + live trim adjustment
    trim_us = saved_trim_us + trim_us_live

    # Convert percent -> base pulse
    base_pulse = percent_to_pulse_us(speed_percent)

    # Apply trim in microseconds BEFORE dead-zone
    left_pulse = base_pulse + trim_us
    right_pulse = base_pulse - trim_us

    # Enforce dead-zone: if pulse falls into [1400..1600], force 1500
    if 1400 <= left_pulse <= 1600:
        left_pulse = MID_US
    if 1400 <= right_pulse <= 1600:
        right_pulse = MID_US

    # Clamp to absolute min/max
    left_pulse = max(MIN_US, min(MAX_US, left_pulse))
    right_pulse = max(MIN_US, min(MAX_US, right_pulse))

    # Apply inversion if needed
    if RIGHT_INVERT:
        # Invert around MID_US: 1500 +/- X becomes 1500 -/+ X
        right_pulse = MID_US - (right_pulse - MID_US)

    # WRITE TO SERVOS
    set_servo_pulse(left_pwm, left_pulse)
    set_servo_pulse(right_pwm, right_pulse)

    last_left_pulse = left_pulse
    last_right_pulse = right_pulse

    # OLED / Serial debug
    oled.fill(0)

    oled.text("Speed:%4d" % speed_percent+"%", 0, 0)
    oled.text("TrimLive:%+3dus" % trim_us_live, 0, 12)
    oled.text("TrimSaved:%+3dus" % saved_trim_us, 0, 24)
    oled.text("L:%4dus" % left_pulse, 0, 36)
    oled.text("R:%4dus" % right_pulse, 64, 36)
    oled.text("P1:%4d P2:%4d" % (raw_speed, raw_trim), 0, 52)
    oled.show()

    print("Speed%:", speed_percent,
          " TrimLive:", trim_us_live,
          " TrimSaved:", saved_trim_us,
          " L_us:", left_pulse,
          " R_us:", right_pulse)

    # Auto-save saved_trim_us when pot_trim is near center and stable
    # pot_trim near center -> raw_trim around 2048
    if 2030 <= raw_trim <= 2060:
        # save current saved_trim_us (user has centered pot to store)
        save_trim_us(saved_trim_us)

    sleep(0.05)
