from machine import Pin, I2C, PWM
import ssd1306
import time
import math
import sys

# OLED setup
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Buttons
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)
btn_enc = Pin(27, Pin.IN, Pin.PULL_UP)

# Encoder pins
enc_clk = Pin(21, Pin.IN, Pin.PULL_UP)
enc_dt = Pin(22, Pin.IN, Pin.PULL_UP)
last_clk_val = enc_clk.value()

# Buzzer
buzzer = PWM(Pin(25), freq=1000, duty=0)

def buzz(freq, duration=100):
    buzzer.freq(freq)
    buzzer.duty(200)
    time.sleep_ms(duration)
    buzzer.duty(0)

def jingle():
    for f in [880, 988, 1047, 880]:
        buzz(f, 100)
        time.sleep_ms(50)

# Levels
levels = [
    {'hole': (100, 30), 'obstacles': []},
    {'hole': (110, 50), 'obstacles': [(60, 20, 5, 30)]},
    {'hole': (10, 10), 'obstacles': [(40, 0, 10, 50), (80, 30, 10, 30)]},
]

# State
level_idx = 0
mode = 'angle'
ball_x = 10
ball_y = 30
vx = vy = 0
angle = 0
power = 0

def draw_level():
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1)
    hx, hy = levels[level_idx]['hole']
    oled.fill_rect(hx - 2, hy - 2, 5, 5, 1)
    for ox, oy, ow, oh in levels[level_idx]['obstacles']:
        oled.fill_rect(ox, oy, ow, oh, 1)
    oled.fill_rect(int(ball_x), int(ball_y), 3, 3, 1)

    if mode == 'angle':
        offset = 5
        length = 10
        rad = math.radians(angle)
        sx = int(ball_x + offset * math.cos(rad))
        sy = int(ball_y + offset * math.sin(rad))
        ex = int(ball_x + (offset + length) * math.cos(rad))
        ey = int(ball_y + (offset + length) * math.sin(rad))
        oled.line(sx + 1, sy + 1, ex, ey, 1)

    if mode == 'power':
        oled.rect(40, 54, 50, 7, 1)
        oled.fill_rect(40, 54, min(power * 5, 50), 7, 1)

    oled.show()

def handle_buttons():
    global mode, angle, power, vx, vy, ball_x, ball_y, level_idx, last_clk_val

    # Exit on long press
    if not btn_left.value() and not btn_enc.value():
        t0 = time.ticks_ms()
        while not btn_left.value() and not btn_enc.value():
            if time.ticks_diff(time.ticks_ms(), t0) > 1000:
                import main
                sys.modules.clear()
                main.main()
                return

    # Encoder rotation for angle
    clk_now = enc_clk.value()
    if mode == 'angle' and last_clk_val == 1 and clk_now == 0:
        if enc_dt.value() == 1:
            angle = (angle + 5) % 360
        else:
            angle = (angle - 5) % 360
    last_clk_val = clk_now

    # Button input
    if mode == 'angle' and not btn_enc.value():
        mode = 'power'
        time.sleep_ms(200)
    elif mode == 'power' and not btn_enc.value():
        power = (power + 1) % 11
        time.sleep_ms(200)
    elif mode == 'power' and not btn_left.value():
        rad = math.radians(angle)
        vx = math.cos(rad) * power
        vy = math.sin(rad) * power
        mode = 'fly'
        time.sleep_ms(200)

def check_collision(ox, oy, ow, oh):
    global vx, vy, ball_x, ball_y
    if ox <= ball_x <= ox + ow and oy <= ball_y <= oy + oh:
        dx = min(abs(ball_x - ox), abs(ball_x - (ox + ow)))
        dy = min(abs(ball_y - oy), abs(ball_y - (oy + oh)))
        if dx < dy:
            vx *= -1
        else:
            vy *= -1
        buzz(400, 50)
        return True
    return False

def update_ball():
    global ball_x, ball_y, vx, vy, level_idx, mode
    ball_x += vx
    ball_y += vy
    vx *= 0.95
    vy *= 0.95

    if ball_x < 1 or ball_x > 124:
        vx *= -1
        ball_x = max(1, min(ball_x, 124))
        buzz(300, 50)
    if ball_y < 1 or ball_y > 61:
        vy *= -1
        ball_y = max(1, min(ball_y, 61))
        buzz(300, 50)

    for ox, oy, ow, oh in levels[level_idx]['obstacles']:
        check_collision(ox, oy, ow, oh)

    if abs(vx) < 0.1 and abs(vy) < 0.1:
        vx = vy = 0
        mode = 'angle'

    hx, hy = levels[level_idx]['hole']
    if abs(ball_x - hx) < 4 and abs(ball_y - hy) < 4:
        celebrate()
        level_idx = (level_idx + 1) % len(levels)
        reset_ball()

def celebrate():
    jingle()
    for r in range(0, 30, 5):
        oled.fill(0)
        oled.rect(0, 0, 128, 64, 1)
        for i in range(0, 360, 45):
            x = int(64 + r * math.cos(math.radians(i)))
            y = int(32 + r * math.sin(math.radians(i)))
            oled.pixel(x, y, 1)
        oled.show()
        time.sleep_ms(100)
    oled.fill(0)
    oled.text("Great shot!", 20, 28)
    oled.show()
    time.sleep_ms(800)

def reset_ball():
    global ball_x, ball_y, vx, vy, angle, power, mode
    ball_x, ball_y = 10, 30
    vx = vy = 0
    angle = 0
    power = 0
    mode = 'angle'

# Main loop
reset_ball()
while True:
    handle_buttons()
    if mode == 'fly':
        update_ball()
    draw_level()
    time.sleep_ms(50)
