import time, math
from machine import Pin
from ssd1306 import SSD1306_I2C

# ---- Pins ----
ENC_A_PIN = 22
ENC_B_PIN = 21
LEFT_BTN_PIN  = 4      # left button
RIGHT_BTN_PIN = 27     # encoder push button

# ---- UI ----
W, H = 128, 64
DETENT = 2

# ---- OLED safe show ----
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

# ---------- Encoder (polled quadrature) ----------
def _enc_init():
    a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    state = (a.value() << 1) | b.value()
    return a, b, state

def _enc_delta(enc_a, enc_b, last_state, accum):
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
    return moved, last_state, accum

# ---------- Math helpers ----------
def _ip(i_pct_annual, py):
    py = max(1, int(py))
    return (i_pct_annual / 100.0) / py

def _pow1p(i, n):
    return math.pow(1.0 + i, n)

def _solve_pv(n, i, pmt, fv, begin):
    if abs(i) < 1e-12:
        return -(fv + pmt * n)
    g = 1.0 + i
    k = (1.0 + i) if begin else 1.0
    return -(fv + pmt * k * ((_pow1p(i, n) - 1.0) / i)) / _pow1p(i, n)

def _solve_fv(n, i, pv, pmt, begin):
    if abs(i) < 1e-12:
        return -(pv + pmt * n)
    k = (1.0 + i) if begin else 1.0
    return -(pv * _pow1p(i, n) + pmt * k * ((_pow1p(i, n) - 1.0) / i))

def _solve_pmt(n, i, pv, fv, begin):
    if n <= 0: return 0.0
    if abs(i) < 1e-12:
        return -(fv + pv) / n
    g = _pow1p(i, n)
    k = (1.0 + i) if begin else 1.0
    denom = k * (g - 1.0) / i
    if abs(denom) < 1e-18: return 0.0
    return -(fv + pv * g) / denom

def _solve_n(i, pv, pmt, fv, begin):
    if abs(i) < 1e-12:
        if abs(pmt) < 1e-18:
            return float('nan')
        return -(fv + pv) / pmt
    k = (1.0 + i) if begin else 1.0
    A = (pmt * k) / i
    denom = (pv + A)
    num   = (A - fv)
    if denom <= 0 or num <= 0:
        ln_g = math.log(1.0 + i)
        N = max(0.0, (0.0 if abs(pmt) < 1e-12 else (-(fv + pv) / max(1e-12, pmt))))
        for _ in range(60):
            gN = _pow1p(i, N)
            f  = pv * gN + pmt * k * ((gN - 1.0) / i) + fv
            df = ln_g * (pv * gN + pmt * k * (gN / i))
            if abs(df) < 1e-14: break
            step = f / df
            N -= step
            if abs(step) < 1e-9: break
        return N
    return math.log(num / denom) / math.log(1.0 + i)

def _solve_i(n, pv, pmt, fv, begin):
    def _f_i(i):
        g = _pow1p(i, n)
        if abs(i) < 1e-14:
            return fv + pv + pmt * n
        k = (1.0 + i) if begin else 1.0
        return fv + pv * g + pmt * k * ((g - 1.0) / i)

    f0 = _f_i(0.0)
    if abs(f0) < 1e-9:
        return 0.0
    lo = -0.9999
    hi = 1.0
    flo = _f_i(lo)
    fhi = _f_i(hi)
    tries = 0
    while (flo * fhi > 0.0) and hi < 100.0 and tries < 30:
        hi *= 2.0
        fhi = _f_i(hi)
        tries += 1
    if flo * fhi > 0.0:
        i = 0.05
        for _ in range(60):
            g = _pow1p(i, n)
            if abs(i) < 1e-12:
                f = fv + pv + pmt * n
                df = pmt * (begin and 1.0 or 0.0) * n
            else:
                k = (1.0 + i) if begin else 1.0
                f = fv + pv * g + pmt * k * ((g - 1.0) / i)
                ln_g = math.log(1.0 + i)
                d_g  = n * _pow1p(i, n-1)
                d_term = ((i * d_g - (g - 1.0)) / (i * i))
                df = pv * d_g + pmt * ((begin and 1.0 or 0.0) * ((g - 1.0) / i) + ((1.0 + i) if begin else 1.0) * d_term)
            if abs(df) < 1e-14: break
            step = f / df
            i -= step
            if abs(step) < 1e-10: break
        return i
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        fm = _f_i(mid)
        if fm == 0 or abs(hi - lo) < 1e-12:
            return mid
        if flo * fm < 0:
            hi = mid; fhi = fm
        else:
            lo = mid; flo = fm
    return 0.5 * (lo + hi)

