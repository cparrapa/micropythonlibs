# main.py — ESP32 + SSD1306 (128x64) + Animated Eyes + Tilt-to-Clock + Sleepy idle mode
# New behavior:
# - If no interaction (tilt) for SLEEP_AFTER_S seconds, eyes become "sleepy" (half-lids + slower motion)
# - If idle longer than SLEEP_BLINK_AFTER_S, eyes close fully (sleep) with occasional slow blink
# - Any tilt wakes him up and shows clock/weather.

from machine import Pin, I2C
import time, gc
import network
import ntptime
import dht
import ssd1306

try:
    import urequests as requests
except ImportError:
    import requests


# ---------------- USER SETTINGS ----------------
WIFI_SSID = "wifi-ssid-here"
WIFI_PASS = "password"

LAT = 49.1951
LON = 16.6068
UTC_OFFSET_HOURS = 1

OLED_W = 128
OLED_H = 64
I2C_SCL = 18
I2C_SDA = 19
I2C_BUS_CANDIDATES = (0, 1)

# DHT11 on GPIO4
DHT_PIN = 4
DHT_MIN_INTERVAL_S = 1.2

# Tilt switch on GPIO26 (one side to GPIO26, other to GND)
TILT_PIN = 26
TILT_ACTIVE_LOW = True  # closed to GND -> 0

SHOW_CLOCK_SECONDS_AFTER_TILT = 8

# Network refresh behavior
WIFI_TRY_PERIOD_S = 15
WEATHER_PERIOD_S = 10 * 60
NTP_RESYNC_PERIOD_S = 6 * 60 * 60

# ---- Tilt sensitivity tuning ----
TILT_SCORE_TRIGGER = 6
TILT_SCORE_DECAY = 1
TILT_COOLDOWN_MS = 700
# --------------------------------

# ---- Sleep behavior tuning ----
SLEEP_AFTER_S = 45            # after 45s no tilt => sleepy eyes
SLEEP_BLINK_AFTER_S = 120     # after 2 min no tilt => fully asleep (eyes closed)
SLEEP_WAKE_FLASH_MS = 250     # tiny "wake" effect time
# --------------------------------
# ------------------------------------------------


# ---------------- OLED INIT ----------------
def init_oled():
    last_err = None
    for bus_id in I2C_BUS_CANDIDATES:
        try:
            i2c = I2C(bus_id, scl=Pin(I2C_SCL), sda=Pin(I2C_SDA), freq=400000)
            addrs = i2c.scan()
            print("I2C bus", bus_id, "scan:", [hex(a) for a in addrs])

            addr = None
            for cand in (0x3C, 0x3D):
                if cand in addrs:
                    addr = cand
                    break
            if addr is None:
                continue

            oled = ssd1306.SSD1306_I2C(OLED_W, OLED_H, i2c, addr=addr)
            oled.fill(0)
            oled.text("OLED OK", 0, 0, 1)
            oled.text("bus:{} {}".format(bus_id, hex(addr)), 0, 12, 1)
            oled.show()
            time.sleep(0.5)
            return oled

        except Exception as e:
            last_err = e
            print("OLED init failed on bus", bus_id, ":", repr(e))

    raise RuntimeError("OLED not found. Last: {}".format(last_err))


# ---------------- WIFI (NON-FATAL) ----------------
def wifi_start():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    return wlan

def wifi_try_connect(wlan, ssid, password, timeout_s=10):
    try:
        if not wlan.active():
            wlan.active(True)
            time.sleep(0.3)

        if wlan.isconnected():
            return True

        try:
            wlan.disconnect()
        except Exception:
            pass
        time.sleep(0.2)

        wlan.connect(ssid, password)

        t0 = time.time()
        while not wlan.isconnected():
            if time.time() - t0 > timeout_s:
                return False
            time.sleep(0.2)

        return True

    except Exception as e:
        print("wifi_try_connect err:", repr(e))
        return False


# ---------------- TIME ----------------
def sync_time():
    try:
        ntptime.host = "pool.ntp.org"
        ntptime.settime()
        return True
    except Exception as e:
        print("NTP failed:", repr(e))
        return False

def localtime_tuple():
    return time.localtime(time.time() + UTC_OFFSET_HOURS * 3600)

def hhmmss():
    lt = localtime_tuple()
    return lt[3], lt[4], lt[5]


