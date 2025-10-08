# stopwatch.py — Simple stopwatch
# Controls:
#   - Short press (BTN GPIO4): Start / Pause
#   - Rotate encoder (A=22, B=21): Reset to 00:00.00 when PAUSED
#   - Long press (≥1.5 s): Back to menu
#
# Display updates ~20 FPS for smooth tenths/hundredths.

import time
from machine import Pin
from ssd1306 import SSD1306_I2C

# Pins (match main)
ENC_A_PIN = 22
ENC_B_PIN = 21
BTN_PIN   = 4

OLED_W, OLED_H = 128, 64
UI_PERIOD_MS   = 50    # ~20 FPS
LONG_PRESS_S   = 1.5
DETENT         = 2     # transitions per detent (set 4 if yours needs it)

def run(shared_i2c):
    oled = SSD1306_I2C(OLED_W, OLED_H, shared_i2c)

    # Inputs (polled quadrature inside the app)
    enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    btn   = Pin(BTN_PIN, Pin.IN)

    _splash(oled)

    running = False
    base_ms = 0          # accumulated time while paused
    start_ms = 0         # when running: ticks at start of current segment

    # encoder state
    last_state = (enc_a.value() << 1) | enc_b.value()
    accum = 0

    # button state
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

            # Reset only when paused
            if not running:
                changed = False
                while accum >= DETENT: accum -= DETENT; changed = True
                while accum <= -DETENT: accum += DETENT; changed = True
                if changed:
                    base_ms = 0
                    start_ms = now
                    _draw(oled, 0)

        # ----- Button (short/long) -----
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
                elif held >= 60:
                    # toggle run/pause
                    if running:
                        # pause: add elapsed since start
                        base_ms = (base_ms + time.ticks_diff(now, start_ms)) & 0x7fffffff
                        running = False
                    else:
                        # start
                        start_ms = now
                        running = True

        # ----- UI update -----
        if time.ticks_diff(now, next_ui) >= 0:
            next_ui = time.ticks_add(now, UI_PERIOD_MS)
            elapsed = base_ms
            if running:
                elapsed = (base_ms + time.ticks_diff(now, start_ms)) & 0x7fffffff
            _draw(oled, elapsed)

        time.sleep_ms(2)

# --------- UI helpers ---------
def _draw(oled, elapsed_ms):
    oled.fill(0)
    oled.text("STOPWATCH", 18, 0)

    # format mm:ss.hh (hundredths)
    total = max(0, int(elapsed_ms))
    minutes = total // 60000
    seconds = (total % 60000) // 1000
    hundred = (total % 1000) // 10
    s = "{:02d}:{:02d}.{:02d}".format(minutes, seconds, hundred)

    # center big time
    x = (OLED_W - len(s)*8)//2
    oled.text(s, x, 26)

    # hint line
    oled.text("press=start/pause", 2, 50)
    oled.show()

def _splash(oled):
    oled.fill(0); oled.text("STOPWATCH", 18, 18); oled.text("Ready", 46, 36); oled.show()
    time.sleep_ms(220)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 10, 26); oled.show()
    time.sleep_ms(160)
