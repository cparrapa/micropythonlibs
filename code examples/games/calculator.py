# calculator.py — Encoder-only calculator (ASCII-only, I2C-safe show)

import time, math
from machine import Pin
from ssd1306 import SSD1306_I2C

# --- Pins (adjust for your wiring) ---
ENC_A_PIN = 22
ENC_B_PIN = 21
BTN_PIN   = 4

# OLED dimensions
W, H = 128, 64

# UI layout
TOP_H = 20
GRID_Y0 = TOP_H + 1
COLS, ROWS = 4, 5
CELL_W = 30
CELL_H = 8
GRID_X0 = (W - (COLS * CELL_W)) // 2

DETENT = 2
LONG_PRESS_S = 1.5

# Keys grid (ASCII only)
KEYS = [
    "C",  "DEL", "+/-", "/",   # row 0
    "7",  "8",   "9",   "*",   # row 1
    "4",  "5",   "6",   "-",   # row 2
    "1",  "2",   "3",   "+",   # row 3
    "0",  ".",   "=",   " "    # row 4
]

def _safe_show(oled, retries=3, delay_ms=4):
    for _ in range(retries):
        try:
            oled.show()
            return True
        except OSError:
            time.sleep_ms(delay_ms)
    try:
        oled.show()
        return True
    except OSError:
        return False

def run(shared_i2c):
    oled = SSD1306_I2C(W, H, shared_i2c)

    enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    btn   = Pin(BTN_PIN, Pin.IN)

    last_state = (enc_a.value() << 1) | enc_b.value()
    accum = 0
    sel = 0

    btn_idle = btn.value()
    in_press = False
    t0 = 0

    entry = "0"
    acc = 0.0
    op = None
    last_rhs = None
    just_evaluated = False
    error_flash_ms = 0

    _draw(oled, entry, acc, op, sel, just_evaluated, error_flash_ms)

    while True:
        now = time.ticks_ms()
        needs_redraw = False

        # --- Encoder handling ---
        s = (enc_a.value() << 1) | enc_b.value()
        moved = 0
        if s != last_state:
            if (last_state == 0b00 and s == 0b01) or (last_state == 0b01 and s == 0b11) or \
               (last_state == 0b11 and s == 0b10) or (last_state == 0b10 and s == 0b00):
                accum += 1
            elif (last_state == 0b00 and s == 0b10) or (last_state == 0b10 and s == 0b11) or \
                 (last_state == 0b11 and s == 0b01) or (last_state == 0b01 and s == 0b00):
                accum -= 1

            last_state = s

            if accum >= DETENT:
                accum = 0
                moved = 1
            elif accum <= -DETENT:
                accum = 0
                moved = -1

        if moved:
            sel = (sel + moved) % len(KEYS)
            needs_redraw = True

        # --- Button handling (debounced) ---
        v = btn.value()
        if not in_press and v != btn_idle:
            time.sleep_ms(20)
            if btn.value() == v:
                in_press = True
                t0 = now

        elif in_press and v == btn_idle:
            held = time.ticks_diff(now, t0)
            in_press = False
            if held >= int(LONG_PRESS_S * 1000):
                _goodbye(oled)
                return
            elif held >= 50:
                key = KEYS[sel]
                entry, acc, op, last_rhs, just_evaluated, error_flash_ms = _tap_key(
                    key, entry, acc, op, last_rhs, just_evaluated)
                needs_redraw = True

        if error_flash_ms and time.ticks_diff(now, error_flash_ms) > 600:
            error_flash_ms = 0
            needs_redraw = True

        if needs_redraw:
            _draw(oled, entry, acc, op, sel, just_evaluated, error_flash_ms)

        time.sleep_ms(4)  # prevent I2C overload

# ---------- Calculator core ----------
def _str_to_float(s):
    try:
        return float(s.replace(",", ".")) if s else 0.0
    except:
        return 0.0

def _format_num(x):
    if math.isinf(x) or math.isnan(x):
        return "Error"
    if abs(x - int(x)) < 1e-10:
        return str(int(x))
    out = "{:.6f}".format(x).rstrip("0").rstrip(".")
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
    return rhs