# ---------------- WEATHER ----------------
def fetch_outside_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude={}&longitude={}"
        "&current_weather=true"
        "&timezone=UTC"
    ).format(lat, lon)
    r = requests.get(url)
    data = r.json()
    r.close()
    cw = data.get("current_weather", {})
    return cw.get("temperature", None), cw.get("weathercode", 0)

def weather_group(wcode):
    if wcode == 0:
        return "sun"
    if wcode in (1, 2, 3):
        return "cloud"
    if wcode in (45, 48):
        return "fog"
    if wcode in (51, 53, 55, 61, 63, 65, 80, 81, 82):
        return "rain"
    if wcode in (71, 73, 75, 85, 86):
        return "snow"
    if wcode in (95, 96, 99):
        return "storm"
    return "cloud"


# ---------------- DHT11 ----------------
_dht_pin = Pin(DHT_PIN, Pin.IN, Pin.PULL_UP)
_dht = dht.DHT11(_dht_pin)
_last_dht_ts = 0

def plausible_dht(t, h):
    if t is None or h is None:
        return False
    if not (-10.0 <= t <= 50.0):
        return False
    if not (0.0 <= h <= 100.0):
        return False
    return True

def read_dht(last_good_t, last_good_h):
    global _last_dht_ts
    now = time.time()
    if now - _last_dht_ts < DHT_MIN_INTERVAL_S:
        return last_good_t, last_good_h
    _last_dht_ts = now

    for _ in range(6):
        try:
            _dht.measure()
            t = float(_dht.temperature())
            h = float(_dht.humidity())
            if plausible_dht(t, h):
                return t, h
            time.sleep(0.25)
        except Exception:
            time.sleep(0.35)
    return last_good_t, last_good_h


# ---------------- Tilt detection (integrator) ----------------
tilt = Pin(TILT_PIN, Pin.IN, Pin.PULL_UP)

def tilt_active():
    v = tilt.value()
    return (v == 0) if TILT_ACTIVE_LOW else (v == 1)

_tilt_score = 0
_tilt_last_ms = time.ticks_ms()
_tilt_cooldown_until = 0

def tilt_event():
    global _tilt_score, _tilt_last_ms, _tilt_cooldown_until

    now = time.ticks_ms()
    if time.ticks_diff(now, _tilt_cooldown_until) < 0:
        return False

    dt = time.ticks_diff(now, _tilt_last_ms)
    if dt < 15:
        return False
    _tilt_last_ms = now

    if tilt_active():
        _tilt_score += 2
    else:
        _tilt_score -= TILT_SCORE_DECAY

    if _tilt_score < 0:
        _tilt_score = 0
    if _tilt_score > 50:
        _tilt_score = 50

    if _tilt_score >= TILT_SCORE_TRIGGER:
        _tilt_score = 0
        _tilt_cooldown_until = time.ticks_add(now, TILT_COOLDOWN_MS)
        return True

    return False


# ---------------- Drawing primitives ----------------
def fill_circle(oled, cx, cy, r, color=1):
    for x in range(-r, r + 1):
        y = int((r * r - x * x) ** 0.5)
        oled.vline(cx + x, cy - y, 2 * y + 1, color)

