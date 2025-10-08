# flashlight.py — Flashlight using ottoneopixel.OttoUltrasonic RGB (6 LEDs)
# Pins:
#   Ultrasonic RGB data -> GPIO16   (ULTRA_RGB_PIN)
#   Ultrasonic IO (one-wire) -> GPIO17
#   Encoder A=22, B=21, Button=4
# Controls:
#   Rotate = brightness (5..100%), short-press = toggle, long-press = exit (LEDs off)

import time
from machine import Pin
from ssd1306 import SSD1306_I2C
from ottoneopixel import OttoUltrasonic

# ----- Pin config (match your wiring) -----
ULTRA_RGB_PIN = 16   # <— you said RGB is on 16
ULTRA_IO_PIN  = 17   # distance IO (unchanged)
ENC_A_PIN     = 22
ENC_B_PIN     = 21
BTN_PIN       = 4

# ----- UI / behavior -----
OLED_W, OLED_H = 128, 64
LONG_PRESS_S   = 1.5
UI_PERIOD_MS   = 50      # ~20 FPS
DETENT         = 2       # transitions per encoder detent (use 4 if your encoder needs it)
STEP_BRIGHT    = 0.05    # 5% per detent
MIN_BRIGHT     = 0.05

def run(shared_i2c):
    oled = SSD1306_I2C(OLED_W, OLED_H, shared_i2c)

    # OttoUltrasonic drives both the 6 RGB LEDs and the one-wire IO
    ultra = OttoUltrasonic(rgb=ULTRA_RGB_PIN, io=ULTRA_IO_PIN)

    # Inputs
    enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    btn   = Pin(BTN_PIN, Pin.IN)

    _splash(oled, "Flashlight")
    _rgb_selftest(oled, ultra)  # quick visible check that RGB pin is correct

    # State
    brightness = 1.0
    on = True
    ultra.setBrightness(brightness)
    ultra.ultrasonicRGB2(255, 255, 255)

    # Quadrature polling (simple & reliable inside app)
    last_state = (enc_a.value() << 1) | enc_b.value()
    accum = 0

    # Button state
    btn_idle = btn.value()
    in_press = False
    t0 = 0

    next_ui = time.ticks_add(time.ticks_ms(), UI_PERIOD_MS)

    while True:
        now = time.ticks_ms()

        # ----- Encoder (quadrature, polled) -----
        s = (enc_a.value() << 1) | enc_b.value()
        if s != last_state:
            # CW: 00->01->11->10->00 ; CCW: 00->10->11->01->00
            if   (last_state == 0 and s == 1) or (last_state == 1 and s == 3) or (last_state == 3 and s == 2) or (last_state == 2 and s == 0):
                accum += 1
            elif (last_state == 0 and s == 2) or (last_state == 2 and s == 3) or (last_state == 3 and s == 1) or (last_state == 1 and s == 0):
                accum -= 1
            last_state = s

            # apply per-detent steps
            while accum >= DETENT:
                accum -= DETENT
                brightness = min(1.0, brightness + STEP_BRIGHT)
                if on:
                    ultra.setBrightness(brightness)
                    ultra.ultrasonicRGB2(255, 255, 255)
            while accum <= -DETENT:
                accum += DETENT
                brightness = max(MIN_BRIGHT, brightness - STEP_BRIGHT)
                if on:
                    ultra.setBrightness(brightness)
                    ultra.ultrasonicRGB2(255, 255, 255)

        # ----- Button -----
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
                    ultra.clearultrasonicRGB()
                    _goodbye(oled)
                    return
                elif held >= 60:
                    on = not on
                    if on:
                        ultra.setBrightness(brightness)
                        ultra.ultrasonicRGB2(255, 255, 255)
                    else:
                        ultra.clearultrasonicRGB()

        # ----- UI -----
        if time.ticks_diff(now, next_ui) >= 0:
            next_ui = time.ticks_add(now, UI_PERIOD_MS)
            _draw(oled, on, int(brightness * 100))

        time.sleep_ms(2)

# ---------- helpers ----------
def _rgb_selftest(oled, ultra):
    """Flash a quick white pulse so you instantly see if RGB pin is correct."""
    try:
        ultra.setBrightness(1.0)
        ultra.ultrasonicRGB2(255, 255, 255)
        _hint(oled, "RGB pin {} OK".format(ULTRA_RGB_PIN), 180)
        # settle to medium while app starts
        ultra.setBrightness(0.5)
        ultra.ultrasonicRGB2(255, 255, 255)
    except Exception as e:
        _hint(oled, "RGB ERR on pin {}".format(ULTRA_RGB_PIN), 600)
        raise e

def _draw(oled, is_on, pct):
    oled.fill(0)
    # icon (flashlight body + beam bars)
    xc, yc = 64, 30
    oled.fill_rect(xc-8, yc-6, 16, 12, 1)   # head
    oled.fill_rect(xc-4, yc+6, 8, 8, 1)     # handle
    # beam bars proportional to pct
    levels = max(1, pct // 20)  # 1..5
    for i in range(1, 6):
        length = 8 + i*6
        y = yc - 12 + i*5
        if is_on and i <= levels:
            oled.hline(xc+10, y, length, 1)
        else:
            # faint dotted guide when off / below level
            for k in range(0, length, 3):
                oled.pixel(xc+10+k, y, 1 if not is_on else 0)
    # footer
    s = ("ON  {:>3d}%".format(pct)) if is_on else "OFF"
    oled.text(s, max(0, (OLED_W - len(s)*8)//2), 50)
    oled.show()

def _splash(oled, title):
    oled.fill(0); oled.text(title, 24, 18); oled.text("RGB pin: {}".format(ULTRA_RGB_PIN), 10, 34); oled.show()
    time.sleep_ms(220)

def _hint(oled, msg, ms):
    oled.fill(0); oled.text(msg, 4, 28); oled.show(); time.sleep_ms(ms)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 8, 26); oled.show()
    time.sleep_ms(160)