# ---------- App ----------
def run(shared_i2c):
    oled = SSD1306_I2C(W, H, shared_i2c)
    enc_a, enc_b, enc_state = _enc_init()
    enc_accum = 0
    btnR = Pin(RIGHT_BTN_PIN, Pin.IN, Pin.PULL_UP)

    items = ["Solve", "N", "I%", "P/Y", "PV", "PMT", "FV", "Mode", "Compute", "Clear All", "Exit App"]
    SOLVES = ["PV", "PMT", "FV", "N", "I%"]
    solve_idx = 0
    sel = 0
    editing = False

    N, IAPR, PY, PV, PMT, FV, MODE_BEGIN = 12.0, 12.0, 12.0, -1000.0, 100.0, 0.0, False
    STEPS = {"N": 1.0, "I%": 0.1, "P/Y": 1.0, "PV": 10.0, "PMT": 10.0, "FV": 10.0}

    def fmt(x, places=4):
        if abs(x) >= 1e10:
            s = "{:.6e}".format(x)
        else:
            s = "{:.4f}".format(x).rstrip("0").rstrip(".")
        return "0" if s == "-0" else s

    def draw():
        oled.fill(0)
        oled.text("TVM Solve: {}".format(SOLVES[solve_idx])[:21], 0, 0)
        first = max(0, min(sel - 4, len(items) - 6))
        values = {
            "Solve": SOLVES[solve_idx],
            "N": fmt(N), "I%": fmt(IAPR), "P/Y": fmt(PY),
            "PV": fmt(PV), "PMT": fmt(PMT), "FV": fmt(FV),
            "Mode": "BEGIN" if MODE_BEGIN else "END",
            "Compute": "▶", "Clear All": "", "Exit App": ""
        }
        for i in range(first, min(first + 6, len(items))):
            y = 12 + (i - first) * 9
            is_selected = (i == sel)
            if is_selected:
                oled.fill_rect(0, y - 1, W, 9, 1)
                oled.text("▶", 0, y, 0)
                text_color = 0
            else:
                text_color = 1
            oled.text("{:<9}".format(items[i]), 10, y, text_color)
            val = values[items[i]]
            oled.text(val, W - 2 - 8 * len(val), y, text_color)
        _safe_show(oled)

    def compute_now():
        nonlocal PV, PMT, FV, N, IAPR
        i_per = _ip(IAPR, max(1.0, PY))
        begin = MODE_BEGIN
        if SOLVES[solve_idx] == "PV": PV = _solve_pv(N, i_per, PMT, FV, begin)
        elif SOLVES[solve_idx] == "PMT": PMT = _solve_pmt(N, i_per, PV, FV, begin)
        elif SOLVES[solve_idx] == "FV": FV = _solve_fv(N, i_per, PV, PMT, begin)
        elif SOLVES[solve_idx] == "N": N = _solve_n(i_per, PV, PMT, FV, begin)
        else:
            i_per = _solve_i(N, PV, PMT, FV, begin)
            IAPR = i_per * PY * 100.0

    draw()
    while True:
        moved, enc_state, enc_accum = _enc_delta(enc_a, enc_b, enc_state, enc_accum)
        if moved:
            if editing:
                name = items[sel]
                step = STEPS.get(name, 1.0)
                if name == "N": N = max(0.0, N + moved * step)
                elif name == "I%": IAPR = max(-100.0, IAPR + moved * step)
                elif name == "P/Y": PY = max(1.0, PY + moved * step)
                elif name == "PV": PV += moved * step
                elif name == "PMT": PMT += moved * step
                elif name == "FV": FV += moved * step
            else:
                sel = (sel + moved) % len(items)
            draw()

        if btnR.value() == 0:
            t0 = time.ticks_ms()
            while btnR.value() == 0:
                time.sleep_ms(1)
            if time.ticks_diff(time.ticks_ms(), t0) > 50:
                name = items[sel]
                if name == "Solve": solve_idx = (solve_idx + 1) % len(SOLVES)
                elif name in STEPS: editing = not editing
                elif name == "Mode": MODE_BEGIN = not MODE_BEGIN
                elif name == "Compute": compute_now()
                elif name == "Clear All": N, IAPR, PY, PV, PMT, FV, MODE_BEGIN = 12.0, 12.0, 12.0, -1000.0, 100.0, 0.0, False
                elif name == "Exit App":
                    oled.fill(0)
                    oled.text("Back to menu", 10, 26)
                    _safe_show(oled)
                    time.sleep_ms(160)
                    return
                draw()
        time.sleep_ms(2)