def fill_round_rect(oled, x, y, w, h, r, color=1):
    r = max(0, min(r, w // 2, h // 2))
    oled.fill_rect(x + r, y, w - 2 * r, h, color)
    oled.fill_rect(x, y + r, r, h - 2 * r, color)
    oled.fill_rect(x + w - r, y + r, r, h - 2 * r, color)

    if r > 0:
        for dx in range(r):
            dy = int((r * r - dx * dx) ** 0.5)
            oled.vline(x + r - dx - 1, y + r - dy, dy, color)
        for dx in range(r):
            dy = int((r * r - dx * dx) ** 0.5)
            oled.vline(x + w - r + dx, y + r - dy, dy, color)
        for dx in range(r):
            dy = int((r * r - dx * dx) ** 0.5)
            oled.vline(x + r - dx - 1, y + h - r, dy, color)
        for dx in range(r):
            dy = int((r * r - dx * dx) ** 0.5)
            oled.vline(x + w - r + dx, y + h - r, dy, color)


# ---------------- Weather icons (16x16) ----------------
SUN_ICON = bytes([
    0x00,0x00, 0x03,0xC0, 0x0C,0x30, 0x18,0x18,
    0x10,0x08, 0x21,0x84, 0x23,0xC4, 0x47,0xE2,
    0x47,0xE2, 0x23,0xC4, 0x21,0x84, 0x10,0x08,
    0x18,0x18, 0x0C,0x30, 0x03,0xC0, 0x00,0x00
])
CLOUD_ICON = bytes([
    0x00,0x00, 0x00,0x00, 0x03,0x80, 0x07,0xC0,
    0x0C,0x60, 0x18,0x30, 0x10,0x10, 0x30,0x18,
    0x7F,0xFC, 0xFF,0xFE, 0xFF,0xFE, 0x7F,0xFC,
    0x00,0x00, 0x00,0x00, 0x00,0x00, 0x00,0x00
])
RAIN_ICON = bytes([
    0x00,0x00, 0x03,0x80, 0x07,0xC0, 0x0C,0x60,
    0x18,0x30, 0x10,0x10, 0x30,0x18, 0x7F,0xFC,
    0xFF,0xFE, 0x7F,0xFC, 0x04,0x40, 0x08,0x20,
    0x04,0x40, 0x08,0x20, 0x04,0x40, 0x00,0x00
])

def blit_16x16(oled, x, y, icon_bytes):
    import framebuf
    fb = framebuf.FrameBuffer(bytearray(icon_bytes), 16, 16, framebuf.MONO_HLSB)
    oled.blit(fb, x, y)

def weather_icon_bytes(group):
    if group == "sun":
        return SUN_ICON
    if group == "rain":
        return RAIN_ICON
    return CLOUD_ICON


# ---------------- Eye animation with sleep expressions ----------------
class Eyes:
    def __init__(self):
        self.eye_w = 40
        self.eye_h = 34
        self.r = 8
        self.gap = 10

        self.center_y = 16
        self.left_x = (OLED_W - (2 * self.eye_w + self.gap)) // 2
        self.right_x = self.left_x + self.eye_w + self.gap

        self.px = 0.0
        self.py = 0.0
        self.vx = 0.0
        self.vy = 0.0

        self.blink_phase = 0
        self.blink_t = time.ticks_ms()
        self.next_blink_ms = time.ticks_add(self.blink_t, 1200)
        self.next_squint_ms = time.ticks_add(self.blink_t, 2500)

        # sleep micro-timing
        self._sleep_blink_next = time.ticks_add(self.blink_t, 2000)

    def step(self, sleepy=False, asleep=False):
        """
        sleepy: slower motion + more squints
        asleep: mostly closed eyes, occasional slow blink
        """
        now = time.ticks_ms()

        # movement: reduce when sleepy/asleep
        move_mul = 1.0
        if sleepy:
            move_mul = 0.35
        if asleep:
            move_mul = 0.05

        self.vx = 0.92 * self.vx + 0.08 * (0.8 * (1 if (now // 700) % 2 == 0 else -1)) * move_mul
        self.vy = 0.92 * self.vy + 0.08 * (0.6 * (1 if (now // 900) % 2 == 0 else -1)) * move_mul

        self.px += 0.05 * self.vx
        self.py += 0.05 * self.vy
        self.px = max(-1.0, min(1.0, self.px))
        self.py = max(-1.0, min(1.0, self.py))

        # Blink behavior
        blink_amt = 0.0
        squint = False

        if asleep:
            # slow "breathing blink": mostly closed, briefly open a little sometimes
            if time.ticks_diff(now, self._sleep_blink_next) >= 0:
                # schedule next in ~2.5–4.5s deterministic
                jitter = (now // 41) % 2000
                self._sleep_blink_next = time.ticks_add(now, 2500 + jitter)
                # do a brief partial opening (we'll represent as blink_amt smaller)
                blink_amt = 0.75  # keeps eyes mostly closed
            else:
                blink_amt = 1.0   # closed
            return blink_amt, False  # squint irrelevant

        # normal blink scheduling, but slower when sleepy
        base = 1400 if sleepy else 1200
        if time.ticks_diff(now, self.next_blink_ms) >= 0 and self.blink_phase == 0:
            self.blink_phase = 1
            self.blink_t = now

        if self.blink_phase == 1:
            dt = time.ticks_diff(now, self.blink_t)
            close_ms = 180 if sleepy else 120
            blink_amt = min(1.0, dt / close_ms)
            if blink_amt >= 1.0:
                self.blink_phase = 2
                self.blink_t = now
        elif self.blink_phase == 2:
            dt = time.ticks_diff(now, self.blink_t)
            open_ms = 260 if sleepy else 160
            blink_amt = max(0.0, 1.0 - dt / open_ms)
            if blink_amt <= 0.0:
                self.blink_phase = 0
                jitter = (now // 37) % 1100
                self.next_blink_ms = time.ticks_add(now, base + jitter)

        # more squints when sleepy
        if sleepy and (now // 900) % 7 == 0 and blink_amt < 0.2:
            squint = True
        else:
            if time.ticks_diff(now, self.next_squint_ms) >= 0:
                squint = True
                jitter = (now // 29) % 4000
                self.next_squint_ms = time.ticks_add(now, 5000 + jitter)

        return blink_amt, squint

    def draw(self, oled, blink_amt, squint, sleepy=False, asleep=False):
        oled.fill(0)

        # base eye height
        h = int(self.eye_h * (1.0 - 0.85 * blink_amt))
        h = max(3, h)

        # sleepy makes eyelids heavier (lower max opening)
        if sleepy and not asleep:
            h = max(6, min(h, int(self.eye_h * 0.65)))

        # asleep: enforce very small slit
        if asleep:
            h = 3

        if squint and blink_amt < 0.2 and not asleep:
            h = max(6, int(h * 0.6))

        y = self.center_y + (self.eye_h - h) // 2

        fill_round_rect(oled, self.left_x, y, self.eye_w, h, min(self.r, h // 2), 1)
        fill_round_rect(oled, self.right_x, y, self.eye_w, h, min(self.r, h // 2), 1)

        # pupils only if not fully asleep
        if not asleep:
            ox = int(self.px * 8)
            oy = int(self.py * 6)

            pcx_l = self.left_x + self.eye_w // 2 + ox
            pcy_l = y + h // 2 + oy
            pcx_r = self.right_x + self.eye_w // 2 + ox
            pcy_r = y + h // 2 + oy

            pr = 6 if h > 10 else 3
            fill_circle(oled, pcx_l, pcy_l, pr, 0)
            fill_circle(oled, pcx_r, pcy_r, pr, 0)

            if h > 10 and blink_amt < 0.3:
                oled.pixel(pcx_l - 2, pcy_l - 2, 1)
                oled.pixel(pcx_r - 2, pcy_r - 2, 1)

        oled.show()


# ---------------- Clock UI (clean + icon) ----------------
DIGITS_3x5 = {
    '0': ["111","101","101","101","111"],
    '1': ["010","110","010","010","111"],
    '2': ["111","001","111","100","111"],
    '3': ["111","001","111","001","111"],
    '4': ["101","101","111","001","001"],
    '5': ["111","100","111","001","111"],
    '6': ["111","100","111","101","111"],
    '7': ["111","001","001","001","001"],
    '8': ["111","101","111","101","111"],
    '9': ["111","101","111","001","111"],
}

def draw_big_digit(oled, ch, x, y, scale=4, color=1):
    pat = DIGITS_3x5.get(ch)
    if not pat:
        return
    for r in range(5):
        row = pat[r]
        for c in range(3):
            if row[c] == "1":
                oled.fill_rect(x + c * scale, y + r * scale, scale, scale, color)

def draw_big_colon(oled, x, y, scale=4, on=True, color=1):
    if not on:
        return
    oled.fill_rect(x, y + 1 * scale, scale, scale, color)
    oled.fill_rect(x, y + 3 * scale, scale, scale, color)

def draw_big_time(oled, hh, mm, blink_on, top_y=2, scale=4):
    s = "{:02d}{:02d}".format(hh, mm)
    digit_w = 3 * scale
    colon_w = 1 * scale
    gap = 1 * scale
    total_w = digit_w * 4 + colon_w + gap * 4
    x0 = (OLED_W - total_w) // 2

    x = x0
    draw_big_digit(oled, s[0], x, top_y, scale); x += digit_w + gap
    draw_big_digit(oled, s[1], x, top_y, scale); x += digit_w + gap
    draw_big_colon(oled, x, top_y, scale, on=blink_on); x += colon_w + gap
    draw_big_digit(oled, s[2], x, top_y, scale); x += digit_w + gap
    draw_big_digit(oled, s[3], x, top_y, scale)

def draw_clock_screen(oled, wifi_ok, out_temp, wgroup, in_t, in_h):
    hh, mm, ss = hhmmss()

    oled.fill(0)
    draw_big_time(oled, hh, mm, (ss % 2 == 0), top_y=2, scale=4)
    oled.text("{:02d}".format(ss), OLED_W - 16, 26, 1)

    oled.hline(0, 34, OLED_W, 1)

    y1, y2, y3 = 36, 46, 56

    if not wifi_ok:
        oled.text("OFFLINE", 0, y1, 1)

    blit_16x16(oled, 112, 36, weather_icon_bytes(wgroup))

    out_s = "--.-C" if out_temp is None else "{:.1f}C".format(out_temp)
    oled.text("OUT:", 0, y2, 1)
    oled.text(out_s, 40, y2, 1)

    in_ts = "--C" if in_t is None else "{:.0f}C".format(in_t)
    in_hs = "--%" if in_h is None else "{:>2.0f}%".format(in_h)

    oled.text("IN:", 0, y3, 1)
    oled.text(in_ts, 32, y3, 1)
    oled.text(in_hs, 72, y3, 1)

    oled.show()


# ---------------- MAIN ----------------
def main():
    gc.collect()
    oled = init_oled()

    wlan = wifi_start()
    wifi_ok = False
    last_wifi_try = 0

    wifi_ok = wifi_try_connect(wlan, WIFI_SSID, WIFI_PASS, timeout_s=8)
    if wifi_ok:
        print("WiFi connected:", wlan.ifconfig())
        sync_time()
    else:
        print("WiFi offline (will retry).")

    last_ntp = time.time()
    out_temp = None
    wgroup = "cloud"
    last_weather = 0

    in_t = None
    in_h = None

    eyes = Eyes()
    show_clock_until = 0

    # interaction tracking
    last_interaction_s = time.time()
    wake_flash_until_ms = 0

    while True:
        now_s = time.time()
        now_ms = time.ticks_ms()

        # Interaction: tilt
        if tilt_event():
            last_interaction_s = now_s
            wake_flash_until_ms = time.ticks_add(now_ms, SLEEP_WAKE_FLASH_MS)
            show_clock_until = now_s + SHOW_CLOCK_SECONDS_AFTER_TILT

        # WiFi maintenance
        if not wlan.isconnected():
            wifi_ok = False
            if now_s - last_wifi_try > WIFI_TRY_PERIOD_S:
                last_wifi_try = now_s
                print("WiFi retry...")
                if wifi_try_connect(wlan, WIFI_SSID, WIFI_PASS, timeout_s=8):
                    wifi_ok = True
                    print("WiFi OK:", wlan.ifconfig())
                    sync_time()
                    last_ntp = now_s
        else:
            wifi_ok = True

        # NTP refresh (only if online)
        if wifi_ok and (now_s - last_ntp > NTP_RESYNC_PERIOD_S):
            sync_time()
            last_ntp = now_s

        # Weather refresh (only if online)
        if wifi_ok and (now_s - last_weather > WEATHER_PERIOD_S):
            try:
                out_temp, wcode = fetch_outside_weather(LAT, LON)
                wgroup = weather_group(wcode)
                last_weather = now_s
                print("OUT:", out_temp, "C group:", wgroup)
            except Exception as e:
                print("Weather fetch failed:", repr(e))

        # DHT read
        in_t, in_h = read_dht(in_t, in_h)

        # Render
        if now_s <= show_clock_until:
            draw_clock_screen(oled, wifi_ok, out_temp, wgroup, in_t, in_h)
            time.sleep(0.15)
        else:
            idle_s = now_s - last_interaction_s
            sleepy = (idle_s >= SLEEP_AFTER_S)
            asleep = (idle_s >= SLEEP_BLINK_AFTER_S)

            # quick wake flash: eyes open wider briefly after tilt
            waking = (time.ticks_diff(now_ms, wake_flash_until_ms) < 0)

            blink_amt, squint = eyes.step(sleepy=sleepy, asleep=asleep)
            # if waking, override to fully open for a moment
            if waking:
                blink_amt = 0.0
                squint = False
                sleepy = False
                asleep = False

            eyes.draw(oled, blink_amt, squint, sleepy=sleepy, asleep=asleep)
            time.sleep(0.03)


main()
