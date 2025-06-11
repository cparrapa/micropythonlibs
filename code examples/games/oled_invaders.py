from machine import Pin, I2C, PWM, ADC
import ssd1306, time, random, os

# --- Hardware Initialization ---
i2c = I2C(0, scl=Pin(18), sda=Pin(19))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
buzzer = PWM(Pin(25)); buzzer.duty(0)
battery_adc = ADC(Pin(39)); battery_adc.atten(ADC.ATTN_11DB)
btn_enc = Pin(14, Pin.IN, Pin.PULL_UP)

# --- Rotary Encoder ---
class Rotary:
    def __init__(self, clk, dt):
        self.clk = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.pos = 0
        self.last_status = self.clk.value()
        self.clk.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._tick)

    def _tick(self, pin):
        if self.clk.value() != self.last_status:
            if self.dt.value() != self.clk.value():
                self.pos += 1
            else:
                self.pos -= 1
            self.last_status = self.clk.value()

    def get(self):
        if self.pos != 0:
            step = self.pos
            self.pos = 0
            return step
        return 0

rot = Rotary(21, 22)

# --- Constants and Variables ---
W, H = 128, 64
PY = H - 10
PW = 10; EW = 10; EH = 4; BS = 3

player_x = W // 2
bullets = []; enemies = []; explosions = []
score = high_score = level = enemy_speed = 0
last_shot = last_enemy = reset_timer = 0
game_state = "MENU"
menu_items = ["Start Game", "High Score", "Level Select"]
menu_idx = 0
selected_level = 1
enemy_bullets = []
last_enemy_shot = 0

# --- Melody Playback ---
def play_rttl(rttl):
    notes = {'c': 261, 'd': 294, 'e': 329, 'f': 349, 'g': 391,
             'a': 440, 'b': 493, 'p': 0}
    parts = rttl.split(':')
    defaults = dict([x.split('=') for x in parts[1].split(',')])
    melody = parts[2].split(',')
    dur = int(defaults['d'])
    bpm = int(defaults['b'])
    wholenote = (60000 * 4) / bpm

    for note in melody:
        n = note
        d = dur
        if n[0].isdigit():
            i = 0
            while n[i].isdigit(): i += 1
            d = int(n[:i]); n = n[i:]
        f = 1
        if '.' in n:
            n = n.replace('.', '')
            f = 1.5
        tone = notes.get(n[0], 0)
        duration = wholenote / d * f
        if tone > 0:
            buzzer.freq(int(tone))
            buzzer.duty(512)
        time.sleep_ms(int(duration))
        buzzer.duty(0)
        time.sleep_ms(20)

# Star Wars RTTL
starwars = "starwars:d=4,o=5,b=100:8g,8g,8g,8eb,16bb,8g,8eb,16bb,8g,p,8d#,8d#,8d#,8eb,16bb,8g,8eb,16bb,8g"

# --- Utility Functions ---
def beep(f, d):
    buzzer.freq(f)
    buzzer.duty(512)
    time.sleep_ms(d)
    buzzer.duty(0)

def explosion_sound():
    for f in range(1500, 500, -200):
        beep(f, 30)

def draw_batt():
    v = battery_adc.read() / 4095 * 2 * 3.3
    pct = min(max(int((v - 3.3) / 0.6 * 100), 0), 100)
    oled.rect(110, 2, 15, 6, 1)
    oled.fill_rect(125, 3, 2, 4, 1)
    oled.fill_rect(111, 3, int(pct / 100 * 13), 4, 1)

def load_hs():
    global high_score
    try:
        high_score = int(open("score.txt").read())
    except:
        high_score = 0

def save_hs():
    with open("score.txt","w") as f:
        f.write(str(high_score))

def spawn():
    global enemies
    enemies = [[i*18+5, j*10+5] for j in range(3) for i in range(6 + level)]

def reset():
    global player_x, bullets, explosions, score, enemy_speed, enemy_bullets
    player_x = W // 2
    bullets.clear(); explosions.clear(); enemy_bullets.clear()
    score = 0; enemy_speed = 1
    spawn()

def move_enemies():
    global enemy_speed
    shift = any(e[0] < 0 or e[0] > W - EW for e in enemies)
    if shift:
        for e in enemies:
            e[1] += enemy_speed
            if e[1] + EH >= PY:
                return True
    for e in enemies:
        e[0] += enemy_speed if not shift else 0
    return False

