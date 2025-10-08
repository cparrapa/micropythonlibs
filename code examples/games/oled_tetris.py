from machine import Pin, I2C
import ssd1306
import time
import random
 
# Display setup
i2c = I2C(scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
 
# Controls
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)   # RIGHT button
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)  # LEFT button
enc_clk = Pin(21, Pin.IN, Pin.PULL_UP)
enc_dt = Pin(22, Pin.IN, Pin.PULL_UP)
last_clk = enc_clk.value()
 
# Grid settings
COLS = 10
ROWS = 16
BLOCK_W = 6
BLOCK_H = 4
OFFSET_X = 1
OFFSET_Y = 0
 
# Shapes
SHAPES = [
    [[(0,0),(1,0),(0,1),(1,1)]],
    [[(0,0),(1,0),(2,0),(1,1)]],
    [[(0,0),(1,0),(2,0),(3,0)]],
    [[(0,1),(1,1),(1,0),(2,0)]],
    [[(0,0),(1,0),(1,1),(2,1)]],
]
 
# Game state
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
px, py = 3, 0
rotation_index = 0
current_piece = None
next_piece = None
score = 0
fall_timer = time.ticks_ms()
fall_interval = 250
move_timer = time.ticks_ms()
move_delay = 150
game_over_flag = False
 
def draw_block(x, y, fill=1):
    oled.fill_rect(OFFSET_X + x * BLOCK_W, OFFSET_Y + y * BLOCK_H, BLOCK_W - 1, BLOCK_H - 1, fill)
 
def draw_grid():
    oled.fill(0)
    oled.rect(OFFSET_X - 1, OFFSET_Y - 1, COLS * BLOCK_W + 2, ROWS * BLOCK_H + 2, 1)
    for y in range(ROWS):
        for x in range(COLS):
            if grid[y][x]:
                draw_block(x, y, 1)
 
def draw_piece():
    for dx, dy in current_piece['shape']:
        x = px + dx
        y = py + dy
        if 0 <= x < COLS and 0 <= y < ROWS:
            draw_block(x, y, 1)
 
def draw_next_preview():
    base_x = 65
    base_y = 10
    oled.rect(base_x - 2, base_y - 2, 18, 18, 1)
    for dx, dy in next_piece['rotations'][0]:
        x = dx * 3 + base_x
        y = dy * 3 + base_y
        oled.fill_rect(x, y, 3, 3, 1)
 
def rotate_all(shape):
    rotations = [shape]
    for _ in range(3):
        shape = [(-y, x) for x, y in shape]
        min_x = min(x for x, y in shape)
        min_y = min(y for x, y in shape)
        norm = [(x - min_x, y - min_y) for x, y in shape]
        rotations.append(norm)
    return rotations
 
def new_piece():
    global current_piece, px, py, rotation_index, next_piece
    if next_piece:
        current_piece = next_piece
    else:
        shape = random.choice(SHAPES)[0]
        rotations = rotate_all(shape)
        current_piece = {'rotations': rotations, 'shape': rotations[0]}
 
    # Preload next
    shape = random.choice(SHAPES)[0]
    rotations = rotate_all(shape)
    next_piece = {'rotations': rotations, 'shape': rotations[0]}
 
    px, py = 3, 0
    rotation_index = 0
 
def valid(x0, y0, shape):
    for dx, dy in shape:
        x = x0 + dx
        y = y0 + dy
        if x < 0 or x >= COLS or y >= ROWS:
            return False
        if y >= 0 and grid[y][x]:
            return False
    return True
 
def freeze():
    for dx, dy in current_piece['shape']:
        x = px + dx
        y = py + dy
        if 0 <= x < COLS and 0 <= y < ROWS:
            grid[y][x] = 1
 
def clear_lines():
    global grid, score
    new_grid = []
    cleared = 0
    for row in grid:
        if all(row):
            cleared += 1
        else:
            new_grid.append(row)
    while len(new_grid) < ROWS:
        new_grid.insert(0, [0] * COLS)
    grid = new_grid
    score += cleared * 100
 
def rotate_piece(clockwise=True):
    global rotation_index
    new_idx = (rotation_index + (1 if clockwise else -1)) % 4
    candidate = current_piece['rotations'][new_idx]
    if valid(px, py, candidate):
        current_piece['shape'] = candidate
        rotation_index = new_idx
 
def game_over():
    global game_over_flag
    oled.fill(0)
    oled.text("GAME OVER", 20, 20)
    oled.text("Score: {}".format(score), 20, 40)
    oled.show()
    game_over_flag = True
 
# Game start
new_piece()
 
# Main loop
while True:
    if game_over_flag:
        continue
 
    draw_grid()
    draw_piece()
    draw_next_preview()
    oled.text("S: {}".format(score), 70, 0)
    oled.show()
 
    # Encoder for rotation
    clk = enc_clk.value()
    if last_clk == 1 and clk == 0:
        rotate_piece(clockwise=enc_dt.value() == 1)
    last_clk = clk
 
    # Button movement (corrected)
    now = time.ticks_ms()
    if time.ticks_diff(now, move_timer) > move_delay:
        if not btn_left.value() and valid(px + 1, py, current_piece['shape']):  # RIGHT
            px += 1
            move_timer = now
        elif not btn_right.value() and valid(px - 1, py, current_piece['shape']):  # LEFT
            px -= 1
            move_timer = now
 
    # Auto fall
    if time.ticks_diff(time.ticks_ms(), fall_timer) > fall_interval:
        fall_timer = time.ticks_ms()
        if valid(px, py + 1, current_piece['shape']):
            py += 1
        else:
            freeze()
            clear_lines()
            new_piece()
            if not valid(px, py, current_piece['shape']):
                game_over()
 
    time.sleep_ms(50)