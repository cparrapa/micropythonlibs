# game1.py - Snake game with left/right turn buttons and long-press exit

from machine import Pin, I2C
import ssd1306
import time
import random

# OLED setup
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Controls
left_btn = Pin(14, Pin.IN, Pin.PULL_UP)      # Left button
enc_btn = Pin(27, Pin.IN, Pin.PULL_UP)       # Encoder button

# Constants
CELL = 10
MAX_COL = 12
MAX_ROW = 6

# Directions
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3
direction = DIR_RIGHT

snake = [(MAX_COL // 2, MAX_ROW // 2)]
apple = None
score = 0

def place_apple():
    global apple
    while True:
        x = random.getrandbits(4) % MAX_COL
        y = random.getrandbits(4) % MAX_ROW
        if (x, y) not in snake:
            apple = (x, y)
            return

def draw():
    oled.fill(0)
    for x, y in snake:
        oled.fill_rect(x * CELL, y * CELL, CELL - 1, CELL - 1, 1)
    if apple:
        oled.rect(apple[0] * CELL, apple[1] * CELL, CELL - 1, CELL - 1, 1)
    oled.text("Score: {}".format(score), 0, 0)
    oled.show()

def move():
    head = snake[0]
    if direction == DIR_UP:
        return (head[0], (head[1] - 1) % MAX_ROW)
    elif direction == DIR_DOWN:
        return (head[0], (head[1] + 1) % MAX_ROW)
    elif direction == DIR_LEFT:
        return ((head[0] - 1) % MAX_COL, head[1])
    else:
        return ((head[0] + 1) % MAX_COL, head[1])

# Game start
place_apple()
last_move = time.ticks_ms()
exit_start = None

while True:
    # Button input for turning
    if not left_btn.value():
        direction = (direction - 1) % 4
        time.sleep_ms(150)

    if not enc_btn.value():
        direction = (direction + 1) % 4
        time.sleep_ms(150)

    # Detect long press of both buttons
    if not left_btn.value() and not enc_btn.value():
        if exit_start is None:
            exit_start = time.ticks_ms()
        elif time.ticks_diff(time.ticks_ms(), exit_start) > 1000:
            import main
            main.main()  # assuming main.py has a main() function
    else:
        exit_start = None

    # Move snake
    now = time.ticks_ms()
    if time.ticks_diff(now, last_move) > 300:
        last_move = now
        new_head = move()
        if new_head in snake:
            break
        snake.insert(0, new_head)
        if new_head == apple:
            score += 1
            place_apple()
        else:
            snake.pop()
        draw()

# Game over or exit
oled.fill(0)
oled.text("GAME OVER", 20, 20)
oled.text("Score: {}".format(score), 20, 36)
oled.show()
time.sleep(2)
