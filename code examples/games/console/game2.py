# game2.py — Space Invaders (levels & scaling, polarity-agnostic buttons)
# Controls:
#   - LEFT  button  (GPIO4):  move left (hold)
#   - RIGHT button  (GPIO27): move right (hold)
#   - Hold BOTH buttons ≥ 1000 ms: exit to menu
#
# Plug-in signature: run(shared_i2c) and return to exit.

import time, urandom
from machine import Pin
from ssd1306 import SSD1306_I2C

# ---- Pins (confirmed) ----
LEFT_BTN_PIN  = 4
RIGHT_BTN_PIN = 27

# ---- OLED ----
W, H = 128, 64

# ---- Player ----
SHIP_W, SHIP_H = 12, 4
SHIP_Y         = 56
SHIP_SPEED     = 2

# ---- Bullet ----
BULLET_W, BULLET_H   = 2, 4
BULLET_SPEED         = 4
SHOT_COOLDOWN_MS     = 500     # auto-fire cadence

# ---- Invaders ----
INV_W, INV_H         = 10, 6
INV_HSTEP            = 4
INV_VSTEP            = 8
INV_BASE_PERIOD_MS   = 600      # moves faster with level
INV_MIN_PERIOD_MS    = 80
INV_COLS             = 12       # 0..11 -> x = col*10
INV_XMAX             = 118      # 128 - INV_W

# ---- Exit gesture ----
LONG_BOTH_MS   = 1000

# ---- Safe OLED show (retry around transient I2C timeouts) ----
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

# ---- RNG helpers ----
def _rand(n):               # 0..n-1
    return urandom.getrandbits(16) % n
def _rand_col():            # 0..11
    return _rand(INV_COLS)

def run(shared_i2c):
    oled = SSD1306_I2C(W, H, shared_i2c)

    # Inputs — NO internal pulls; respect board's resistors
    btnL = Pin(LEFT_BTN_PIN,  Pin.IN)
    btnR = Pin(RIGHT_BTN_PIN, Pin.IN)

    # Sample idle levels to be polarity-agnostic
    idleL = btnL.value()
    idleR = btnR.value()
    def pressedL(): return btnL.value() != idleL
    def pressedR(): return btnR.value() != idleR

    # Exit gesture tracking
    both_hold_t = None

    # Game state
    score = 0
    level = 1
    ship_x = 60

    bullet_x = None
    bullet_y = None
    last_shot = time.ticks_ms() - SHOT_COOLDOWN_MS  # allow immediate shot

    invaders = []
    inv_dir = 1
    last_inv_step = time.ticks_ms()

    def inv_period():
        # Speed up as level increases, but clamp to a minimum
        return max(INV_MIN_PERIOD_MS, INV_BASE_PERIOD_MS - level * 40)

    def reset_invaders():
        nonlocal invaders, inv_dir
        invaders = []
        rows = min(2 + level, 6)        # 2..6 rows as level grows
        used = set()
        for r in range(rows):
            col = _rand_col()
            while (r, col) in used:
                col = _rand_col()
            used.add((r, col))
            x = col * 10
            y = 8 * r
            invaders.append([x, y])
        inv_dir = 1

    reset_invaders()

    # ---- Draw ----
    def draw():
        oled.fill(0)
        oled.text("L{} S{}".format(level, score), 0, 0)
        oled.fill_rect(ship_x, SHIP_Y, SHIP_W, SHIP_H, 1)       # Ship
        for x, y in invaders:                                   # Invaders
            oled.fill_rect(x, y, INV_W, INV_H, 1)
        if bullet_x is not None:                                # Bullet
            oled.fill_rect(bullet_x, bullet_y, BULLET_W, BULLET_H, 1)
        _safe_show(oled)

    # ---- Actions ----
    def move_ship(dx):
        nonlocal ship_x
        nx = ship_x + dx
        if nx < 0: nx = 0
        if nx > W - SHIP_W: nx = W - SHIP_W
        ship_x = nx

    def fire():
        nonlocal bullet_x, bullet_y, last_shot
        now = time.ticks_ms()
        if bullet_x is None and time.ticks_diff(now, last_shot) >= SHOT_COOLDOWN_MS:
            bullet_x = ship_x + SHIP_W // 2
            bullet_y = SHIP_Y - BULLET_H
            last_shot = now

    def step_invaders():
        nonlocal inv_dir
        shift_down = False
        for inv in invaders:
            inv[0] += inv_dir * INV_HSTEP
            if inv[0] < 0 or inv[0] > INV_XMAX:
                shift_down = True
        if shift_down:
            for inv in invaders:
                inv[1] += INV_VSTEP
            inv_dir *= -1

    def move_bullet():
        nonlocal bullet_x, bullet_y
        if bullet_x is None:
            return
        bullet_y -= BULLET_SPEED
        if bullet_y < -BULLET_H:
            bullet_x = bullet_y = None

    def bullet_hit():
        nonlocal bullet_x, bullet_y, score
        if bullet_x is None:
            return
        bx0, by0 = bullet_x, bullet_y
        bx1, by1 = bx0 + BULLET_W, by0 + BULLET_H
        # AABB collision
        hit_idx = -1
        for i, (ix, iy) in enumerate(invaders):
            ix1, iy1 = ix + INV_W, iy + INV_H
            if (bx0 < ix1 and bx1 > ix and by0 < iy1 and by1 > iy):
                hit_idx = i
                break
        if hit_idx >= 0:
            invaders.pop(hit_idx)
            score += 1
            bullet_x = bullet_y = None

    # Initial draw
    draw()

    # ---- Main loop ----
    try:
        while True:
            now = time.ticks_ms()

            # ------ Exit gesture: BOTH held long ------
            if pressedL() and pressedR():
                if both_hold_t is None:
                    both_hold_t = now
                elif time.ticks_diff(now, both_hold_t) >= LONG_BOTH_MS:
                    _exit_to_menu(oled)
                    return
            else:
                both_hold_t = None

            # ------ Controls (hold to move; no move when both held) ------
            if pressedL() and not pressedR():
                move_ship(-SHIP_SPEED)
            elif pressedR() and not pressedL():
                move_ship(+SHIP_SPEED)
            # if both pressed: reserved for exit (no movement)

            # Auto-fire (same cadence as your original)
            fire()

            # Invader timing
            if time.ticks_diff(now, last_inv_step) >= inv_period():
                last_inv_step = now
                step_invaders()

            # Bullet + collisions
            move_bullet()
            bullet_hit()

            # Level up
            if not invaders:
                level += 1
                reset_invaders()
                bullet_x = bullet_y = None
                draw()
                time.sleep_ms(300)

            # Game over: any invader reaches ship row
            for ix, iy in invaders:
                if iy + INV_H >= SHIP_Y:
                    _game_over(oled, score, level)
                    return

            # Draw frame
            draw()
            time.sleep_ms(20)

    except Exception as _e:
        _game_over(oled, score, level)
        return

# ---- UI helpers ----
def _game_over(oled, score, level):
    oled.fill(0)
    oled.text("GAME OVER", 20, 18)
    oled.text("Score: {}".format(score), 16, 34)
    oled.text("Lvl: {}".format(level),   40, 46)
    _safe_show(oled)
    time.sleep_ms(1200)

def _exit_to_menu(oled):
    oled.fill(0)
    oled.text("Exit to menu", 16, 26)
    _safe_show(oled)
    time.sleep_ms(200)
