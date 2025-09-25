# game2.py - Space Invaders with levels and scaling

from machine import Pin, I2C, reset
import ssd1306
import time
import random

# OLED setup
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Controls
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)
btn_right = Pin(27, Pin.IN, Pin.PULL_UP)

# Game state
score = 0
level = 1

# Player
ship_x = 60
ship_y = 56
ship_w = 12
ship_h = 4

# Bullet
bullet_x = None
bullet_y = None
bullet_speed = 4
last_shot = time.ticks_ms()

# Invaders
invaders = []
inv_dir = 1
last_invader_move = time.ticks_ms()

# Long press detection
both_pressed_time = None
LONG_PRESS_DURATION = 2000  # milliseconds

def reset_invaders():
    global invaders, inv_dir
    invaders = []
    for i in range(min(2 + level, 6)):  # up to 6 invaders
        x = random.randint(0, 11) * 10
        y = i * 8
        invaders.append([x, y])
    inv_dir = 1

def draw():
    oled.fill(0)
    oled.fill_rect(ship_x, ship_y, ship_w, ship_h, 1)
    for x, y in invaders:
        oled.fill_rect(x, y, 10, 6, 1)
    if bullet_x is not None:
        oled.fill_rect(bullet_x, bullet_y, 2, 4, 1)
    oled.text("L{} S{}".format(level, score), 0, 0)
    oled.show()

def move_ship(dx):
    global ship_x
    ship_x = max(0, min(128 - ship_w, ship_x + dx))

def fire():
    global bullet_x, bullet_y
    if bullet_x is None:
        bullet_x = ship_x + ship_w // 2
        bullet_y = ship_y - 4

# Start level
reset_invaders()
draw()

try:
    while True:
        now = time.ticks_ms()

        # Long press check
        if not btn_left.value() and not btn_right.value():
            if both_pressed_time is None:
                both_pressed_time = now
            elif time.ticks_diff(now, both_pressed_time) > LONG_PRESS_DURATION:
                import main
                main.main()  # assuming main.py has a main() function
        else:
            both_pressed_time = None

        # Controls
        if not btn_left.value():
            move_ship(-2)
        if not btn_right.value():
            move_ship(2)

        # Auto-fire
        if time.ticks_diff(now, last_shot) > 500:
            fire()
            last_shot = now

        # Move invaders
        if time.ticks_diff(now, last_invader_move) > max(80, 600 - level * 40):
            last_invader_move = now
            shift_down = False
            for inv in invaders:
                inv[0] += inv_dir * 4
                if inv[0] < 0 or inv[0] > 118:
                    shift_down = True
            if shift_down:
                for inv in invaders:
                    inv[1] += 8
                inv_dir *= -1

        # Move bullet
        if bullet_x is not None:
            bullet_y -= bullet_speed
            if bullet_y < 0:
                bullet_x = None
                bullet_y = None

        # Collision detection
        if bullet_x is not None:
            hit = None
            for inv in invaders:
                if inv[0] < bullet_x < inv[0] + 10 and inv[1] < bullet_y < inv[1] + 6:
                    hit = inv
                    break
            if hit:
                invaders.remove(hit)
                score += 1
                bullet_x = None
                bullet_y = None

        # Level up
        if not invaders:
            level += 1
            reset_invaders()
            bullet_x = bullet_y = None
            time.sleep(0.5)

        # Game over
        for inv in invaders:
            if inv[1] + 6 >= ship_y:
                raise Exception("Game Over")

        draw()
        time.sleep_ms(20)

except Exception as e:
    oled.fill(0)
    oled.text("GAME OVER", 20, 20)
    oled.text("Score: {}".format(score), 20, 36)
    oled.text("Lvl: {}".format(level), 40, 50)
    oled.show()
    time.sleep(3)
