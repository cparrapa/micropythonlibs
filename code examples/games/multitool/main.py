# main.py — Text-only menu + Startup Splash (Otto / Digital / Multitool)
# I2C0: SDA=19, SCL=18 (400 kHz); Button: GPIO4; Encoder A: GPIO22, B: GPIO21

import time
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# ---------- Pins ----------
I2C_ID  = 0
I2C_SDA = 19
I2C_SCL = 18
ENC_A_PIN = 22          # encoder channel A
ENC_B_PIN = 21          # encoder channel B
BTN_PIN   = 4           # encoder button
ENCODER_REVERSE = False

# ---------- OLED ----------
W, H = 128, 64

# ---------- I2C / OLED (400 kHz) ----------
i2c = I2C(I2C_ID, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=400000)
oled = SSD1306_I2C(W, H, i2c)

# ---------- Button (edge-based, polarity-agnostic) ----------
btn = Pin(BTN_PIN, Pin.IN)
_btn_idle = btn.value()
_in_press = False
_press_t0 = 0
def button_released(min_ms=60):
    """Return hold time (ms) when a full press cycle is completed; else None."""
    global _in_press, _press_t0, _btn_idle
    v = btn.value(); now = time.ticks_ms()
    if not _in_press:
        if v != _btn_idle:
            _in_press = True
            _press_t0 = now
    else:
        if v == _btn_idle:
            held = time.ticks_diff(now, _press_t0)
            _in_press = False
            return held if held >= min_ms else None
    return None

# ---------- Encoder (full quadrature A/B) ----------
enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)

_enc_state = (enc_a.value() << 1) | enc_b.value()
_enc_accum = 0
DETENT = 2  # transitions per click (many encoders are 2; set 4 if yours is stiffer)

def _enc_isr(pin):
    global _enc_state, _enc_accum
    a = enc_a.value(); b = enc_b.value()
    s = (a << 1) | b
    last = _enc_state
    if s == last: return
    # CW: 00->01->11->10->00
    if   (last == 0 and s == 1) or (last == 1 and s == 3) or (last == 3 and s == 2) or (last == 2 and s == 0):
        _enc_accum += 1
    # CCW: 00->10->11->01->00
    elif (last == 0 and s == 2) or (last == 2 and s == 3) or (last == 3 and s == 1) or (last == 1 and s == 0):
        _enc_accum -= 1
    _enc_state = s

enc_a.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=_enc_isr)
enc_b.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=_enc_isr)

# ---------- Apps ----------
import measure
import temperature
import light
import sound
import flashlight
import stopwatch
import dice
import wifi_scan
import pomodoro
import calculator   # NEW

# label, launcher
APPS = [
    ("Distance",     lambda: measure.run(i2c)),
    ("Temp & Hum",   lambda: temperature.run(i2c)),
    ("Light",        lambda: light.run(i2c)),
    ("Noise",        lambda: sound.run(i2c)),
    ("Flashlight",   lambda: flashlight.run(i2c)),
    ("Stopwatch",    lambda: stopwatch.run(i2c)),
    ("Dice Roller",  lambda: dice.run(i2c)),
    ("WiFi Scan",    lambda: wifi_scan.run(i2c)),
    ("Pomodoro",     lambda: pomodoro.run(i2c)),
    ("Calculator",   lambda: calculator.run(i2c)),  # NEW
]

# ---------- Splash (shown once on power-up) ----------
def _draw_tool_icon_ruler(xc=34, yc=32, w=60, h=18):
    """Simple 'tool' icon: chunky measuring ruler."""
    x = xc - w//2; y = yc - h//2
    oled.rect(x, y, w, h, 1)
    oled.hline(x+2, y + h//2, w-4, 1)
    step = 6
    for i in range(2, w-2, step):
        xpos = x + i
        major = ((i // step) % 5 == 0)
        t = 6 if major else 3
        oled.vline(xpos, y+1, t, 1)
        oled.vline(xpos, y + h - 1 - t, t, 1)

def _text_right_offset(s, y, offset_px=0, margin=2):
    """Right-align text with extra left offset (to slide in)."""
    x = W - margin - len(s)*8 - offset_px
    if x < 0: x = 0
    oled.text(s, x, y)

def splash_screen():
    # Three slide-in frames, then hold longer (1.6s)
    lines = ("Otto", "Digital", "Multitool")
    y_start = 12
    offsets = (24, 12, 0)  # ease-out slide distances
    for off in offsets:
        oled.fill(0)
        _draw_tool_icon_ruler(34, 32, 60, 18)
        _text_right_offset(lines[0], y_start + 0*18, off)
        _text_right_offset(lines[1], y_start + 1*18, off)
        _text_right_offset(lines[2], y_start + 2*18, off)
        oled.show()
        time.sleep_ms(100)
    time.sleep_ms(1600)

# ---------- UI helpers ----------
def clear(): oled.fill(0)

def draw_page_squares(idx, total):
    size = 6; gap = 6
    total_w = total*size + (total-1)*gap
    x0 = (W - total_w) // 2
    y  = H - size - 4
    for i in range(total):
        x = x0 + i*(size + gap)
        if i == idx: oled.fill_rect(x, y, size, size, 1)
        else:        oled.rect(x, y, size, size, 1)

def draw_center_text(text, y):
    x = (W - len(text)*8)//2
    if x < 0: x = 0
    oled.text(text, x, y)

def draw_menu(idx):
    clear()
    draw_center_text(APPS[idx][0], 28)
    draw_page_squares(idx, len(APPS))
    oled.show()

# ---------- Ultra-snappy slide (3 frames) ----------
def animate_slide(curr_idx, next_idx, direction):
    ease = (0.55, 0.90, 1.00)
    span = W
    curr = APPS[curr_idx][0]; nxt = APPS[next_idx][0]
    for f in ease:
        shift = int(span * f) * direction
        clear()
        oled.text(curr, (W - len(curr)*8)//2 - shift, 28)
        oled.text(nxt,  (W - len(nxt)*8)//2  + (span*direction) - shift, 28)
        draw_page_squares(next_idx, len(APPS))
        oled.show()
        time.sleep_ms(5)

def launch(idx):
    try:
        APPS[idx][1]()  # run app; returns on long-press inside app
    except Exception as e:
        clear()
        oled.text("ERR:", 0, 0); oled.text(str(e)[:20], 0, 12); oled.show()
        import sys; sys.print_exception(e)
        time.sleep_ms(600)

# ---------- Main ----------
splash_screen()
idx = 0
draw_menu(idx)

while True:
    moved = 0
    if _enc_accum >= DETENT:
        _enc_accum -= DETENT; moved = +1
    elif _enc_accum <= -DETENT:
        _enc_accum += DETENT; moved = -1

    if moved:
        if ENCODER_REVERSE: moved = -moved
        next_idx = (idx + moved) % len(APPS)
        animate_slide(idx, next_idx, +1 if moved > 0 else -1)
        idx = next_idx

    held = button_released(min_ms=60)
    if held is not None:
        oled.fill_rect(0,0,4,4,1); oled.show(); time.sleep_ms(40)
        draw_menu(idx)
        launch(idx)
        draw_menu(idx)

    time.sleep_ms(2)
