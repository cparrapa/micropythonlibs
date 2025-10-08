# sound.py — Noise level (analog mic on GPIO27), ~10 Hz UI, long-press = back
# (RMS over 128 samples for responsiveness; not calibrated SPL)

import time, math
from machine import Pin, ADC
from ssd1306 import SSD1306_I2C

MIC_ADC_PIN = 27
BTN_PIN = 4

OLED_W = 128
OLED_H = 64
LONG_PRESS_S = 1.5
PERIOD_MS = 100  # 10 Hz

def run(shared_i2c):
    oled = SSD1306_I2C(OLED_W, OLED_H, shared_i2c)
    adc = ADC(Pin(MIC_ADC_PIN))
    adc.atten(ADC.ATTN_11DB); adc.width(ADC.WIDTH_12BIT)
    btn = Pin(BTN_PIN, Pin.IN)

    _splash(oled, "Noise")

    btn_idle = btn.value(); in_press = False; t0 = 0
    next_t = time.ticks_add(time.ticks_ms(), PERIOD_MS)
    db = 0.0; pct = 0

    while True:
        v = btn.value(); now = time.ticks_ms()
        if not in_press:
            if v != btn_idle: in_press = True; t0 = now
        else:
            if v == btn_idle:
                held = time.ticks_diff(now, t0); in_press = False
                if held >= int(LONG_PRESS_S*1000): _goodbye(oled); return

        if time.ticks_diff(now, next_t) >= 0:
            next_t = time.ticks_add(now, PERIOD_MS)
            db, pct = _mic_level(adc, 128)   # lighter window for snappier updates
            _draw(oled, db, pct)

        time.sleep_ms(2)

def _mic_level(adc, samples=128):
    s = 0; s2 = 0
    for _ in range(samples):
        x = adc.read()
        s += x; s2 += x*x
    mean = s / samples
    var = max(1, (s2 / samples) - (mean * mean))
    rms = math.sqrt(var)
    norm = min(1.0, rms / 2048.0)
    db = 20 * math.log10(norm + 1e-6) + 60
    pct = max(0, min(100, int(norm * 100)))
    return db, pct

def _draw(oled, db, pct):
    oled.fill(0)
    oled.text("Noise", 44, 0)
    s = "{:>3.0f} dB".format(db)
    oled.text(s, max(0,(OLED_W-len(s)*8)//2), 22)
    _bar(oled, 16, 42, 96, 12, pct)
    oled.show()

def _bar(oled, x, y, w, h, pct):
    oled.rect(x, y, w, h, 1)
    fw = int((w-2) * pct / 100)
    if fw > 0: oled.fill_rect(x+1, y+1, fw, h-2, 1)

def _splash(oled, title):
    oled.fill(0); oled.text(title, 40, 16); oled.text("Starting...", 24, 34); oled.show()
    time.sleep_ms(180)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 8, 26); oled.show()
    time.sleep_ms(160)
