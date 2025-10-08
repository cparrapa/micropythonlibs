# dice.py — Visual Dice Roller (d6) with animation
# Controls:
#   - Rotate (A=22, B=21): change number of dice (1..10)
#   - Short press (BTN=4): roll with ~600ms animation
#   - Long press (≥1.5 s): back to menu
#
# Shows up to 6 dice at once (3×2 grid). If more, displays “+N more”.
# Sum is shown at the bottom.

import time
import urandom
from machine import Pin
from ssd1306 import SSD1306_I2C

# Pins
ENC_A_PIN = 22
ENC_B_PIN = 21
BTN_PIN   = 4

# UI
W, H = 128, 64
HEADER_Y = 0
GRID_Y0  = 12          # dice grid starts here
ROW_H    = 22
COL_W    = 40
GRID_COLS = 3
GRID_ROWS = 2
PER_PAGE  = GRID_COLS * GRID_ROWS
FOOTER_Y  = 54

DETENT = 2
LONG_PRESS_S = 1.5
MIN_DICE = 1
MAX_DICE = 10

def run(shared_i2c):
    oled = SSD1306_I2C(W, H, shared_i2c)

    enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    btn   = Pin(BTN_PIN, Pin.IN)

    _splash(oled)

    # state
    count = 2
    results = [1, 2]
    total = sum(results)

    # encoder
    last_state = (enc_a.value() << 1) | enc_b.value()
    accum = 0

    # button
    btn_idle = btn.value(); in_press = False; t0 = 0

    # first draw
    _draw(oled, count, results, total)

    while True:
        now = time.ticks_ms()

        # encoder changes count
        s = (enc_a.value() << 1) | enc_b.value()
        if s != last_state:
            if   (last_state == 0 and s == 1) or (last_state == 1 and s == 3) or (last_state == 3 and s == 2) or (last_state == 2 and s == 0):
                accum += 1
            elif (last_state == 0 and s == 2) or (last_state == 2 and s == 3) or (last_state == 3 and s == 1) or (last_state == 1 and s == 0):
                accum -= 1
            last_state = s

            changed = False
            while accum >= DETENT:
                accum -= DETENT
                if count < MAX_DICE: count += 1; changed = True
            while accum <= -DETENT:
                accum += DETENT
                if count > MIN_DICE: count -= 1; changed = True
            if changed:
                # keep previous results but only show subset; sum updates on next roll
                _draw(oled, count, results, sum(results) if results else 0)

        # button (short/long)
        v = btn.value()
        if not in_press:
            if v != btn_idle:
                in_press = True; t0 = now
        else:
            if v == btn_idle:
                held = time.ticks_diff(now, t0); in_press = False
                if held >= int(LONG_PRESS_S*1000):
                    _bye(oled); return
                elif held >= 60:
                    # roll animation then settle
                    results, total = _roll_animated(oled, count)

        time.sleep_ms(2)

# ---------- visuals ----------
def _draw_header(oled, count):
    oled.fill_rect(0, 0, W, 12, 0)
    title = "DICE {:>2d}x d6".format(count)
    x = (W - len(title)*8)//2
    if x < 0: x = 0
    oled.text(title, x, HEADER_Y)

def _draw(oled, count, results, total):
    oled.fill(0)
    _draw_header(oled, count)

    # draw dice grid
    show = min(count, PER_PAGE)
    for i in range(show):
        val = results[i] if i < len(results) else 1
        row = i // GRID_COLS
        col = i % GRID_COLS
        x = 6 + col * COL_W
        y = GRID_Y0 + row * ROW_H
        _draw_die(oled, x, y, 20, val)

    # overflow tag
    if count > PER_PAGE:
        more = count - PER_PAGE
        msg = "+{} more".format(more)
        oled.text(msg, W - len(msg)*8 - 2, GRID_Y0 + ROW_H*2 - 10)

    # footer
    oled.text("Sum: {:>3d}".format(total), 2, FOOTER_Y)
    oled.text("Press=roll  Hold=back", 2, FOOTER_Y-10)
    oled.show()

def _draw_die(oled, x, y, s, value):
    # body (white)
    oled.fill_rect(x, y, s, s, 1)
    oled.rect(x, y, s, s, 1)
    # pips (black holes)
    def pip(px, py):
        oled.fill_rect(px-1, py-1, 3, 3, 0)
    # positions
    L = x + s//4
    C = x + s//2
    R = x + (3*s)//4
    T = y + s//4
    M = y + s//2
    B = y + (3*s)//4
    # faces
    if value == 1:
        pip(C, M)
    elif value == 2:
        pip(L, T); pip(R, B)
    elif value == 3:
        pip(L, T); pip(C, M); pip(R, B)
    elif value == 4:
        pip(L, T); pip(R, T); pip(L, B); pip(R, B)
    elif value == 5:
        pip(L, T); pip(R, T); pip(C, M); pip(L, B); pip(R, B)
    elif value == 6:
        pip(L, T); pip(L, M); pip(L, B); pip(R, T); pip(R, M); pip(R, B)

def _roll_once(n):
    return [(urandom.getrandbits(16) % 6) + 1 for _ in range(n)]

def _roll_animated(oled, count):
    t0 = time.ticks_ms()
    duration = 600  # ms
    frame = 0
    results = _roll_once(count)
    while time.ticks_diff(time.ticks_ms(), t0) < duration:
        # jitter the displayed values rapidly
        results = _roll_once(count)
        _draw(oled, count, results, sum(results))
        # faster at start, slower at end (ease-out)
        frame += 1
        delay = 20 + min(80, frame * 6)
        time.sleep_ms(delay)
    # final settle
    results = _roll_once(count)
    total = sum(results)
    _draw(oled, count, results, total)
    return results, total

def _splash(oled):
    oled.fill(0); oled.text("DICE ROLLER", 10, 18); oled.text("Rotate=Count", 10, 34); oled.show()
    time.sleep_ms(200)

def _bye(oled):
    oled.fill(0); oled.text("Back to menu", 10, 26); oled.show()
    time.sleep_ms(160)
