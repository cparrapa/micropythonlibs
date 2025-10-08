# game1.py — Snake with two-button control (left/right + long-hold both to exit)
# Controls:
#   - LEFT button (GPIO14): turn left
#   - RIGHT button (encoder button, default GPIO4): turn right
#   - Hold BOTH buttons >= 1000 ms: exit back to menu
#
# Plug-in signature: run(shared_i2c) and return to exit.

import time, urandom
from machine import Pin
from ssd1306 import SSD1306_I2C

# ---- Pins (adjust if needed) ----
LEFT_BTN_PIN  = 4     # left turn button (active-low, pull-up)
RIGHT_BTN_PIN = 27      # encoder push button; set to 27 if yours is on GPIO27

# ---- OLED ----
W, H = 128, 64

# ---- Grid/layout ----
CELL    = 10
GRID_Y0 = 10                        # top bar for score
MAX_COL = 12                        # 12*10 = 120 px
MAX_ROW = (H - GRID_Y0) // CELL     # 54//10 = 5 rows

# ---- Directions ----
DIR_UP, DIR_RIGHT, DIR_DOWN, DIR_LEFT = 0, 1, 2, 3

# ---- Timing / debounce ----
TURN_DEBOUNCE_MS = 120
EXIT_HOLD_MS     = 1000
STEP_MS_START    = 300
STEP_MS_MIN      = 120
SPEEDUP_PER_APPLE = 10  # ms faster per apple

# --- safe OLED show (retry to avoid I2C ETIMEDOUT) ---
def _safe_show(oled, retries=3, delay_ms=4):
    for _ in range(retries):
        try:
            oled.show()
            return True
        except OSError:
            time.sleep_ms(delay_ms)
    try:
        oled.show()
        return True
    except OSError:
        return False

def run(shared_i2c):
    oled = SSD1306_I2C(W, H, shared_i2c)

    # ---- Inputs ----
    btnL = Pin(LEFT_BTN_PIN,  Pin.IN, Pin.PULL_UP)
    btnR = Pin(RIGHT_BTN_PIN, Pin.IN, Pin.PULL_UP)

    # Edge tracking
    prevL = btnL.value()   # 1=idle, 0=pressed
    prevR = btnR.value()
    last_turn_t = 0
    both_hold_t = None

    # ---- Game state ----
    direction = DIR_RIGHT
    snake = [(MAX_COL // 2, MAX_ROW // 2)]
    score = 0
    apple = _place_apple(snake)
    step_ms = STEP_MS_START
    last_step = time.ticks_ms()

    _draw(oled, snake, apple, score)

    while True:
        now = time.ticks_ms()

        # ----- Buttons: edges + long-hold-both exit -----
        curL = btnL.value()
        curR = btnR.value()

        # Detect "both held" for exit
        if curL == 0 and curR == 0:
            if both_hold_t is None:
                both_hold_t = now
            elif time.ticks_diff(now, both_hold_t) >= EXIT_HOLD_MS:
                _bye(oled)
                return
        else:
            both_hold_t = None

        # Turn left on falling edge of LEFT (debounced)
        if prevL == 1 and curL == 0:
            if time.ticks_diff(now, last_turn_t) >= TURN_DEBOUNCE_MS:
                direction = (direction - 1) % 4
                last_turn_t = now

        # Turn right on falling edge of RIGHT (debounced)
        if prevR == 1 and curR == 0:
            if time.ticks_diff(now, last_turn_t) >= TURN_DEBOUNCE_MS:
                direction = (direction + 1) % 4
                last_turn_t = now

        prevL, prevR = curL, curR

        # ----- Tick / movement -----
        if time.ticks_diff(now, last_step) >= step_ms:
            last_step = now
            head_x, head_y = snake[0]
            if   direction == DIR_UP:    head_y = (head_y - 1) % MAX_ROW
            elif direction == DIR_DOWN:  head_y = (head_y + 1) % MAX_ROW
            elif direction == DIR_LEFT:  head_x = (head_x - 1) % MAX_COL
            else:                        head_x = (head_x + 1) % MAX_COL

            new_head = (head_x, head_y)

            # Self collision -> game over
            if new_head in snake:
                _game_over(oled, score)
                return

            snake.insert(0, new_head)

            if new_head == apple:
                score += 1
                apple = _place_apple(snake)
                step_ms = max(STEP_MS_MIN, STEP_MS_START - score * SPEEDUP_PER_APPLE)
            else:
                snake.pop()

            _draw(oled, snake, apple, score)

        time.sleep_ms(2)

# ---------- helpers ----------
def _rand(n):
    # uniform 0..n-1 using 8/16-bit entropy
    return urandom.getrandbits(16) % n

def _place_apple(snake):
    while True:
        x = _rand(MAX_COL)
        y = _rand(MAX_ROW)
        if (x, y) not in snake:
            return (x, y)

def _draw(oled, snake, apple, score):
    oled.fill(0)
    # Score bar
    oled.text("Score: {}".format(score), 0, 0)
    # Apple (hollow square)
    ax, ay = apple
    oled.rect(ax * CELL, GRID_Y0 + ay * CELL, CELL - 1, CELL - 1, 1)
    # Snake (filled squares)
    for (x, y) in snake:
        oled.fill_rect(x * CELL, GRID_Y0 + y * CELL, CELL - 1, CELL - 1, 1)
    _safe_show(oled)

def _game_over(oled, score):
    oled.fill(0)
    oled.text("GAME OVER", 22, 20)
    oled.text("Score: {}".format(score), 18, 36)
    _safe_show(oled)
    time.sleep_ms(1200)

def _bye(oled):
    oled.fill(0)
    oled.text("Exit to menu", 16, 26)
    _safe_show(oled)
    time.sleep_ms(220)
