# calculator.py — Encoder-only calculator (basic ops)
# Controls:
#   - Rotate encoder: move selection in 4x5 key grid
#   - Short press (BTN): "tap" selected key
#   - Long press (≥1.5 s): exit back to menu
#
# Keys: 0-9, ., +, −, ×, ÷, =, C (clear), DEL (backspace), ± (sign)
# Behavior: pending-operator style, repeated '=' repeats last operation

import time, math
from machine import Pin
from ssd1306 import SSD1306_I2C

# Pins (match your wiring)
ENC_A_PIN = 22
ENC_B_PIN = 21
BTN_PIN   = 4

# OLED
W, H = 128, 64

# UI layout
TOP_H = 20              # display area height
GRID_Y0 = TOP_H + 1
COLS, ROWS = 4, 5
CELL_W = 30
CELL_H = 8              # 5 rows * 8 = 40px, fits 64 - TOP_H
GRID_X0 = (W - (COLS * CELL_W)) // 2  # center horizontally

DETENT = 2
LONG_PRESS_S = 1.5

# Grid labels (20 keys)
KEYS = [
    "C",  "DEL", "+/-",  "/",
    "7",  "8",   "9",  "*",
    "4",  "5",   "6",  "-",
    "1",  "2",   "3",  "+",
    "0",  ".",   "=",  " "
]

def run(shared_i2c):
    oled = SSD1306_I2C(W, H, shared_i2c)

    # Inputs
    enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    btn   = Pin(BTN_PIN, Pin.IN)

    # Encoder state (polled quadrature)
    last_state = (enc_a.value() << 1) | enc_b.value()
    accum = 0
    sel = 0  # index in KEYS (0..19)

    # Button state
    btn_idle = btn.value(); in_press = False; t0 = 0

    # Calculator state
    entry = "0"       # string being edited
    acc = 0.0         # accumulator
    op = None         # '+', '-', '*', '/'
    last_rhs = None   # for repeated '='
    just_evaluated = False
    error_flash_ms = 0

    _draw(oled, entry, acc, op, sel, just_evaluated, error_flash_ms)

    while True:
        now = time.ticks_ms()

        # ----- Encoder navigation -----
        s = (enc_a.value() << 1) | enc_b.value()
        if s != last_state:
            if   (last_state == 0 and s == 1) or (last_state == 1 and s == 3) or (last_state == 3 and s == 2) or (last_state == 2 and s == 0):
                accum += 1
            elif (last_state == 0 and s == 2) or (last_state == 2 and s == 3) or (last_state == 3 and s == 1) or (last_state == 1 and s == 0):
                accum -= 1
            last_state = s

            moved = 0
            while accum >= DETENT: accum -= DETENT; moved += 1
            while accum <= -DETENT: accum += DETENT; moved -= 1
            if moved:
                # linear wrap across 20 keys
                sel = (sel + moved) % len(KEYS)
                _draw(oled, entry, acc, op, sel, just_evaluated, error_flash_ms)

        # ----- Button handling -----
        v = btn.value()
        if not in_press:
            if v != btn_idle:
                in_press = True; t0 = now
        else:
            if v == btn_idle:
                held = time.ticks_diff(now, t0); in_press = False
                if held >= int(LONG_PRESS_S*1000):
                    _goodbye(oled); return
                elif held >= 50:
                    key = KEYS[sel]
                    entry, acc, op, last_rhs, just_evaluated, error_flash_ms = _tap_key(
                        key, entry, acc, op, last_rhs, just_evaluated)
                    _draw(oled, entry, acc, op, sel, just_evaluated, error_flash_ms)

        # brief error banner timeout
        if error_flash_ms and time.ticks_diff(now, error_flash_ms) > 600:
            error_flash_ms = 0
            _draw(oled, entry, acc, op, sel, just_evaluated, error_flash_ms)

        time.sleep_ms(2)

# ---------- Calculator core ----------
def _str_to_float(s):
    try:
        return float(s.replace(",", ".")) if s else 0.0
    except:
        return 0.0

def _format_num(x):
    # Nicely formatted to fit small screen
    if math.isinf(x) or math.isnan(x):
        return "Error"
    # Show integers without .0
    if abs(x - int(x)) < 1e-10 and abs(x) < 1e12:
        return str(int(x))
    # Otherwise clamp to ~8 significant places
    out = "{:.8f}".format(x).rstrip("0").rstrip(".")
    if len(out) > 12:
        out = "{:.6e}".format(x)
    return out

def _apply(acc, op, rhs):
    if op == "+": return acc + rhs
    if op == "-": return acc - rhs
    if op == "*": return acc * rhs
    if op == "/":
        if abs(rhs) < 1e-18:
            return float("nan")
        return acc / rhs
    return rhs  # no op -> just rhs

