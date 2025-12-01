from machine import Pin, ADC, PWM, I2C
from time import sleep
import ssd1306
import esp32, sys

# -------------------------------------------------
#                CONFIG
# -------------------------------------------------
LEFT_SERVO_PIN  = 14
RIGHT_SERVO_PIN = 13

FREQ = 50
MIN_US = 500
MID_US = 1500
MAX_US = 2500

# Potentiometers
POT_SPEED_PIN = 32
POT_TRIM_PIN  = 33

# Trim max range
TRIM_MAX = 25     # adjust if needed

# -------------------------------------------------
#                LOAD TRIMS FROM FLASH
# -------------------------------------------------
try:
    nvs = esp32.NVS("robot")
    LEFT_TRIM  = nvs.get_i32("ltrim")
    RIGHT_TRIM = nvs.get_i32("rtrim")
    print("Loaded trims L:%d  R:%d" % (LEFT_TRIM, RIGHT_TRIM))
except Exception:
    print("No saved trims, using defaults.")
    LEFT_TRIM  = 0
    RIGHT_TRIM = 0

# -------------------------------------------------
#                 SETUP HARDWARE
# -------------------------------------------------
left_pwm  = PWM(Pin(LEFT_SERVO_PIN),  freq=FREQ)
right_pwm = PWM(Pin(RIGHT_SERVO_PIN), freq=FREQ)

pot_speed = ADC(Pin(POT_SPEED_PIN))
pot_speed.width(ADC.WIDTH_12BIT)
pot_speed.atten(ADC.ATTN_11DB)

pot_trim = ADC(Pin(POT_TRIM_PIN))
pot_trim.width(ADC.WIDTH_12BIT)
pot_trim.atten(ADC.ATTN_11DB)

# ---------------- I2C OLED ---------------------------
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# -------------------------------------------------
#                 HELPER FUNCTIONS
# -------------------------------------------------
def servo_pulse_to_duty(us):
    return int((us / 20000) * 1023)

def drive_servo(pwm, percent, invert=False):
    percent = max(-100, min(100, percent))

    if invert:
        percent = -percent

    if percent == 0:
        us = MID_US
    elif percent > 0:
        us = MID_US + (MAX_US - MID_US) * (percent / 100)
    else:
        us = MID_US - (MID_US - MIN_US) * (abs(percent) / 100)

    pwm.duty(servo_pulse_to_duty(us))
    return us

def map_range(x, a, b, c, d):
    return (x - a) * (d - c) // (b - a) + c

def save_trims():
    try:
        nvs.set_i32("ltrim", LEFT_TRIM)
        nvs.set_i32("rtrim", RIGHT_TRIM)
        nvs.commit()
        print("Trims saved!")
    except Exception as e:
        print("Error saving trims:", e)


# -------------------------------------------------
#            MAIN CONTROL LOOP
# -------------------------------------------------
while True:

    # --- SPEED FROM POT 1 ---
    raw_speed = pot_speed.read()       # 0–4095
    speed = map_range(raw_speed, 0, 4095, -100, 100)

    # --- TRIM FROM POT 2 ---
    raw_trim = pot_trim.read()         # 0–4095
    trim = map_range(raw_trim, 0, 4095, -TRIM_MAX, TRIM_MAX)

    # Live trim adjustment
    # Left wheel gets negative trim when pot rotates left
    LEFT_TRIM  = trim
    RIGHT_TRIM = -trim

    # --- Apply speeds including trims ---
    left_cmd  = speed + LEFT_TRIM
    right_cmd = speed + RIGHT_TRIM

    pulse_l = drive_servo(left_pwm,  left_cmd,  invert=False)
    pulse_r = drive_servo(right_pwm, right_cmd, invert=True)

    # --- Debug output ---
    print("--------------------------------")
    print("Speed: %3d%%" % speed)
    print("Trim:  L:%3d  R:%3d" % (LEFT_TRIM, RIGHT_TRIM))
    print("Out:   L:%3d%% R:%3d%%" % (left_cmd, right_cmd))
    oled.fill(0)
    oled.text("L:%3d%%" % (left_cmd),  0,  0)
    oled.text("R:%3d%%" % (right_cmd), 0, 12)
    oled.text("Trim L:%d R:%d" % (LEFT_TRIM, RIGHT_TRIM), 0, 26)
    oled.show()
    
    # --- Save when trim potentiometer is near center ---
    if -3 < trim < 3:   # small dead zone
        save_trims()

    sleep(0.1)

