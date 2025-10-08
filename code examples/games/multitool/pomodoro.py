# pomodoro.py — Pomodoro timer (Work/Break cycles)
# Controls:
#   - Short press (BTN=4): Start/Pause
#   - Rotate (A=22,B=21) while PAUSED: adjust current phase duration (±1 min)
#   - Long press (≥1.5 s): Back to menu
#
# Defaults: 25 min Work, 5 min Break. Auto-switch on zero; counts completed cycles.

import time
from machine import Pin
from ssd1306 import SSD1306_I2C

# Pins
ENC_A_PIN = 22
ENC_B_PIN = 21
BTN_PIN   = 4

# UI
W, H = 128, 64
HEADER_H = 12
DETENT = 2
LONG_PRESS_S = 1.5
UI_PERIOD_MS = 200

WORK_MIN_DEFAULT  = 25
BREAK_MIN_DEFAULT = 5
MIN_MINUTES = 1
MAX_MINUTES = 90

def run(shared_i2c):
    oled = SSD1306_I2C(W, H, shared_i2c)

    enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    btn   = Pin(BTN_PIN, Pin.IN)

    _splash(oled)

    # state
    work_min  = WORK_MIN_DEFAULT
    break_min = BREAK_MIN_DEFAULT
    mode = "WORK"          # "WORK" or "BREAK"
    running = False
    cycles = 0

    # time left in ms
    time_left = work_min * 60 * 1000

    # encoder
    last_state = (enc_a.value() << 1) | enc_b.value()
    accum = 0

    # button
    btn_idle = btn.value(); in_press = False; t0 = 0

    next_ui = time.ticks_add(time.ticks_ms(), UI_PERIOD_MS)
    last_tick = time.ticks_ms()

    while True:
        now = time.ticks_ms()

        # encoder (adjust duration when paused)
        s = (enc_a.value() << 1) | enc_b.value()
        if s != last_state:
            if   (last_state == 0 and s == 1) or (last_state == 1 and s == 3) or (last_state == 3 and s == 2) or (last_state == 2 and s == 0):
                accum += 1
            elif (last_state == 0 and s == 2) or (last_state == 2 and s == 3) or (last_state == 3 and s == 1) or (last_state == 1 and s == 0):
                accum -= 1
            last_state = s

            if not running:
                changed = 0
                while accum >= DETENT: accum -= DETENT; changed += 1
                while accum <= -DETENT: accum += DETENT; changed -= 1
                if changed != 0:
                    if mode == "WORK":
                        work_min = _clamp(work_min + changed, MIN_MINUTES, MAX_MINUTES)
                        time_left = work_min * 60 * 1000
                    else:
                        break_min = _clamp(break_min + changed, MIN_MINUTES, MAX_MINUTES)
                        time_left = break_min * 60 * 1000

        # button (short/long)
        v = btn.value()
        if not in_press:
            if v != btn_idle:
                in_press = True; t0 = now
        else:
            if v == btn_idle:
                held = time.ticks_diff(now, t0); in_press = False
                if held >= int(LONG_PRESS_S*1000):
                    _goodbye(oled); return
                elif held >= 60:
                    running = not running
                    last_tick = now

        # countdown when running
        if running:
            dt = time.ticks_diff(now, last_tick)
            last_tick = now
            if dt > 0:
                time_left -= dt
                if time_left <= 0:
                    # phase switch
                    if mode == "WORK":
                        mode = "BREAK"
                        cycles += 1
                        time_left = break_min * 60 * 1000
                        _flash(oled, "Break!")
                    else:
                        mode = "WORK"
                        time_left = work_min * 60 * 1000
                        _flash(oled, "Work!")

        # draw UI
        if time.ticks_diff(now, next_ui) >= 0:
            next_ui = time.ticks_add(now, UI_PERIOD_MS)
            _draw(oled, mode, running, time_left, work_min, break_min, cycles)

        time.sleep_ms(2)

# ---------- helpers ----------
def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def _fmt_mmss(ms):
    if ms < 0: ms = 0
    sec = ms // 1000
    m = sec // 60
    s = sec % 60
    return "{:02d}:{:02d}".format(m, s)

def _draw(oled, mode, running, time_left, work_min, break_min, cycles):
    oled.fill(0)
    # header
    title = "POMODORO"
    oled.text(title, (W - len(title)*8)//2, 0)
    oled.hline(0, 11, W, 1)

    # mode + durations line
    mode_txt = "WORK" if mode == "WORK" else "BREAK"
    hint = "Press=Start/Pause"
    oled.text("{}  (W{} B{})".format(mode_txt, work_min, break_min), 2, 14)

    # timer big
    t = _fmt_mmss(time_left)
    oled.text(t, (W - len(t)*8)//2, 30)

    # cycles & hint
    oled.text("Cycles: {}".format(cycles), 2, 52)
    oled.text(hint, W - len(hint)*8 - 2, 52)

    # simple progress bar
    total_ms = (work_min if mode == "WORK" else break_min) * 60 * 1000
    if total_ms > 0:
        pct = max(0, min(100, int((total_ms - time_left) * 100 / total_ms)))
        x, y, w, h = 14, 46, 100, 6
        oled.rect(x, y, w, h, 1)
        fillw = (w-2) * pct // 100
        if fillw > 0:
            oled.fill_rect(x+1, y+1, fillw, h-2, 1)

    oled.show()

def _flash(oled, msg):
    # brief inverted banner
    oled.fill(0)
    oled.fill_rect(0, 0, W, H, 1)
    oled.fill_rect(0, 0, W, 16, 0)
    oled.text(msg, (W - len(msg)*8)//2, 4)  # black on white header
    oled.show()
    time.sleep_ms(400)

def _splash(oled):
    oled.fill(0); oled.text("POMODORO", 24, 18); oled.text("Ready", 46, 34); oled.show()
    time.sleep_ms(220)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 10, 26); oled.show()
    time.sleep_ms(160)
