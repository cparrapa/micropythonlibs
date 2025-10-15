from machine import Pin, PWM
import neopixel
import time
import random
import os

# ========== TETRIS CONFIG ==========
MATRIX_PIN = 18
WIDTH, HEIGHT = 8, 16
BRIGHTNESS = 0.3
LEFT_BTN_PIN = 27
RIGHT_BTN_PIN = 14
ENC_CLK = 21
ENC_DT = 22
BUZZER_PIN = 25
# ============================

FONT = {
    '0': [(1,1,1),
           (1,0,1),
           (1,0,1),
           (1,0,1),
           (1,1,1)],
    '1': [(0,1,0),
           (1,1,0),
           (0,1,0),
           (0,1,0),
           (1,1,1)],
    '2': [(1,1,1),
           (0,0,1),
           (1,1,1),
           (1,0,0),
           (1,1,1)],
    '3': [(1,1,1),
           (0,0,1),
           (1,1,1),
           (0,0,1),
           (1,1,1)],
    '4': [(1,0,1),
           (1,0,1),
           (1,1,1),
           (0,0,1),
           (0,0,1)],
    '5': [(1,1,1),
           (1,0,0),
           (1,1,1),
           (0,0,1),
           (1,1,1)],
    '6': [(1,1,1),
           (1,0,0),
           (1,1,1),
           (1,0,1),
           (1,1,1)],
    '7': [(1,1,1),
           (0,0,1),
           (0,1,0),
           (1,0,0),
           (1,0,0)],
    '8': [(1,1,1),
           (1,0,1),
           (1,1,1),
           (1,0,1),
           (1,1,1)],
    '9': [(1,1,1),
           (1,0,1),
           (1,1,1),
           (0,0,1),
           (1,1,1)],
}

FONT.update({
    'S': [(1,1,1),
          (1,0,0),
          (1,1,1),
          (0,0,1),
          (1,1,1)],
    'C': [(1,1,1),
          (1,0,0),
          (1,0,0),
          (1,0,0),
          (1,1,1)],
    'O': [(1,1,1),
          (1,0,1),
          (1,0,1),
          (1,0,1),
          (1,1,1)],
    'R': [(1,1,0),
          (1,0,1),
          (1,1,0),
          (1,0,1),
          (1,0,1)],
    'E': [(1,1,1),
          (1,0,0),
          (1,1,1),
          (1,0,0),
          (1,1,1)],
    'T': [(1,1,1),
          (0,1,0),
          (0,1,0),
          (0,1,0),
          (0,1,0)],
    'P': [(1,1,1),
          (1,0,1),
          (1,1,1),
          (1,0,0),
          (1,0,0)],
    ' ': [(0,0,0),
          (0,0,0),
          (0,0,0),
          (0,0,0),
          (0,0,0)],
})

# NeoPixel matrix
np = neopixel.NeoPixel(Pin(MATRIX_PIN), WIDTH * HEIGHT)

# Controls
btn_left = Pin(LEFT_BTN_PIN, Pin.IN, Pin.PULL_UP)
btn_right = Pin(RIGHT_BTN_PIN, Pin.IN, Pin.PULL_UP)
enc_clk = Pin(ENC_CLK, Pin.IN, Pin.PULL_UP)
enc_dt = Pin(ENC_DT, Pin.IN, Pin.PULL_UP)
last_clk_val = enc_clk.value()

# Button states for edge detection
last_btn_left = 1
last_btn_right = 1

# Buzzer setup
buzzer = PWM(Pin(BUZZER_PIN), freq=1000, duty=0)
def buzz(freq, dur=100, duty=200):
    buzzer.freq(freq)
    buzzer.duty(duty)
    time.sleep_ms(dur)
    buzzer.duty(0)
def blip(): buzz(1200, 40)
def click(): buzz(1500, 20)
def thud(): buzz(300, 60)
def jingle():
    for f in [600, 800, 1000, 1200]:
        buzz(f, 80)
        time.sleep_ms(30)
def sad_tone():
    for f in [400, 300, 200]:
        buzz(f, 200)
        time.sleep_ms(100)
        
