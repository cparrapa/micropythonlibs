from machine import Pin, I2C, PWM
import time
import ssd1306
import framebuf
import urandom

# === Display Setup ===
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# === Button Pins ===
btn_up = Pin(26, Pin.IN, Pin.PULL_UP)
btn_down = Pin(27, Pin.IN, Pin.PULL_UP)
btn_trigger = Pin(15, Pin.IN, Pin.PULL_UP)

# === Buzzer ===
buzzer = PWM(Pin(25))
buzzer.duty(0)

# === Bitmaps ===
storm = bytearray([
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
    0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7F,0xFE,0x00,0x00,
    0x00,0x07,0x80,0x01,0xE0,0x00,0x00,0x0C,0x00,0x00,0x20,0x00,
    0x00,0x18,0x00,0x00,0x18,0x00,0x00,0x30,0x00,0x00,0x04,0x00,
    0x00,0x20,0x00,0x00,0x04,0x00,0x00,0x20,0x00,0x00,0x04,0x00
])
storm_buf = framebuf.FrameBuffer(storm, 16, 16, framebuf.MONO_HLSB)
icon = bytearray([
    0x00, 0x00, 0x1C, 0x00, 0x3F, 0xF0, 0x3C, 0x00,
    0x3C, 0x00, 0xFF, 0x00, 0x7F, 0xFF, 0xFF, 0x00,
    0x3C, 0x00, 0x3C, 0x00, 0x1F, 0xF0, 0x1C, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
])
icon_buf = framebuf.FrameBuffer(icon, 16, 16, framebuf.MONO_HLSB)

# === Helpers ===
def beep(freq, duration):
    buzzer.freq(freq)
    buzzer.duty(200)
    time.sleep_ms(duration)
    buzzer.duty(0)
    time.sleep_ms(50)

def fill_circle(oled, x0, y0, r, color):
    for y in range(-r, r + 1):
        for x in range(-r, r + 1):
            if x * x + y * y <= r * r:
                oled.pixel(x0 + x, y0 + y, color)

# === Game Variables ===
pos = 30
metx, mety = 0, 0
postoji = 0
rx, ry = 95, 0
rx2, ry2 = 95, 0
rx3, ry3 = 95, 0
rx4, ry4 = 95, 0
ispaljeno = 0
brzina = 3
bkugle = 1
promjer = 10
zivoti = 5
nivo = 1
bodovi = 0
centar = 95
nep = 8
smjer = 0
go = 0
poc = 0
pocetno = 0
odabrano = 0
nivovrijeme = 0
deathx, deathy = centar, nep  # enemy shooter coords
death_bx, death_by = deathx, deathy
can_shoot = True

# === Timing ===
def ticks():
    return time.ticks_ms()

# === Wait for Start Menu ===
oled.fill(0)
oled.text("xWing vs Death Star", 5, 10)
oled.text("Press Trigger", 20, 30)
oled.text("to Start", 40, 45)
oled.show()
while btn_trigger.value():
    time.sleep_ms(10)
beep(1000, 150)

# === Main Loop ===
while True:
    if go == 0:
        oled.fill(0)

        # Optional: Show stormtrooper at boot once
        if nivo == 1 and bodovi == 0:
            oled.blit(storm_buf, 40, 8)
            oled.text("xWing vs Death Star", 5, 0)
            oled.show()
            time.sleep(2)

        # spawn enemy at random
        now = ticks()
        if poc == 0:
            pocetno = now
            odabrano = urandom.getrandbits(10) % 800 + 400  # 400-1200ms
            poc = 1

        if time.ticks_diff(now, pocetno) > odabrano:
            poc = 0
            ispaljeno += 1
            if ispaljeno == 1:
                rx, ry = 95, nep
            elif ispaljeno == 2:
                rx2, ry2 = 95, nep
            elif ispaljeno == 3:
                rx3, ry3 = 95, nep
            elif ispaljeno == 4:
                rx4, ry4 = 95, nep

        if ispaljeno > 0:
            oled.pixel(rx, ry, 1)
            rx -= brzina
        if ispaljeno > 1:
            oled.pixel(rx2, ry2, 1)
            rx2 -= brzina
        if ispaljeno > 2:
            oled.pixel(rx3, ry3, 1)
            rx3 -= brzina
        if ispaljeno > 3:
            oled.pixel(rx4, ry4, 1)
            rx4 -= brzina

        # Player movement
        if not btn_up.value() and pos >= 2:
            pos -= 2
        if not btn_down.value() and pos <= 46:
            pos += 2

        # Shooting
        if not btn_trigger.value() and not postoji:
            postoji = 1
            metx, mety = 6, pos + 8
            beep(1200, 20)

        if postoji:
            metx += 8
            oled.hline(metx, mety, 4, 1)

        # Death Star fires
        if can_shoot:
            death_bx, death_by = centar, nep
            can_shoot = False
        else:
            death_bx -= 4
            oled.pixel(death_bx, death_by, 1)
            if death_bx < 0:
                can_shoot = True

        # Collision: enemy bullet vs player
        if 4 < death_bx < 20 and pos < death_by < pos + 16:
            zivoti -= 1
            beep(150, 100)
            can_shoot = True

        # Draw player and enemy
        oled.blit(icon_buf, 4, pos)
        fill_circle(oled, centar, nep, promjer, 1)
        fill_circle(oled, centar+2, nep+3, promjer//3, 0)

        # UI
        oled.text(f"Score: {bodovi}", 33, 56)
        oled.text(f"Lives: {zivoti}", 0, 0)
        oled.text(f"L:{nivo}", 100, 0)
        oled.text(str(ticks() // 1000), 108, 56)

        oled.show()

        # Logic
        if metx > 128:
            postoji = 0
        nep += bkugle if smjer == 0 else -bkugle
        if nep >= 64 - promjer:
            smjer = 1
        if nep <= promjer:
            smjer = 0

        if postoji and mety in range(nep - promjer, nep + promjer + 1) and centar - promjer < metx < centar + promjer:
            beep(500, 20)
            bodovi += 1
            postoji = 0

        if ticks() - nivovrijeme > 50000:
            nivovrijeme = ticks()
            nivo += 1
            brzina += 1
            if nivo % 2 == 0:
                bkugle += 1
                promjer = max(2, promjer - 1)

        if zivoti == 0:
            go = 1

    else:
        oled.fill(0)
        oled.text("GAME OVER!", 7, 10)
        oled.text(f"Score: {bodovi}", 7, 30)
        oled.text(f"Level: {nivo}", 7, 40)
        oled.text(f"Time: {ticks()//1000}s", 7, 50)
        oled.show()
        if not btn_trigger.value():
            beep(280, 300)
            beep(250, 200)
            beep(370, 300)
            # Reset state
            metx = mety = postoji = ispaljeno = poc = bodovi = 0
            rx = ry = rx2 = ry2 = rx3 = ry3 = rx4 = ry4 = 95
            brzina = 3
            bkugle = 1
            promjer = 12
            zivoti = 5
            nivo = 1
            nep = 8
            smjer = 0
            pocetno = odabrano = nivovrijeme = 0
            go = 0
            can_shoot = True

    time.sleep_ms(30)

