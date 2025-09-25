from machine import Pin, I2C
import ssd1306
import time

# I2C and OLED
i2c = I2C(scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Buttons
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)
btn_enc = Pin(27, Pin.IN, Pin.PULL_UP)

# Encoder pins
enc_clk = Pin(21, Pin.IN, Pin.PULL_UP)
enc_dt = Pin(22, Pin.IN, Pin.PULL_UP)
last_state = (enc_clk.value(), enc_dt.value())

# Menu layout
ROWS, COLS = 2, 3
ITEMS_PER_PAGE = ROWS * COLS
TOTAL_ITEMS = 12
NUM_PAGES = (TOTAL_ITEMS + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
cursor_global = 0

# Buttons state
last_btn_left = 1
last_btn_enc = 1
btn_both_press_time = None

# ==== ICON DEFINITIONS (16x16 bitmaps) ====
icons = [None] * TOTAL_ITEMS

# Snake icon
icons[0] = [
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000011, 0b11000000,
    0b00000100, 0b00100000,
    0b00000101, 0b10000000,
    0b00000100, 0b00000000,
    0b00000010, 0b01000000,
    0b00000010, 0b11000000,
    0b00001011, 0b00001100,
    0b00010001, 0b00010100,
    0b00101111, 0b00110000,
    0b00100000, 0b10000000,
    0b00011000, 0b11100000,
    0b00000111, 0b10000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
]


# Space Invaders icon
icons[1] = [
    0b00011110, 0b00000000,
    0b00111111, 0b00000000,
    0b01111111, 0b10000000,
    0b11111111, 0b11000000,
    0b11011011, 0b11000000,
    0b11111111, 0b11000000,
    0b01111111, 0b10000000,
    0b00100100, 0b10000000,
    0b01000000, 0b01000000,
    0b00011000, 0b00000000,
    0b00111100, 0b00000000,
    0b00100100, 0b00000000,
    0b01111110, 0b00000000,
    0b01011010, 0b00000000,
    0b10000001, 0b00000000,
    0b00000000, 0b00000000,
]

icons[2] = [
    0b00000000, 0b00000000,
    0b00000111, 0b11100000,
    0b00011111, 0b11111000,
    0b00111111, 0b11111100,
    0b01111111, 0b11111110,
    0b01111111, 0b11111110,
    0b01111111, 0b11111110,
    0b00111111, 0b11111100,
    0b00011111, 0b11111000,
    0b00001111, 0b11110000,
    0b00000111, 0b11100000,
    0b00000011, 0b11000000,
    0b00000111, 0b11100000,
    0b00001111, 0b11110000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
]

# Aranoid icon
icons[3] = [
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00111111, 0b11111100,
    0b11111111, 0b00000000,
    0b00000000, 0b01000000,
    0b00111111, 0b11000000,
    0b00001111, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00100000,
    0b00000000, 0b00100000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
]

# MiniGolf icon
icons[4] = [
    0b00000001, 0b11000000,
    0b00000001, 0b10010000,
    0b00000001, 0b01001000,
    0b00000001, 0b00010100,
    0b00000001, 0b01000011,
    0b00000001, 0b00100000,
    0b00000001, 0b10000000,
    0b00000001, 0b00000000,
    0b00000001, 0b00000000,
    0b00000001, 0b00000000,
    0b00000111, 0b11000000,
    0b01100001, 0b00001000,
    0b10001101, 0b01000010,
    0b10001001, 0b00100010,
    0b01000001, 0b00000100,
    0b00011100, 0b01110000,
]

icons[6] = [
    0b00000000, 0b00000000,
    0b00000011, 0b00000000,
    0b00000111, 0b10000000,
    0b00000101, 0b10000000,
    0b00000001, 0b10000000,
    0b00000011, 0b00000000,
    0b00000111, 0b00000000,
    0b00000110, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
    0b00000000, 0b00000000,
]


# ==== Draw Menu ====
def draw_menu():
    oled.fill(0)
    page = cursor_global // ITEMS_PER_PAGE
    cursor_local = cursor_global % ITEMS_PER_PAGE
    start = page * ITEMS_PER_PAGE
    end = min(start + ITEMS_PER_PAGE, TOTAL_ITEMS)

    for i, idx in enumerate(range(start, end)):
        row, col = divmod(i, COLS)
        x = 5 + col * 40
        y = 5 + row * 20
        if icons[idx]:
            oled.blit_framebuf(bytearray(icons[idx]), 16, 16, x, y)
        else:
            oled.text(f"G{idx+1}", x, y)

        if i == cursor_local:
            oled.rect(x - 2, y - 2, 20, 20, 1)

    # Page indicators
    indic_y = 50
    for p in range(NUM_PAGES):
        x = 54 + (p - NUM_PAGES // 2) * 8
        oled.fill_rect(x, indic_y, 6, 6, 1 if p == page else 0)
        if p != page:
            oled.rect(x, indic_y, 6, 6, 1)
    oled.show()

# Add helper for blit 1-bit bitmap
def blit_framebuf(data, width, height, x, y):
    import framebuf
    fb = framebuf.FrameBuffer(data, width, height, framebuf.MONO_HLSB)
    oled.blit(fb, x, y)

# Inject it into oled object
oled.blit_framebuf = blit_framebuf

# Encoder handling
def check_encoder():
    global last_state, cursor_global
    clk_now = enc_clk.value()
    dt_now = enc_dt.value()
    if (clk_now, dt_now) != last_state:
        if last_state == (1, 1):
            if clk_now == 0 and dt_now == 1:
                cursor_global = (cursor_global + 1) % TOTAL_ITEMS
            elif clk_now == 1 and dt_now == 0:
                cursor_global = (cursor_global - 1 + TOTAL_ITEMS) % TOTAL_ITEMS
            draw_menu()
        last_state = (clk_now, dt_now)

# Button handling
def check_buttons():
    global cursor_global, btn_both_press_time, last_btn_left, last_btn_enc
    l = btn_left.value()
    e = btn_enc.value()
    t = time.ticks_ms()

    if last_btn_left == 1 and l == 0:
        idx = cursor_global
        fname = f'game{idx+1}.py'
        try:
            import gc
            gc.collect()
            with open(fname) as f:
                exec(f.read(), {})
        except Exception as e:
            print(f"Failed to run {fname}: {e}")
    last_btn_left = l

    if l == 0 and e == 0:
        if btn_both_press_time is None:
            btn_both_press_time = t
        elif time.ticks_diff(t, btn_both_press_time) > 1000:
            cursor_global = 0
            draw_menu()
            btn_both_press_time = None
    else:
        btn_both_press_time = None
    last_btn_enc = e

# Main loop
def main():
    draw_menu()
    while True:
        check_encoder()
        check_buttons()
        time.sleep_ms(10)

if __name__ == "__main__":
    main()