def play_tetris_theme():
    # simplified Korobeiniki melody (main motif)
    melody = [
        (659, 150), (494, 100), (523, 100), (587, 100),
        (523, 100), (494, 100), (440, 150),
        (440, 100), (523, 100), (659, 150), (587, 100),
        (523, 100), (494, 100), (523, 100),
        (494, 150), (392, 150)
    ]
    for freq, dur in melody:
        buzz(freq, dur, 300)
        time.sleep_ms(30)

# Fixed colors per shape
SHAPE_COLORS = [
    (255, 0, 0),     # O
    (0, 255, 0),     # T
    (0, 0, 255),     # I
    (255, 255, 0),   # S
    (0, 255, 255),   # Z
    (255, 128, 0),   # L
    (128, 0, 255),   # J
]

# Predefined 4 rotation states per shape
SHAPES = [
    # O
    [[(0,0),(1,0),(0,1),(1,1)]] * 4,

    # T
    [[(0,0),(1,0),(2,0),(1,1)],
     [(1,0),(1,1),(1,2),(0,1)],
     [(0,1),(1,1),(2,1),(1,0)],
     [(1,0),(1,1),(1,2),(2,1)]],

    # I
    [[(0,0),(1,0),(2,0),(3,0)],
     [(2,0),(2,1),(2,2),(2,3)],
     [(0,1),(1,1),(2,1),(3,1)],
     [(1,0),(1,1),(1,2),(1,3)]],

    # S
    [[(1,0),(2,0),(0,1),(1,1)],
     [(1,0),(1,1),(2,1),(2,2)],
     [(1,1),(2,1),(0,2),(1,2)],
     [(0,0),(0,1),(1,1),(1,2)]],

    # Z
    [[(0,0),(1,0),(1,1),(2,1)],
     [(2,0),(1,1),(2,1),(1,2)],
     [(0,1),(1,1),(1,2),(2,2)],
     [(1,0),(0,1),(1,1),(0,2)]],

    # L
    [[(1,0),(1,1),(1,2),(0,2)],
     [(0,1),(1,1),(2,1),(2,2)],
     [(0,0),(1,0),(0,1),(0,2)],
     [(0,0),(0,1),(1,1),(2,1)]],

    # J
    [[(0,0),(0,1),(0,2),(1,2)],
     [(0,1),(1,1),(2,1),(2,0)],
     [(0,0),(1,0),(1,1),(1,2)],
     [(0,1),(1,1),(2,1),(0,2)]],
]

