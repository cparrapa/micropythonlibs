# game5.py – Tap Duel with split-screen visual scoreboard

from machine import Pin, I2C
import ssd1306
import time

# OLED init
i2c = I2C(scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Buttons
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

def wait_release():
    while btn_left.value() == 0 or btn_right.value() == 0:
        time.sleep_ms(10)

def wait_ms(ms):
    t0 = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), t0) < ms:
        if check_exit(): return True
        time.sleep_ms(10)
    return False

def check_exit():
    if btn_left.value() == 0 and btn_right.value() == 0:
        start = time.ticks_ms()
        while btn_left.value() == 0 and btn_right.value() == 0:
            if time.ticks_diff(time.ticks_ms(), start) > 1000:
                import main
                main.main()
                return True
            time.sleep_ms(10)
    return False

# Draw split UI with counts
def draw_split_ui(p1, p2):
    oled.fill(0)

    # Right half = white background
    oled.fill_rect(64, 0, 64, 64, 1)

    # Player 1 (left) score in white-on-black
    p1_text = str(p1)
    x1 = 32 - len(p1_text) * 8 // 2
    oled.text(p1_text, x1, 28, 1)

    # Player 2 (right) score in black-on-white
    p2_text = str(p2)
    x2 = 64 + (32 - len(p2_text) * 8 // 2)
    oled.text(p2_text, x2, 28, 0)

    oled.show()

# Game loop
while True:
    wait_release()
    if wait_ms(500): break

    oled.fill(0)
    oled.text("Tap Duel!", 28, 20)
    oled.text("Get Ready...", 20, 40)
    oled.show()
    if wait_ms(2000): break

    p1_count = 0
    p2_count = 0
    last_left = 1
    last_right = 1

    oled.fill(0)
    oled.text("GO!", 52, 28)
    oled.show()
    if wait_ms(500): break

    duration = 5000
    start = time.ticks_ms()
    last_ui_update = time.ticks_ms()

    while time.ticks_diff(time.ticks_ms(), start) < duration:
        if check_exit(): break

        l = btn_left.value()
        r = btn_right.value()

        if last_left == 1 and l == 0:
            p1_count += 1
        if last_right == 1 and r == 0:
            p2_count += 1

        last_left = l
        last_right = r

        if time.ticks_diff(time.ticks_ms(), last_ui_update) > 100:
            draw_split_ui(p1_count, p2_count)
            last_ui_update = time.ticks_ms()

        time.sleep_ms(5)

    # Final screen
    draw_split_ui(p1_count, p2_count)
    oled.text("END", 54, 0, 0)
    if p1_count > p2_count:
        oled.text("P1 Wins", 5, 54, 1)
    elif p2_count > p1_count:
        oled.text("P2 Wins", 70, 54, 0)
    else:
        oled.text("TIE", 58, 54, 0)
    oled.show()

    if wait_ms(4000): break
