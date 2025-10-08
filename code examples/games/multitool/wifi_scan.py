# wifi_scan.py — WiFi signal strength viewer (threaded scan + scrollable list)
# Controls:
#   - Rotate encoder (A=22, B=21): move selection (scrolls list)
#   - Short press (BTN=4): start a new scan (non-blocking)
#   - Long press (≥1.5 s): back to menu
#
# Notes:
# - Scans run in a background _thread (ESP32 MicroPython supports this).
# - If threads aren't available, falls back to blocking scan but will NOT crash
#   on KeyboardInterrupt — it catches it and keeps running.

import time
import network
from machine import Pin
from ssd1306 import SSD1306_I2C

# ---- Pins (match your wiring) ----
ENC_A_PIN = 22
ENC_B_PIN = 21
BTN_PIN   = 4

# ---- UI ----
OLED_W, OLED_H   = 128, 64
HEADER_H         = 12
ROW_H            = 13
VIEW_ROWS        = 4               # rows visible per page
LIST_Y0          = HEADER_H
LONG_PRESS_S     = 1.5
DETENT           = 2               # encoder transitions per detent
SPINNER          = ("|","/","-","\\")

# ---- Thread support ----
try:
    import _thread
    HAVE_THREAD = True
except:
    HAVE_THREAD = False

def run(shared_i2c):
    oled = SSD1306_I2C(OLED_W, OLED_H, shared_i2c)

    # Inputs
    enc_a = Pin(ENC_A_PIN, Pin.IN, Pin.PULL_UP)
    enc_b = Pin(ENC_B_PIN, Pin.IN, Pin.PULL_UP)
    btn   = Pin(BTN_PIN, Pin.IN)

    _splash(oled)

    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)
        time.sleep_ms(80)

    # ---- State ----
    rows      = []     # [(ssid, rssi, ch), ...]
    selected  = 0
    offset    = 0
    scanning  = False
    spin_i    = 0
    last_err  = None

    # For threaded mode: stage results in new_rows under a lock
    lock = _thread.allocate_lock() if HAVE_THREAD else None
    new_rows = None

    # Encoder (polled quadrature)
    last_state = (enc_a.value() << 1) | enc_b.value()
    accum = 0

    # Button state
    btn_idle = btn.value(); in_press = False; t0 = 0

    # Kick off an initial scan
    def _start_scan():
        nonlocal scanning, last_err, new_rows
        if scanning:
            return
        scanning = True
        last_err = None
        if HAVE_THREAD:
            def worker():
                nonlocal scanning, last_err, new_rows
                try:
                    parsed = _do_scan(wlan)
                    if lock:
                        lock.acquire()
                        new_rows = parsed
                        lock.release()
                except Exception as e:
                    last_err = str(e)
                finally:
                    scanning = False
            _thread.start_new_thread(worker, ())
        else:
            # Fallback: blocking scan but swallow KeyboardInterrupt/Errors
            try:
                parsed = _do_scan(wlan)
                rows[:] = parsed  # replace contents in-place
                selected = min(selected, max(0, len(rows)-1))
                offset   = _fit_offset(offset, selected, len(rows))
            except Exception as e:
                last_err = str(e)
            finally:
                scanning = False

    _start_scan()

    # ---- Main loop ----
    while True:
        now = time.ticks_ms()

        # Pull in finished threaded results
        if HAVE_THREAD and not scanning:
            if lock:
                lock.acquire()
                pending = new_rows
                new_rows = None
                lock.release()
            else:
                pending = None
            if pending is not None:
                rows = pending
                selected = min(selected, max(0, len(rows)-1))
                offset   = _fit_offset(offset, selected, len(rows))

        # ----- Encoder (scroll selection) -----
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

            if moved and rows:
                selected = _clamp(selected + moved, 0, len(rows) - 1)
                if selected < offset:
                    offset = selected
                elif selected >= offset + VIEW_ROWS:
                    offset = selected - VIEW_ROWS + 1

        # ----- Button (short/long) -----
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
                    _start_scan()

        # ----- Draw -----
        spin_i = (spin_i + 1) % len(SPINNER)
        _draw(oled, rows, selected, offset,
              spinner=SPINNER[spin_i] if scanning else None,
              error=last_err)

        time.sleep_ms(90)

