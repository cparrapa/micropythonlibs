from machine import Pin, I2C
import ssd1306
import time

# --- OLED Setup ---
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # Adjust if needed
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# --- Button Setup ---
button = Pin(26, Pin.IN, Pin.PULL_UP)  # Connect button to GPIO14

# --- Animation Variables ---
x, y = 0, 0
dx, dy = 2, 2
shape = 0  # 0: Square, 1: Circle, 2: Triangle

# --- Debounce ---
last_button_state = 1
last_press_time = 0

def draw_shape(shape, x, y):
    size = 15
    if shape == 0:  # Square
        oled.rect(x, y, size, size, 1)
    elif shape == 1:  # Circle (simulated)
        r = size // 2
        for angle in range(0, 360, 30):
            rad = angle * 3.14159 / 180
            px = int(x + r + r * 0.9 * cos(rad))
            py = int(y + r + r * 0.9 * sin(rad))
            oled.pixel(px, py, 1)
    elif shape == 2:  # Triangle
        oled.line(x, y + size, x + size // 2, y, 1)
        oled.line(x + size // 2, y, x + size, y + size, 1)
        oled.line(x, y + size, x + size, y + size, 1)

# Trigonometric helpers
def sin(angle):
    from math import sin, radians
    return sin(radians(angle))

def cos(angle):
    from math import cos, radians
    return cos(radians(angle))

# --- Main Loop ---
while True:
    oled.fill(0)

    # Draw current shape
    draw_shape(shape, x, y)
    oled.show()

    # Update position
    x += dx
    y += dy

    # Bounce off edges
    if x <= 0 or x >= 128 - 15:
        dx = -dx
    if y <= 0 or y >= 64 - 15:
        dy = -dy

    # Check button press (simple debounce)
    current_state = button.value()
    if current_state == 0 and last_button_state == 1 and time.ticks_ms() - last_press_time > 200:
        shape = (shape + 1) % 3
        last_press_time = time.ticks_ms()

    last_button_state = current_state
    time.sleep(0.05)