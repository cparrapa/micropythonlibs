from machine import Pin, I2C, Timer
import ssd1306
import time

# === Display setup ===
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === Input setup ===
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# === Game constants ===
paddle_width = 20
paddle_height = 4
paddle_y = 60
ball_size = 2
brick_width = 16
brick_height = 6
brick_cols = 8
max_levels = 5

# === Game state ===
def init_game(level=1):
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy
    global game_over, score, bricks, current_level, speed_factor

    paddle_x = 54
    ball_x = 64
    ball_y = 32
    ball_dx = 1
    ball_dy = -1
    game_over = False
    score = 0 if level == 1 else score
    current_level = level
    speed_factor = 1.0 + (level - 1) * 0.2  # Increase speed per level

    # Create bricks grid
    bricks = []
    brick_rows = level + 2  # More rows with level
    for row in range(brick_rows):
        for col in range(brick_cols):
            x = col * brick_width
            y = row * brick_height
            bricks.append((x, y))

init_game()

def draw():
    oled.fill(0)

    # Draw paddle
    oled.fill_rect(paddle_x, paddle_y, paddle_width, paddle_height, 1)

    # Draw ball
    oled.fill_rect(int(ball_x), int(ball_y), ball_size, ball_size, 1)

    # Draw bricks
    for (bx, by) in bricks:
        oled.rect(bx, by, brick_width - 2, brick_height - 2, 1)

    # Score and level
    oled.text("Score: {}".format(score), 0, 56)
    oled.text("Lvl:{}".format(current_level), 90, 56)

    # Game over
    if game_over:
        oled.text("GAME OVER", 30, 30)

    oled.show()

def reset_check():
    # Hold both buttons 2 sec
    start = time.ticks_ms()
    while not btn_left.value() and not btn_right.value():
        if time.ticks_diff(time.ticks_ms(), start) > 2000:
            init_game(1)
            return True
    return False

def advance_level():
    global current_level
    if current_level < max_levels:
        current_level += 1
        init_game(current_level)
    else:
        # Game completed
        global game_over
        game_over = True

def update_game(timer):
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, game_over, score, bricks, speed_factor

    if game_over:
        if reset_check():
            draw()
        return

    # Paddle control
    if not btn_left.value() and paddle_x > 0:
        paddle_x -= 2
    if not btn_right.value() and paddle_x < 128 - paddle_width:
        paddle_x += 2

    # Ball movement
    ball_x += ball_dx * speed_factor
    ball_y += ball_dy * speed_factor

    # Wall bounce
    if ball_x <= 0 or ball_x >= 128 - ball_size:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    # Paddle bounce
    if (paddle_y <= ball_y + ball_size <= paddle_y + paddle_height and
            paddle_x <= ball_x <= paddle_x + paddle_width):
        ball_dy *= -1
        ball_y = paddle_y - ball_size

    # Brick collision
    hit_index = None
    for i, (bx, by) in enumerate(bricks):
        if (bx <= ball_x <= bx + brick_width - 2 and
                by <= ball_y <= by + brick_height - 2):
            hit_index = i
            break
    if hit_index is not None:
        del bricks[hit_index]
        score += 1
        ball_dy *= -1
        speed_factor += 0.02  # Increase speed slightly per hit

    # Win level
    if not bricks:
        advance_level()
        return

    # Game over
    if ball_y > 64:
        game_over = True

    draw()

# === Game timer ===
game_timer = Timer(0)
game_timer.init(period=30, mode=Timer.PERIODIC, callback=update_game)

# === Main loop ===
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    game_timer.deinit()
    print("Game stopped.")