# ---- Scan helpers ----
def _do_scan(wlan):
    """Perform the scan and return parsed list. Never raises KeyboardInterrupt."""
    try:
        nets = wlan.scan()  # [(ssid,bssid,channel,rssi,auth,hidden), ...]
    except KeyboardInterrupt:
        # user poked the REPL during scan; just return empty list
        return []
    except Exception as e:
        # Propagate to caller to display error
        raise e

    out = []
    for e in nets:
        try:
            ssid = e[0].decode("utf-8", "ignore") if isinstance(e[0], bytes) else str(e[0])
        except:
            ssid = "<noname>"
        rssi = int(e[3]) if len(e) > 3 else -100
        ch   = int(e[2]) if len(e) > 2 else 0
        out.append((ssid, rssi, ch))
    out.sort(key=lambda x: x[1], reverse=True)
    return out

# ---- UI helpers ----
def _clamp(v, lo, hi):
    return lo if v < lo else hi if v > hi else v

def _fit_offset(offset, selected, total):
    if selected < offset:
        offset = selected
    elif selected >= offset + VIEW_ROWS:
        offset = selected - VIEW_ROWS + 1
    max_off = max(0, total - VIEW_ROWS)
    return _clamp(offset, 0, max_off)

def _bars_for_rssi(dbm):
    if dbm >= -50: return 4
    if dbm >= -60: return 3
    if dbm >= -70: return 2
    if dbm >= -80: return 1
    return 0

def _draw_bars(oled, x, y, level):
    heights = (3,5,7,9)
    for i,h in enumerate(heights):
        if i < level:
            oled.fill_rect(x + i*4, y + (10-h), 3, h, 1)
        else:
            oled.rect(x + i*4, y + (10-h), 3, h, 1)

def _truncate(name, max_chars):
    return name if len(name) <= max_chars else (name[:max_chars-1] + "…")

def _draw_header(oled, count, spinner=None, error=None):
    oled.fill_rect(0, 0, OLED_W, HEADER_H, 0)
    title = "WiFi SCAN"
    if spinner:
        title += " " + spinner
    x = (OLED_W - len(title)*8)//2
    if x < 0: x = 0
    oled.text(title, x, 0)
    right = "{}".format(count)
    oled.text(right, OLED_W - len(right)*8 - 2, 0)
    oled.hline(0, HEADER_H-1, OLED_W, 1)
    if error:
        # show one-line error just under header if any
        msg = _truncate(error, 16)
        oled.text(msg, 2, HEADER_H+1)

def _draw_scrollbar(oled, total, offset):
    if total <= VIEW_ROWS:
        return
    bar_x = OLED_W - 3
    oled.vline(bar_x, HEADER_H, OLED_H - HEADER_H - 1, 1)
    track_h = OLED_H - HEADER_H - 1
    bar_h = max(6, track_h * VIEW_ROWS // total)
    bar_y = HEADER_H + (track_h - bar_h) * offset // max(1, total - VIEW_ROWS)
    oled.fill_rect(bar_x-1, bar_y, 3, bar_h, 1)

def _draw(oled, rows, selected, offset, spinner=None, error=None):
    oled.fill(0)
    _draw_header(oled, len(rows), spinner, error)

    # render list area
    total = len(rows)
    y = LIST_Y0
    x_text = 24

    start_row = offset
    end_row   = min(offset + VIEW_ROWS, total)
    for idx in range(start_row, end_row):
        ssid, rssi, ch = rows[idx]
        if idx == selected:
            oled.text(">", 0, y)
        _draw_bars(oled, 8, y+1, _bars_for_rssi(rssi))
        name = _truncate(ssid, 11)
        oled.text("{:<11}".format(name), x_text, y)
        oled.text("{:>4}dBm ch{:>2}".format(rssi, ch), x_text, y+8)
        y += ROW_H

    _draw_scrollbar(oled, total, offset)
    oled.show()

def _splash(oled):
    oled.fill(0); oled.text("WiFi SCAN", 28, 18); oled.text("Starting...", 20, 34); oled.show()
    time.sleep_ms(220)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 10, 26); oled.show()
    time.sleep_ms(160)
