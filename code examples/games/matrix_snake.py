import machine, neopixel, time, urandom, math

# ==== CONFIGURATION ====
PIN_NUM = 18              # NeoPixel pin
WIDTH = 16
HEIGHT = 8
BRIGHTNESS = 0.05
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BOOST_COLOR = (0, 0, 255)
INIT_SPEED = 0.3
BOOST_SPEED = 0.1
BOOST_DURATION = 5

BTN_LEFT = 14
BTN_RIGHT = 27
BUZZER_PIN = 25

MATRIX_TYPE = "col_straight"  # fixed for your matrix

# ==== SETUP ====
np = neopixel.NeoPixel(machine.Pin(PIN_NUM), WIDTH * HEIGHT)
btn_left = machine.Pin(BTN_LEFT, machine.Pin.IN, machine.Pin.PULL_UP)
btn_right = machine.Pin(BTN_RIGHT, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
buzzer.duty(0)  # off

# ==== GAME VARIABLES ====
snake = [(WIDTH//2, HEIGHT//2)]
DIRECTIONS = [(1,0), (0,1), (-1,0), (0,-1)]
dir_index = 0
food = None
boost = None
speed = INIT_SPEED
boost_end_time = 0
score = 0
rainbow_offset = 0

# ==== FUNCTIONS ====
def xy_to_index(x, y):
    if MATRIX_TYPE == "col_straight":
        return x * HEIGHT + y
    elif MATRIX_TYPE == "col_zigzag":
        if x % 2 == 0:
            return x * HEIGHT + y
        else:
            return x * HEIGHT + (HEIGHT - 1 - y)
    elif MATRIX_TYPE == "straight":
        return y * WIDTH + x
    elif MATRIX_TYPE == "zigzag":
        if y % 2 == 0:
            return y * WIDTH + x
        else:
            return y * WIDTH + (WIDTH - 1 - x)

def set_pixel(x, y, color):
    if 0 <= x < WIDTH and 0 <= y < HEIGHT:
        r, g, b = color
        np[xy_to_index(x, y)] = (int(r*BRIGHTNESS), int(g*BRIGHTNESS), int(b*BRIGHTNESS))

def wheel(pos):
    # pos 0-255 → RGB rainbow
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def draw():
    global rainbow_offset
    np.fill((0, 0, 0))
    if is_boosted():
        # Rainbow snake
        for i, segment in enumerate(snake):
            color = wheel((rainbow_offset + i*10) % 256)
            set_pixel(segment[0], segment[1], color)
        rainbow_offset = (rainbow_offset + 8) % 256
    else:
        for segment in snake:
            set_pixel(segment[0], segment[1], SNAKE_COLOR)
    if food:
        set_pixel(food[0], food[1], FOOD_COLOR)
    if boost:
        set_pixel(boost[0], boost[1], BOOST_COLOR)
    np.write()

def spawn_item(exclude):
    while True:
        pos = (urandom.getrandbits(4) % WIDTH, urandom.getrandbits(4) % HEIGHT)
        if pos not in exclude:
            return pos

def read_input():
    global dir_index
    if not btn_left.value():
        dir_index = (dir_index - 1) % 4
        time.sleep(0.15)
    elif not btn_right.value():
        dir_index = (dir_index + 1) % 4
        time.sleep(0.15)

def beep(freq, duration):
    buzzer.freq(freq)
    buzzer.duty(512)
    time.sleep(duration)
    buzzer.duty(0)

def move_snake():
    global snake, food, boost, score, speed, boost_end_time
    head_x, head_y = snake[0]
    dx, dy = DIRECTIONS[dir_index]
    new_head = ((head_x + dx) % WIDTH, (head_y + dy) % HEIGHT)

    if new_head in snake:
        game_over()
        return False

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        beep(880, 0.05)  # food beep
        food = spawn_item(snake)
        if urandom.getrandbits(2) == 0:
            boost = spawn_item(snake + [food])
    elif boost and new_head == boost:
        boost = None
        beep(1200, 0.05)  # boost double beep
        time.sleep(0.05)
        beep(1500, 0.05)
        boost_end_time = time.ticks_ms() + BOOST_DURATION * 1000
        speed = BOOST_SPEED
        snake.append(snake[-1])
    else:
        snake.pop()

    return True

def is_boosted():
    return boost_end_time and time.ticks_ms() <= boost_end_time

def update_boost():
    global speed
    if boost_end_time and time.ticks_ms() > boost_end_time:
        speed = INIT_SPEED

def game_over():
    np.fill((255, 0, 0))
    np.write()
    beep(200, 0.5)
    time.sleep(1)
    machine.reset()

# ==== INITIAL SPAWN ====
food = spawn_item(snake)

# ==== MAIN LOOP ====
last_move = time.ticks_ms()

while True:
    read_input()
    update_boost()
    if time.ticks_diff(time.ticks_ms(), last_move) > speed * 1000:
        if not move_snake():
            break
        draw()
        last_move = time.ticks_ms()

