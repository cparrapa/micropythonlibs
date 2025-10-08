# light.py — Light level (ADC GPIO33), fast UI (~10 Hz), long-press = back

import time
from machine import Pin, ADC
from ssd1306 import SSD1306_I2C

LIGHT_ADC_PIN = 33
BTN_PIN = 4

OLED_W = 128
OLED_H = 64
LONG_PRESS_S = 1.5
PERIOD_MS = 100  # 10 Hz

def run(shared_i2c):
    oled = SSD1306_I2C(OLED_W, OLED_H, shared_i2c)
    adc = ADC(Pin(LIGHT_ADC_PIN))
    adc.atten(ADC.ATTN_11DB); adc.width(ADC.WIDTH_12BIT)
    btn = Pin(BTN_PIN, Pin.IN)

    _splash(oled, "Light level")

    btn_idle = btn.value(); in_press = False; t0 = 0
    next_t = time.ticks_add(time.ticks_ms(), PERIOD_MS)
    pct = 0

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
            pct = _read_light_pct(adc)
            _draw(oled, pct)

        time.sleep_ms(2)

def _read_light_pct(adc, samples=5):
    vals = []
    for _ in range(samples):
        vals.append(adc.read())
    vals.sort()
    v = vals[len(vals)//2]            # median
    return max(0, min(100, int((v / 4095) * 100)))

def _draw(oled, pct):
    oled.fill(0)
    oled.text("Light", 44, 0)
    s = "{:>3d}%".format(pct)
    oled.text(s, max(0,(OLED_W-len(s)*8)//2), 22)
    _bar(oled, 16, 42, 96, 12, pct)
    oled.show()

def _bar(oled, x, y, w, h, pct):
    oled.rect(x, y, w, h, 1)
    fw = int((w-2) * pct / 100)
    if fw > 0: oled.fill_rect(x+1, y+1, fw, h-2, 1)

def _splash(oled, title):
    oled.fill(0); oled.text(title, 24, 16); oled.text("Starting...", 24, 34); oled.show()
    time.sleep_ms(180)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 8, 26); oled.show()
    time.sleep_ms(160)