def _tap_key(k, entry, acc, op, last_rhs, just_evaluated):
    err_until = 0

    if k.isdigit() or k == ".":
        if just_evaluated and op is None:
            entry = "0"
        just_evaluated = False
        if k == ".":
            if "." not in entry:
                entry = entry + "." if entry else "0."
        else:
            if entry == "0":
                entry = k
            elif entry == "-0":
                entry = "-" + k
            else:
                if len(entry) < 12:
                    entry += k
        return entry, acc, op, last_rhs, just_evaluated, err_until

    if k == "+/-":
        just_evaluated = False
        if entry.startswith("-"):
            entry = entry[1:] or "0"
        else:
            entry = "-" + entry if entry != "0" else "-0"
        return entry, acc, op, last_rhs, just_evaluated, err_until

    if k == "DEL":
        just_evaluated = False
        if len(entry) <= 1 or (len(entry) == 2 and entry.startswith("-")):
            entry = "0"
        else:
            entry = entry[:-1]
        return entry, acc, op, last_rhs, just_evaluated, err_until

    if k == "C":
        return "0", 0.0, None, None, False, err_until

    if k == "=":
        if op is None:
            just_evaluated = True
            last_rhs = _str_to_float(entry)
            return _format_num(last_rhs), last_rhs, None, last_rhs, True, err_until
        if entry in ("", "-", "-0"):
            rhs = last_rhs if last_rhs is not None else acc
        else:
            rhs = _str_to_float(entry)
            last_rhs = rhs
        res = _apply(acc, op, rhs)
        if math.isnan(res) or math.isinf(res):
            return "0", 0.0, None, None, False, time.ticks_ms()
        return _format_num(res), res, None, last_rhs, True, err_until

    if k in ("+", "-", "*", "/"):
        rhs = _str_to_float(entry)
        if op is None:
            acc = rhs
        else:
            res = _apply(acc, op, rhs)
            if math.isnan(res) or math.isinf(res):
                return "0", 0.0, None, None, False, time.ticks_ms()
            acc = res
        op = k
        entry = "0"
        just_evaluated = False
        return entry, acc, op, last_rhs, just_evaluated, err_until

    return entry, acc, op, last_rhs, just_evaluated, err_until

# ---------- Drawing ----------
def _draw(oled, entry, acc, op, sel, just_eval, error_flash_ms):
    oled.fill(0)
    expr = "{} {}".format(_format_num(acc), op) if op is not None else ""
    oled.text(expr[:21], 2, 2)

    text = entry
    x = W - 2 - len(text)*8
    if x < 2: x = 2
    oled.text(text, x, 10)

    if error_flash_ms:
        oled.fill_rect(0, 0, W, 12, 1)
        oled.fill_rect(6, 1, 116, 10, 0)
        oled.text("MATH ERROR", (W - len("MATH ERROR")*8)//2, 2)

    for idx, label in enumerate(KEYS):
        row = idx // COLS
        col = idx % COLS
        x0 = GRID_X0 + col * CELL_W
        y0 = GRID_Y0 + row * CELL_H
        oled.rect(x0, y0, CELL_W-2, CELL_H-1, 1)
        if idx == sel:
            oled.rect(x0+1, y0+1, CELL_W-4, CELL_H-3, 1)
            oled.pixel(x0+2, y0+2, 1); oled.pixel(x0+CELL_W-5, y0+2, 1)
            oled.pixel(x0+2, y0+CELL_H-4, 1); oled.pixel(x0+CELL_W-5, y0+CELL_H-4, 1)
        _draw_key_label(oled, label, x0, y0)

    _safe_show(oled)

def _draw_key_label(oled, label, x0, y0):
    lab = "" if label == " " else label
    lx = x0 + (CELL_W-2 - len(lab)*8)//2
    if lx < x0+1: lx = x0+1
    ly = y0 + (CELL_H-8)//2
    oled.text(lab, lx, ly)

def _goodbye(oled):
    oled.fill(0)
    oled.text("Back to menu", 10, 26)
    _safe_show(oled)
    time.sleep_ms(160)