def update():
    global last_shot, level, enemy_speed, game_state
    global high_score, explosions, enemies, bullets, score, last_enemy
    global enemy_bullets, last_enemy_shot

    for b in bullets:
        b[1] -= BS
    bullets[:] = [b for b in bullets if b[1] > 0]

    for b in bullets[:]:
        for e in enemies[:]:
            if e[0] < b[0] < e[0] + EW and e[1] < b[1] < e[1] + EH:
                explosions.append([e[0], e[1]])
                enemies.remove(e); bullets.remove(b)
                explosion_sound(); score += 10
                break

    if time.ticks_ms() - last_enemy > 500:
        if move_enemies():
            game_state = "OVER"
            beep(400, 300)
        last_enemy = time.ticks_ms()

    if not enemies:
        level += 1; enemy_speed += 1; spawn()

    if explosions and random.random() < 0.5:
        explosions.pop()

    if enemies and time.ticks_ms() - last_enemy_shot > 1000:
        shooter = random.choice(enemies)
        enemy_bullets.append([shooter[0]+EW//2, shooter[1]+EH])
        last_enemy_shot = time.ticks_ms()

    for b in enemy_bullets:
        b[1] += 2
    enemy_bullets[:] = [b for b in enemy_bullets if b[1] < PY + 6]

    for b in enemy_bullets:
        if player_x < b[0] < player_x + PW and PY < b[1] < PY + 5:
            game_state = "OVER"
            beep(200, 300)

def draw():
    oled.fill(0)
    if game_state == "MENU":
        oled.text("SPACE INVADERS", 14, 5)
        for i, item in enumerate(menu_items):
            prefix = ">" if i == menu_idx else " "
            oled.text(f"{prefix} {item}", 10, 20 + i * 12)
        if menu_items[menu_idx] == "Level Select":
            oled.text(f"Level: {selected_level}", 60, 45)
    elif game_state == "HIGH SCORE":
        oled.text("HIGH SCORE", 30, 20)
        oled.text(str(high_score), 50, 35)
        oled.text("Press btn", 20, 50)
    elif game_state == "PLAY":
        oled.text(f"S:{score}", 0, 0); draw_batt()
        oled.text(f"Lv{level}", 70, 0)
        oled.line(player_x+5, PY, player_x, PY+4, 1)
        oled.line(player_x+5, PY, player_x+10, PY+4, 1)
        oled.line(player_x, PY+4, player_x+10, PY+4, 1)
        for b in bullets:
            oled.fill_rect(b[0], b[1], 2, 4, 1)
        for e in enemies:
            oled.fill_rect(e[0], e[1], EW, EH, 1)
        for ex in explosions:
            oled.rect(ex[0], ex[1], 6, 6, 1)
        for b in enemy_bullets:
            oled.fill_rect(b[0], b[1], 2, 4, 1)
    elif game_state == "OVER":
        oled.text("GAME OVER", 25, 20)
        oled.text(f"S:{score}", 25, 35)
        oled.text("Press btn", 25, 50)
    oled.show()

# --- Startup ---
load_hs()
draw()
play_rttl(starwars)

# --- Main Loop ---
while True:
    d = rot.get()
    pb = not btn_enc.value()

    if game_state == "MENU":
        if d != 0:
            menu_idx = (menu_idx + d) % len(menu_items)
        if pb:
            item = menu_items[menu_idx]
            if item == "Start Game":
                level = selected_level; reset(); game_state = "PLAY"
            elif item == "High Score":
                game_state = "HIGH SCORE"
            elif item == "Level Select":
                selected_level = (selected_level + 1) % 6 or 1
        draw()

    elif game_state == "HIGH SCORE":
        if pb: game_state = "MENU"
        draw()

    elif game_state == "PLAY":
        step = rot.get()
        if step < 0:
            player_x = max(0, player_x - 5)
        elif step > 0:
            player_x = min(W - PW, player_x + 5)
        if pb and time.ticks_ms() - last_shot > 400:
            bullets.append([player_x + 4, PY - 5])
            beep(2000, 30); last_shot = time.ticks_ms()
        update(); draw()
        if score > high_score:
            high_score = score
            save_hs()

    elif game_state == "OVER":
        if pb:
            game_state = "MENU"
        draw()

    time.sleep_ms(30)