# Game state
grid = [[(0,0,0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
current_piece = None
px, py = 2, 0
rotation_index = 0
score = 0
high_score = 0

def scale_color(color):
    return tuple(int(c * BRIGHTNESS) for c in color)

def clear_matrix():
    for i in range(WIDTH * HEIGHT):
        np[i] = (0, 0, 0)

def draw_grid():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            np[y * WIDTH + x] = scale_color(grid[y][x])

def draw_piece():
    shape = current_piece['shape']
    color = scale_color(current_piece['color'])
    for dx, dy in shape:
        x, y = px + dx, py + dy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            np[y * WIDTH + x] = color

def valid_position(x0, y0, shape):
    for dx, dy in shape:
        x, y = x0 + dx, y0 + dy
        if x < 0 or x >= WIDTH or y >= HEIGHT:
            return False
        if y >= 0 and grid[y][x] != (0, 0, 0):
            return False
    return True

def freeze_piece():
    for dx, dy in current_piece['shape']:
        x, y = px + dx, py + dy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            grid[y][x] = current_piece['color']

def remove_lines():
    global grid, score
    cleared = 0
    new_grid = []
    for row in grid:
        if all(p != (0,0,0) for p in row):
            cleared += 1
        else:
            new_grid.append(row)
    while len(new_grid) < HEIGHT:
        new_grid.insert(0, [(0, 0, 0)] * WIDTH)
    grid = new_grid
    if cleared:
        score += cleared * 10
        jingle()

def new_piece():
    global current_piece, px, py, rotation_index
    i = random.randint(0, len(SHAPES) - 1)
    rotations = SHAPES[i]
    color = SHAPE_COLORS[i]
    current_piece = {
        'rotations': rotations,
        'shape': rotations[0],
        'color': color
    }
    px, py, rotation_index = 2, 0, 0

def rotate_piece(clockwise=True):
    global rotation_index
    new_idx = (rotation_index + (1 if clockwise else -1)) % 4
    candidate = current_piece['rotations'][new_idx]
    if valid_position(px, py, candidate):
        current_piece['shape'] = candidate
        rotation_index = new_idx

def scroll_text(text, color=(0,255,0), speed=100):
    pixels = []
    for ch in text:
        if ch in FONT:
            char = FONT[ch]
            for col in range(3):
                column = [char[row][col] for row in range(5)]
                pixels.append(column)
            pixels.append([0]*5)  # spacing
    total_cols = len(pixels)
    for offset in range(total_cols - WIDTH + 1):
        clear_matrix()
        for x in range(WIDTH):
            col = pixels[offset + x] if offset + x < total_cols else [0]*5
            for y in range(5):
                if col[y]:
                    np[(y+5)*WIDTH + x] = scale_color(color)
        np.write()
        time.sleep_ms(speed)
    
def show_score_animation():
    global score, high_score
    if score > high_score:
        high_score = score
        save_high_score(high_score)
        jingle()

    scroll_text("SCORE " + str(score), color=(0,255,0))
    time.sleep(1)
    scroll_text("TOP " + str(high_score), color=(0,0,255))
    time.sleep(1)

def load_high_score():
    try:
        with open("highscore.txt") as f:
            return int(f.read().strip())
    except:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as f:
        f.write(str(score))

high_score = load_high_score()

def game_over():
    sad_tone()
    show_score_animation()
    reset_game()

def reset_game():
    global grid, score
    grid = [[(0, 0, 0) for _ in range(WIDTH)] for _ in range(HEIGHT)]
    score = 0
    new_piece()

# --- Game start ---
new_piece()
fall_timer = time.ticks_ms()
fall_interval = 500
move_timer = time.ticks_ms()
move_delay = 150

# Encoder state
last_btn_left = btn_left.value()
last_btn_right = btn_right.value()
last_clk = enc_clk.value()

play_tetris_theme()

# --- Main Loop ---
while True:
    clear_matrix()
    draw_grid()
    draw_piece()
    np.write()
    time.sleep_ms(1)

     # --- Encoder Rotation ---
    clk_now = enc_clk.value()
    dt_now = enc_dt.value()
    now = time.ticks_ms()

    # Detect *either* edge to improve response
    if clk_now != last_clk:
        if time.ticks_diff(now, move_timer) > 100:  # debounce
            rotate_piece(clockwise=(clk_now != dt_now))
            click()
            move_timer = now
    last_clk = clk_now

    # --- Movement (edge detection) ---
    if time.ticks_diff(now, move_timer) > move_delay:
        curr_left = btn_left.value()
        curr_right = btn_right.value()

        if last_btn_left == 1 and curr_left == 0:
            if valid_position(px - 1, py, current_piece['shape']):
                px -= 1
                move_timer = now
                blip()

        elif last_btn_right == 1 and curr_right == 0:
            if valid_position(px + 1, py, current_piece['shape']):
                px += 1
                move_timer = now
                blip()

        last_btn_left = curr_left
        last_btn_right = curr_right

    # --- Fall (with fast drop) ---
    now_ms = time.ticks_ms()

    # Detect long press on both buttons
    if btn_left.value() or not btn_right.value():
        if 'press_start' not in locals():
            press_start = now_ms
        elif time.ticks_diff(now_ms, press_start) > 1000:  # 1 sec hold
            fall_interval = 75   # fast drop speed
    else:
        press_start = None
        fall_interval = 500      # normal speed

    # Apply gravity
    if time.ticks_diff(now_ms, fall_timer) > fall_interval:
        fall_timer = now_ms
        if valid_position(px, py + 1, current_piece['shape']):
            py += 1
        else:
            freeze_piece()
            thud()
            remove_lines()
            new_piece()
            if not valid_position(px, py, current_piece['shape']):
                game_over()