def _tap_key(k, entry, acc, op, last_rhs, just_evaluated):
    err_until = 0
    # map symbols
    if k == "×": kmap = "*"
    elif k == "÷": kmap = "/"
    elif k == "−": kmap = "-"
    else: kmap = k

    # digits / dot
    if kmap.isdigit() or kmap == ".":
        if just_evaluated and op is None:
            # start a fresh number after hitting '='
            entry = "0"
        just_evaluated = False
        if kmap == ".":
            if "." not in entry:
                entry = entry + "." if entry else "0."
        else:
            if entry == "0":
                entry = kmap
            elif entry == "-0":
                entry = "-" + kmap
            else:
                if len(entry) < 12:
                    entry += kmap
        return entry, acc, op, last_rhs, just_evaluated, err_until

    # sign toggle
    if kmap == "±":
        just_evaluated = False
        if entry.startswith("-"):
            entry = entry[1:] or "0"
        else:
            if entry != "0":
                entry = "-" + entry
            else:
                entry = "-0"
        return entry, acc, op, last_rhs, just_evaluated, err_until

    # backspace
    if kmap == "DEL":
        just_evaluated = False
        if len(entry) <= 1 or (len(entry) == 2 and entry.startswith("-")):
            entry = "0"
        else:
            entry = entry[:-1]
        return entry, acc, op, last_rhs, just_evaluated, err_until

    # clear
    if kmap == "C":
        return "0", 0.0, None, None, False, err_until

    # equals
    if kmap == "=":
        if op is None:
            # nothing pending; show current entry as result
            just_evaluated = True
            last_rhs = _str_to_float(entry)
            return _format_num(last_rhs), last_rhs, None, last_rhs, True, err_until
        # do op with rhs
        if entry in ("", "-", "-0"):
            rhs = last_rhs if last_rhs is not None else acc
        else:
            rhs = _str_to_float(entry)
            last_rhs = rhs
        res = _apply(acc, op, rhs)
        if math.isnan(res) or math.isinf(res):
            # error
            entry, acc, op, last_rhs, just_evaluated = "0", 0.0, None, None, False
            err_until = time.ticks_ms()
            return entry, acc, op, last_rhs, just_evaluated, err_until
        return _format_num(res), res, None, last_rhs, True, err_until

    # operator
    if kmap in ("+", "-", "*", "/"):
        rhs = _str_to_float(entry)
        if op is None:
            acc = rhs
        else:
            res = _apply(acc, op, rhs)
            if math.isnan(res) or math.isinf(res):
                return "0", 0.0, None, None, False, time.ticks_ms()
            acc = res
        op = kmap
        entry = "0"
        just_evaluated = False
        return entry, acc, op, last_rhs, just_evaluated, err_until

    # ignore unknown or blank cell
    return entry, acc, op, last_rhs, just_evaluated, err_until

# ---------- Drawing ----------
def _draw(oled, entry, acc, op, sel, just_eval, error_flash_ms):
    oled.fill(0)
    # Display area (top)
    # First line: pending expression "acc op"
    expr = ""
    if op is not None:
        expr = "{} {}".format(_format_num(acc), {"*":"×","/":"÷","-":"−","+" :"+"}[op])
    oled.text(expr[:21], 2, 2)

    # Second line: current entry/result (right-aligned)
    disp = entry if not just_eval or op is not None else entry
    # If entry is "0" or "-0" show as-is while editing
    text = disp
    # Right align
    x = W - 2 - len(text)*8
    if x < 2: x = 2
    y = 10
    oled.text(text, x, y)

    # Error banner (if any)
    if error_flash_ms:
        oled.fill_rect(0, 0, W, 12, 1)
        oled.text(" MATH ERROR ", 8, 2, 0)

    # Grid
    for idx, label in enumerate(KEYS):
        row = idx // COLS
        col = idx % COLS
        x0 = GRID_X0 + col * CELL_W
        y0 = GRID_Y0 + row * CELL_H
        selected = (idx == sel)
        if selected:
            oled.fill_rect(x0, y0, CELL_W-2, CELL_H-1, 1)
            _draw_key_label(oled, label, x0, y0, invert=True)
        else:
            oled.rect(x0, y0, CELL_W-2, CELL_H-1, 1)
            _draw_key_label(oled, label, x0, y0, invert=False)

    oled.show()

def _draw_key_label(oled, label, x0, y0, invert=False):
    # center text in the cell
    lab = label
    if lab == " ": lab = ""
    lx = x0 + (CELL_W-2 - len(lab)*8)//2
    if lx < x0+1: lx = x0+1
    ly = y0 + (CELL_H-8)//2
    color = 0 if invert else 1
    oled.text(lab, lx, ly, color)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 10, 26); oled.show()
    time.sleep_ms(160)
