# game6.py – Dodge Dots with splash, score, and increasing difficulty

from machine import Pin, I2C
import ssd1306
import time
import random

# OLED display
i2c = I2C(scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Button setup
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# Grid config
COLS = 16
ROWS = 8
BLOCK = 8

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

def wait_release():
    while btn_left.value() == 0 or btn_right.value() == 0:
        time.sleep_ms(10)

def wait_for_start():
    oled.fill(0)
    oled.text("DODGE DOTS", 20, 20)
    oled.text("Press to start", 10, 40)
    oled.show()
    while btn_left.value() == 1 and btn_right.value() == 1:
        time.sleep_ms(10)

# Game loop
while True:
    wait_release()
    wait_for_start()
    wait_release()

    player_x = COLS // 2
    enemies = []
    score = 0
    tick = 0

    while True:
        if check_exit(): break

        # Move player
        if btn_left.value() == 0 and player_x > 0:
            player_x -= 1
            wait_release()
        elif btn_right.value() == 0 and player_x < COLS - 1:
            player_x += 1
            wait_release()

        # Move enemies
        enemies = [(x, y + 1) for (x, y) in enemies if y + 1 < ROWS]

        # Spawn enemies
        if tick % 5 == 0:
            enemies.append((random.randint(0, COLS - 1), 0))

        # Collision detection
        if any(x == player_x and y == ROWS - 1 for (x, y) in enemies):
            oled.fill(0)
            oled.text("GAME OVER", 28, 20)
            oled.text("Score: {}".format(score), 20, 40)
            oled.show()
            time.sleep(3000)
            break

        # Draw frame
        oled.fill(0)
        oled.text(str(score), 0, 0)

        for (x, y) in enemies:
            oled.fill_rect(x * BLOCK, y * BLOCK, BLOCK - 1, BLOCK - 1, 1)

        oled.rect(player_x * BLOCK, (ROWS - 1) * BLOCK, BLOCK - 1, BLOCK - 1, 1)

        oled.show()
        tick += 1
        score += 1

        # Calculate delay: start at 80ms, down to 30ms
        delay = max(30, 80 - (score // 50) * 10)
        time.sleep_ms(delay)
