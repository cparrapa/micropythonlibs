# main.py
from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import time, ujson, os, math

# === Hardware ===
WIDTH, HEIGHT = 128, 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

btn_a = Pin(14, Pin.IN, Pin.PULL_UP)  # Menu scroll
btn_b = Pin(27, Pin.IN, Pin.PULL_UP)  # Menu select
buzzer = PWM(Pin(25))
buzzer.duty(0)

# === Save State ===
FILE = "otto_state.json"
pet = {
    "hunger": 100,
    "happiness": 100,
    "level": 1,
    "poops": 0,
    "awake": True,
    "last_tick": time.time()
}

menu = ["Feed", "Play", "Clean", "Sleep"]
menu_index = 0

# === Utils ===
def beep(freq=1000, dur=100):
    buzzer.freq(freq)
    buzzer.duty(200)
    time.sleep_ms(dur)
    buzzer.duty(0)

def save():
    with open(FILE, "w") as f:
        ujson.dump(pet, f)

def load():
    global pet
    if FILE in os.listdir():
        with open(FILE) as f:
            loaded = ujson.load(f)
        for key in pet:
            if key not in loaded:
                loaded[key] = pet[key]
        pet.update(loaded)

def reset():
    global pet
    pet = {
        "hunger": 100,
        "happiness": 100,
        "level": 1,
        "poops": 0,
        "awake": True,
        "last_tick": time.time()
    }
    save()

# === Drawing Helpers ===
def draw_circle(xc, yc, r, color=1):
    for angle in range(0, 360, 5):
        x = int(xc + r * math.cos(math.radians(angle)))
        y = int(yc + r * math.sin(math.radians(angle)))
        oled.pixel(x, y, color)

def draw_filled_circle(xc, yc, r, color=1):
    for y in range(-r, r):
        for x in range(-r, r):
            if x*x + y*y <= r*r:
                oled.pixel(xc + x, yc + y, color)

def draw_arc(xc, yc, r, start, end, color=1):
    for angle in range(start, end):
        x = int(xc + r * math.cos(math.radians(angle)))
        y = int(yc + r * math.sin(math.radians(angle)))
        oled.pixel(x, y, color)

# === Otto Drawing ===
def draw_otto():
    oled.fill(0)
    oled.text(f"Lvl {pet['level']}", 0, 0)

    # Head
    draw_filled_circle(64, 32, 16, 1)

    # Eyes
    oled.fill_rect(58, 26, 3, 3, 0)
    oled.fill_rect(70, 26, 3, 3, 0)

    # Mood-based mouth
    if pet['happiness'] > 70:
        draw_arc(64, 40, 6, 0, 180, 0)
    elif pet['happiness'] < 30:
        draw_arc(64, 44, 6, 180, 360, 0)
    else:
        oled.hline(58, 40, 12, 0)

    for i in range(pet['poops']):
        oled.text("*", 10 + i*6, 50)

    draw_bars()
    oled.text(menu[menu_index], 90, 0)
    oled.show()

def draw_bars():
    oled.text("H", 0, 12)
    oled.rect(10, 12, 40, 6, 1)
    oled.fill_rect(11, 13, int(pet["hunger"] * 0.38), 4, 1)
    oled.text("M", 0, 20)
    oled.rect(10, 20, 40, 6, 1)
    oled.fill_rect(11, 21, int(pet["happiness"] * 0.38), 4, 1)

# === Animations ===
def anim_eat():
    for _ in range(2):
        draw_filled_circle(64, 32, 16, 0)
        draw_arc(64, 32, 16, 45, 315, 1)
        oled.show()
        beep(500)
        time.sleep(0.2)
        draw_filled_circle(64, 32, 16, 1)
        oled.fill_rect(58, 26, 3, 3, 0)
        oled.fill_rect(70, 26, 3, 3, 0)
        oled.show()
        time.sleep(0.2)

def anim_play():
    for i in range(3):
        draw_filled_circle(64, 32, 16, 0)
        draw_filled_circle(64, 32 + i % 2 * 2, 16, 1)
        oled.fill_rect(58, 26 + i % 2, 3, 3, 0)
        oled.fill_rect(70, 26 + i % 2, 3, 3, 0)
        oled.show()
        beep(800 + i * 100)
        time.sleep(0.2)

def anim_clean():
    oled.fill(0)
    for i in range(3):
        oled.text("CLEANING", 30, 30)
        oled.show()
        beep(1000 + i * 200)
        time.sleep(0.2)
        oled.fill(0)
        oled.show()
        time.sleep(0.1)

# === Sleep Logic ===
def sleep_check():
    t = time.localtime()
    pet["awake"] = not (t[3] >= 22 or t[3] < 7)

# === Boot Screen ===
def startup():
    oled.fill(0)
    oled.text("OTTO v2", 35, 10)
    oled.text("Hold both btns", 10, 30)
    oled.text("to reset", 35, 40)
    oled.show()
    time.sleep(2)
    if not btn_a.value() and not btn_b.value():
        reset()
        oled.fill(0)
        oled.text("Resetting...", 20, 30)
        oled.show()
        time.sleep(1)

# === Main Game Loop ===
def main():
    global menu_index
    startup()
    load()
    last_update = time.time()

    while True:
        sleep_check()

        if time.time() - last_update > 10:
            pet["hunger"] = max(0, pet["hunger"] - 1)
            pet["happiness"] = max(0, pet["happiness"] - 1)
            if pet["hunger"] < 50 and pet["poops"] < 5:
                pet["poops"] += 1
            if pet["happiness"] > 80 and pet["hunger"] > 80:
                pet["level"] = min(10, pet["level"] + 1)
            save()
            last_update = time.time()

        if not btn_a.value():
            menu_index = (menu_index + 1) % len(menu)
            beep(800)
            time.sleep(0.3)

        if not btn_b.value():
            action = menu[menu_index]
            if action == "Feed":
                pet["hunger"] = min(100, pet["hunger"] + 20)
                anim_eat()
            elif action == "Play":
                pet["happiness"] = min(100, pet["happiness"] + 20)
                anim_play()
            elif action == "Clean":
                pet["poops"] = 0
                anim_clean()
            elif action == "Sleep":
                pet["awake"] = not pet["awake"]
                beep(200)
            save()
            time.sleep(0.3)

        draw_otto()
        time.sleep(0.1)

main()
