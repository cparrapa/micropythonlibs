from machine import Pin, I2C, Timer, PWM
import ssd1306
import random
import time

# === OLED Display Setup ===
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === Buttons & Buzzer ===
btn_a = Pin(14, Pin.IN, Pin.PULL_UP)
btn_b = Pin(27, Pin.IN, Pin.PULL_UP)
buzzer = PWM(Pin(25))
buzzer.duty(0)  # Off initially

# === Game Constants ===
WIDTH = 128
HEIGHT = 64
GRID = 4
GRID_W = WIDTH // GRID
GRID_H = HEIGHT // GRID

# === Directions: (dx, dy) ===
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]  # Clockwise

# === Game Variables ===
snake = [(10, 10)]
direction_idx = 1  # Starts going RIGHT
food = (5, 5)
boosts = []
score = 0
level = 1
speed = 200  # in ms

# === Timers ===
game_timer = Timer(0)
button_timer = Timer(1)
btn_hold_time = 0

def buzz(freq=1000, duration=100):
    buzzer.freq(freq)
    buzzer.duty(512)
    time.sleep_ms(duration)
    buzzer.duty(0)

def draw():
    oled.fill(0)
    for segment in snake:
        oled.fill_rect(segment[0]*GRID, segment[1]*GRID, GRID, GRID, 1)
    oled.fill_rect(food[0]*GRID, food[1]*GRID, GRID, GRID, 1)
    for bx, by in boosts:
        oled.rect(bx*GRID, by*GRID, GRID, GRID, 1)
    oled.text(f"S:{score} L:{level}", 0, 0)
    oled.show()

def place_item(exclude):
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(1, GRID_H - 1))
        if pos not in exclude:
            return pos

def restart_game(t=None):
    global snake, direction_idx, food, boosts, score, level, speed
    snake = [(10, 10)]
    direction_idx = 1
    food = place_item(snake)
    boosts = []
    score = 0
    level = 1
    speed = 200
    draw()
    game_timer.init(period=speed, mode=Timer.PERIODIC, callback=update)

def check_buttons(t):
    global direction_idx, btn_hold_time

    # Button turn logic
    if not btn_a.value() and btn_b.value():
        direction_idx = (direction_idx - 1) % 4
        time.sleep_ms(150)
    elif not btn_b.value() and btn_a.value():
        direction_idx = (direction_idx + 1) % 4
        time.sleep_ms(150)

    # Button hold detection for reset
    if not btn_a.value() and not btn_b.value():
        btn_hold_time += 100
        if btn_hold_time >= 2000:
            buzz(200, 300)
            restart_game()
            btn_hold_time = 0
    else:
        btn_hold_time = 0

def update(t):
    global snake, food, boosts, score, level, speed

    dx, dy = DIRECTIONS[direction_idx]
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    # Wrap around screen edges
    new_head = (new_head[0] % GRID_W, new_head[1] % GRID_H)
    if new_head[1] == 0:
        new_head = (new_head[0], 1)  # Avoid drawing on score row

    # Self-collision detection only
    if new_head in snake:
        oled.fill(0)
        oled.text("Game Over", 30, 25)
        oled.text(f"Score:{score}", 30, 40)
        oled.show()
        buzz(100, 500)
        game_timer.deinit()
        return


    snake.insert(0, new_head)

    # Food eaten
    if new_head == food:
        score += 1
        buzz(1500, 100)
        food = place_item(snake + boosts)
        if score % 5 == 0:
            level += 1
            speed = max(50, speed - 20)
            game_timer.init(period=speed, mode=Timer.PERIODIC, callback=update)
        if random.random() < 0.3:
            boosts.append(place_item(snake + [food]))
    else:
        snake.pop()

    # Boosts
    if new_head in boosts:
        score += 2
        buzz(2000, 80)
        boosts.remove(new_head)

    draw()

# === Initial Game Start ===
food = place_item(snake)
draw()
game_timer.init(period=speed, mode=Timer.PERIODIC, callback=update)
button_timer.init(period=100, mode=Timer.PERIODIC, callback=check_buttons)
