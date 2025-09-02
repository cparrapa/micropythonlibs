import time
from machine import Pin, ADC, PWM, I2C
import framebuf

# ======== PIN MAP ========
PINS = {
    "BTN_ABCD": 0,     # Button pad A/B/C/D (analog resistor ladder)
    "BTN_L": 8,
    "BTN_R": 10,
    "BUZZER": 6,
    "VIBE": 7,
    "JOY_Y": 3,        # Joystick Y axis (ADC)
    "JOY_X": 1,        # Joystick X axis (ADC)
    "JOY_PRESS": 2,    # Joystick push button
    "I2C_SDA": 4,      # OLED SDA
    "I2C_SCL": 5,      # OLED SCL
}

# ======== Joystick Calibration Values ========
# Adjust these by reading raw ADC values when centered and at extremes
JOY_X_CENTER = 2200
JOY_Y_CENTER = 2200
JOY_X_RANGE = 1200  # distance from center to extreme
JOY_Y_RANGE = 1800

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

vibe_pwm = PWM(Pin(PINS["VIBE"]))
vibe_pwm.freq(200)
vibe_pwm.duty(0)

i2c = I2C(0, sda=Pin(PINS["I2C_SDA"]), scl=Pin(PINS["I2C_SCL"]))
oled = SSD1306(128, 32, i2c)

# ======== Helpers ========
def norm(v, center, rng):
    return round((v - center) / rng, 2)

def read_pad():
    val = pad_adc.read()
    if val > 2200 and val < 2400:
        return "A"
    elif val > 10 and val < 50:
        return "B"
    elif val > 3100 and val < 3250:
        return "C"
    elif val > 700 and val < 900:
        return "D"
    else:
        return None

def beep():
    buzzer.freq(2000)
    buzzer.duty(200)
    time.sleep_ms(50)
    buzzer.duty(0)

def vibrate():
    vibe_pwm.duty(800)  # stronger vibration
    time.sleep_ms(50)
    vibe_pwm.duty(0)

# ======== Main loop ========
while True:
    x = norm(adc_x.read(), JOY_X_CENTER, JOY_X_RANGE)
    y = norm(adc_y.read(), JOY_Y_CENTER, JOY_Y_RANGE)

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

    oled.fill(0)
    oled.text("X: {}".format(x), 0, 0)
    oled.text("Y: {}".format(y), 0, 10)
    oled.text("Btn:{}".format(",".join(buttons)), 0, 20)
    oled.show()
    time.sleep_ms(100)
    
    if buttons:
        beep()
        vibrate()