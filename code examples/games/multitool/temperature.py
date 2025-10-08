# temperature.py — Temperature & Humidity (DHT11 on GPIO15)
# UI refresh ~10 Hz (smooth), sensor read 1 Hz (DHT11 limit). Long-press = back.

import time
from machine import Pin
import dht
from ssd1306 import SSD1306_I2C

DHT_PIN = 15
BTN_PIN = 4

OLED_W = 128
OLED_H = 64
LONG_PRESS_S = 1.5
UI_PERIOD_MS = 100     # 10 Hz UI redraw
DHT_PERIOD_MS = 1000   # ~1 Hz sensor read (DHT11 limit)

def run(shared_i2c):
    oled = SSD1306_I2C(OLED_W, OLED_H, shared_i2c)
    sensor = dht.DHT11(Pin(DHT_PIN, Pin.IN, Pin.PULL_UP))
    btn = Pin(BTN_PIN, Pin.IN)

    _splash(oled, "Temp/Humidity")

    btn_idle = btn.value(); in_press = False; t0 = 0
    next_ui  = time.ticks_add(time.ticks_ms(), UI_PERIOD_MS)
    next_dht = time.ticks_add(time.ticks_ms(), DHT_PERIOD_MS)
    tick = 0  # heartbeat

    t = None; h = None

    while True:
        now = time.ticks_ms()

        # exit on long press
        v = btn.value()
        if not in_press:
            if v != btn_idle: in_press = True; t0 = now
        else:
            if v == btn_idle:
                held = time.ticks_diff(now, t0); in_press = False
                if held >= int(LONG_PRESS_S*1000): _goodbye(oled); return

        # read DHT at 1 Hz
        if time.ticks_diff(now, next_dht) >= 0:
            next_dht = time.ticks_add(now, DHT_PERIOD_MS)
            try:
                sensor.measure()
                t = sensor.temperature()
                h = sensor.humidity()
            except:
                pass

        # redraw UI at 10 Hz
        if time.ticks_diff(now, next_ui) >= 0:
            next_ui = time.ticks_add(now, UI_PERIOD_MS)
            tick ^= 1
            _draw(oled, t, h, tick)

        time.sleep_ms(2)

def _draw(oled, t, h, beat):
    oled.fill(0)
    # tiny heartbeat pixel so UI feels alive between 1 Hz updates
    if beat: oled.fill_rect(0,0,2,2,1)
    oled.text("Temp/Humidity", 8, 0)
    if t is None or h is None:
        oled.text("--.- C", 20, 24); oled.text("-- %", 24, 40)
    else:
        oled.text("T:", 8, 24);  oled.text("{:>4.1f} C".format(t), 28, 24)
        oled.text("H:", 8, 40);  oled.text("{:>3.0f} %".format(h), 28, 40)
    oled.show()

def _splash(oled, title):
    oled.fill(0); oled.text(title, 16, 16); oled.text("Starting...", 24, 34); oled.show()
    time.sleep_ms(200)

def _goodbye(oled):
    oled.fill(0); oled.text("Back to menu", 8, 26); oled.show()
    time.sleep_ms(180)
