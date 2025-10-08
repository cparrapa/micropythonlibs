# measure.py — Distance app using ottoneopixel.OttoUltrasonic (single I/O pin)
# Stable + snappy: paced pings, warm-up, quick retry, fast UI
#
# Wiring:
#   Ultrasonic (one-pin) IO -> GPIO16  (change ULTRA_IO_PIN to 17 if your board's "pin 2" maps there)
#   Encoder button          -> GPIO4   (short = force immediate read, long (≥1.5s) = back)
#
# Requires: ottoneopixel.py (fixed version) providing OttoUltrasonic

import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from ottoneopixel import OttoUltrasonic

# ---- Pins ----
ULTRA_IO_PIN  = 17     # try 17 if your header maps the IO to 17 instead
ULTRA_RGB_PIN = 23     # just to satisfy library init for its 6 LEDs (unused here)
BTN_PIN       = 4

# ---- OLED/UI ----
OLED_W, OLED_H = 128, 64
LONG_PRESS_S   = 1.5
PERIOD_MS      = 150   # ping every 150 ms (~6.7 Hz). Many one-wire HC-SR04 clones dislike <100 ms.

def run(shared_i2c=None):
    i2c  = shared_i2c or I2C(0, sda=Pin(19), scl=Pin(18), freq=100000)
    oled = SSD1306_I2C(OLED_W, OLED_H, i2c)

    ultra = OttoUltrasonic(rgb=ULTRA_RGB_PIN, io=ULTRA_IO_PIN)
    btn   = Pin(BTN_PIN, Pin.IN)  # polarity-agnostic

    _splash(oled, "Distance (Otto)")

    # --- button state ---
    btn_idle = btn.value()
    in_press = False
    t0 = 0

    # --- timing & state ---
    now = time.ticks_ms()
    next_t = time.ticks_add(now, PERIOD_MS)
    last_valid_cm = None
    last_ok_ms = None
    consecutive_fail = 0

    # --- warm-up: some one-wire drivers need a couple of pings ---
    for _ in range(2):
        try:
            _ = ultra.readultrasonicRGB(unit=1)
        except:
            pass
        time.sleep_ms(60)

    while True:
        now = time.ticks_ms()

        # ----- button handling -----
        v = btn.value()
        if not in_press:
            if v != btn_idle:
                in_press = True
                t0 = now
        else:
            if v == btn_idle:
                held = time.ticks_diff(now, t0)
                in_press = False
                if held >= int(LONG_PRESS_S * 1000):
                    _goodbye(oled)
                    return
                elif held >= 40:
                    # force an immediate measurement
                    next_t = now

        # ----- paced polling -----
        if time.ticks_diff(now, next_t) >= 0:
            next_t = time.ticks_add(now, PERIOD_MS)

            # quick double-try (some cycles miss the pulse)
            reading = None
            for _ in range(2):
                try:
                    d = ultra.readultrasonicRGB(unit=1)  # cm
                except:
                    d = None
                if d is not None and 1.0 <= d <= 500.0:
                    reading = d
                    break
                time.sleep_ms(20)

            if reading is not None:
                last_valid_cm = reading
                last_ok_ms = now
                consecutive_fail = 0
            else:
                consecutive_fail += 1

            # draw every cycle
            stale_ms = None if last_ok_ms is None else time.ticks_diff(now, last_ok_ms)
            _draw(oled, last_valid_cm, stale_ms, consecutive_fail)

        time.sleep_ms(2)

# ---------- UI ----------
def _draw(oled, cm, stale_ms, fail_count):
    oled.fill(0)
    oled.text("Distance", 28, 0)

    if cm is None:
        oled.text("--.-- cm", 28, 22)
    else:
        s = "{:>5.1f} cm".format(cm)
        oled.text(s, max(0, (OLED_W - len(s)*8)//2), 22)

    # status line: IO pin + freshness (how long since last good read)
    freshness = "--" if stale_ms is None else "{}ms".format(min(9999, max(0, stale_ms)))
    if fail_count >= 3:
        oled.text("IO:{}  stale:{} (!)".format(ULTRA_IO_PIN, freshness), 0, 50)
    else:
        oled.text("IO:{}  stale:{}".format(ULTRA_IO_PIN, freshness), 0, 50)

    oled.show()

def _splash(oled, title):
    oled.fill(0)
    oled.text(title, 10, 16)
    oled.text("IO pin: {}".format(ULTRA_IO_PIN), 8, 34)
    oled.show()
    time.sleep_ms(250)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 8, 26); oled.show()
    time.sleep_ms(200)
