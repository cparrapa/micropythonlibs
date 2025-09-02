import time
from machine import Pin, ADC, PWM, I2C
import framebuf
import network, espnow

# ======== PIN MAP ========
PINS = {
    "BTN_ABCD": 0,     # Button pad A/B/C/D (analog ladder)
    "BTN_L": 8,
    "BTN_R": 10,
    "BUZZER": 6,
    "JOY_Y": 3,
    "JOY_X": 1,
    "JOY_PRESS": 2,
    "I2C_SDA": 4,
    "I2C_SCL": 5,
}

# ======== Joystick Calibration ========
JOY_X_LEFT   = 1100
JOY_X_CENTER = 2300
JOY_X_RIGHT  = 3600

JOY_Y_DOWN   = 380
JOY_Y_CENTER = 2320
JOY_Y_UP     = 2500

DEADZONE = 0.1  # ignore small jitter near center

def norm_axis(val, low, center, high):
    if val < center:   # left/down
        n = (val - center) / (center - low)
    else:              # right/up
        n = (val - center) / (high - center)
    # clamp
    if n < -1: n = -1
    if n > 1:  n = 1
    # deadzone
    if abs(n) < DEADZONE:
        n = 0
    return round(n, 2)

# ======== OLED Driver ========
class SSD1306:
    def __init__(self, w, h, i2c, addr=0x3C):
        self.w = w
        self.h = h
        self.i2c = i2c
        self.addr = addr
        self.buffer = bytearray((h // 8) * w)
        self.fb = framebuf.FrameBuffer(self.buffer, w, h, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        for cmd in (
            0xAE, 0x20, 0x00, 0xB0, 0xC8, 0x00, 0x10, 0x40, 0x81, 0xFF,
            0xA1, 0xA6, 0xA8, self.h - 1, 0xA4, 0xD3, 0x00, 0xD5, 0xF0,
            0xD9, 0x22, 0xDA, 0x02, 0xDB, 0x20, 0x8D, 0x14, 0xAF
        ):
            self.cmd(cmd)
        self.fill(0)
        self.show()

    def cmd(self, c):
        self.i2c.writeto(self.addr, b'\x00' + bytes([c]))

    def fill(self, c):
        self.fb.fill(c)

    def text(self, s, x, y):
        self.fb.text(s, x, y, 1)

    def show(self):
        self.i2c.writeto(self.addr, b'\x40' + self.buffer)

# ======== Init hardware ========
def safe_pin(n, mode, pull=None):
    try:
        if pull:
            return Pin(n, mode, pull)
        else:
            return Pin(n, mode)
    except ValueError:
        print("Pin", n, "invalid on ESP32-C3")
        return None

btn_l = safe_pin(PINS["BTN_L"], Pin.IN, Pin.PULL_UP)
btn_r = safe_pin(PINS["BTN_R"], Pin.IN, Pin.PULL_UP)
joy_press = safe_pin(PINS["JOY_PRESS"], Pin.IN, Pin.PULL_UP)

pad_adc = ADC(Pin(PINS["BTN_ABCD"]))
pad_adc.atten(ADC.ATTN_11DB)

adc_x = ADC(Pin(PINS["JOY_X"]))
adc_y = ADC(Pin(PINS["JOY_Y"]))
adc_x.atten(ADC.ATTN_11DB)
adc_y.atten(ADC.ATTN_11DB)

buzzer = PWM(Pin(PINS["BUZZER"]))
buzzer.duty(0)

i2c = I2C(0, sda=Pin(PINS["I2C_SDA"]), scl=Pin(PINS["I2C_SCL"]))
oled = SSD1306(128, 32, i2c)

# ======== Buttons ========
def read_pad():
    val = pad_adc.read()
    if 2200 < val < 2400:
        return "A"
    elif 10 < val < 50:
        return "B"
    elif 3100 < val < 3250:
        return "C"
    elif 700 < val < 900:
        return "D"
    else:
        return None

def beep():
    buzzer.freq(2000)
    buzzer.duty(200)
    time.sleep_ms(40)
    buzzer.duty(0)

# ======== ESP-NOW Setup ========
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

esp = espnow.ESPNow()
esp.active(True)

# 👇 Replace with your receiver’s MAC
peer = b'\xfc\xb4g}\xb4\x8c'
esp.add_peer(peer)

# ======== Main loop ========
while True:
    raw_x = adc_x.read()
    raw_y = adc_y.read()
    x = norm_axis(raw_x, JOY_X_LEFT, JOY_X_CENTER, JOY_X_RIGHT)
    y = norm_axis(raw_y, JOY_Y_DOWN, JOY_Y_CENTER, JOY_Y_UP)

    buttons = []
    pad_btn = read_pad()
    if pad_btn:
        buttons.append(pad_btn)
    if btn_l and btn_l.value() == 0:
        buttons.append("L")
    if btn_r and btn_r.value() == 0:
        buttons.append("R")
    if joy_press and joy_press.value() == 0:
        buttons.append("JP")

    # package data: x,y,buttons
    msg = "{};{};{}".format(x, y, ",".join(buttons))
    esp.send(peer, msg)

    # display
    oled.fill(0)
    oled.text("X:{:.2f}".format(x), 0, 0)
    oled.text("Y:{:.2f}".format(y), 0, 10)
    oled.text("Btn:{}".format(",".join(buttons)), 0, 20)
    oled.show()

    if buttons:
        beep()

    time.sleep_ms(100)
