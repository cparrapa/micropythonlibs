import machine, neopixel, time, framebuf, math

# Config
PIN = 22         # NeoPixel data pin
BUZZER_PIN = 25
WIDTH, HEIGHT = 8, 8
NUM_LEDS = WIDTH * HEIGHT
BRIGHTNESS = 0.3  # 0 to 1.0

# Setup
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_LEDS)
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)

# Pixel Mapping
def xy_to_index(x, y):
    return y * WIDTH + (x if y % 2 == 0 else WIDTH - 1 - x)

# Draw 8x8 Bitmap
def draw_bitmap(bitmap, color=(255, 255, 255)):
    np.fill((0, 0, 0))
    for y in range(8):
        row = bitmap[y]
        for x in range(8):
            if (row >> (7 - x)) & 1:
                idx = xy_to_index(x, y)
                np[idx] = tuple(int(BRIGHTNESS * c) for c in color)
    np.write()

# Interpolated transition between two frames
def interpolate_frames(f1, f2, steps=5, color1=(255,255,255), color2=(255,255,255)):
    for step in range(steps):
        np.fill((0, 0, 0))
        for y in range(8):
            r1 = f1[y]
            r2 = f2[y]
            for x in range(8):
                p1 = (r1 >> (7 - x)) & 1
                p2 = (r2 >> (7 - x)) & 1
                v = p1 * (1 - step/steps) + p2 * (step/steps)
                if v > 0.5:
                    idx = xy_to_index(x, y)
                    c = tuple(int(BRIGHTNESS * ((1-step/steps)*color1[i] + (step/steps)*color2[i])) for i in range(3))
                    np[idx] = c
        np.write()
        time.sleep(0.05)

# Play a beep
def beep(duration=0.1):
    buzzer.value(1)
    time.sleep(duration)
    buzzer.value(0)

# Emoji Bitmaps
emoji_dict = {
    "heart":     [0x00,0x66,0xFF,0xFF,0xFF,0x7E,0x3C,0x18],
    "smile":     [0x3C,0x42,0xA5,0x81,0xA5,0x99,0x42,0x3C],
    "sad":       [0x3C,0x42,0xA5,0x81,0x99,0xA5,0x42,0x3C],
    "beer":      [0x7E,0xFF,0xFF,0xDB,0xDB,0xDB,0xFF,0x7E],
    "angry":     [0x3C,0x42,0xA5,0xBD,0x81,0xA5,0x42,0x3C],
    "surprised": [0x3C,0x42,0x81,0xBD,0xBD,0x81,0x42,0x3C],
    "like":      [0x10,0x30,0x70,0xF0,0xFE,0xFE,0x3E,0x0C]
}

emoji_colors = {
    "heart":     (255, 0, 0),
    "smile":     (255, 255, 0),
    "sad":       (0, 0, 255),
    "beer":      (255, 200, 0),
    "angry":     (255, 50, 0),
    "surprised": (0, 255, 255),
    "like":      (50, 255, 50)
}

# Animation with transition and sound
def animate_emojis(names, delay=1.0):
    for i in range(len(names)):
        name1 = names[i]
        name2 = names[(i+1)%len(names)]
        bmp1, bmp2 = emoji_dict[name1], emoji_dict[name2]
        c1, c2 = emoji_colors[name1], emoji_colors[name2]
        draw_bitmap(bmp1, c1)
        beep(0.05)
        time.sleep(delay)
        interpolate_frames(bmp1, bmp2, steps=6, color1=c1, color2=c2)

# Scrolling Text
def scroll_text(msg, color=(0, 255, 0), delay=0.08):
    fbw = len(msg)*8 + 8
    buffer = bytearray((fbw * HEIGHT) // 8)
    fb = framebuf.FrameBuffer(buffer, fbw, HEIGHT, framebuf.MONO_HLSB)
    fb.fill(0)
    fb.text(msg, 0, 0, 1)

    for shift in range(fbw - WIDTH):
        np.fill((0, 0, 0))
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if fb.pixel(x + shift, y):
                    idx = xy_to_index(x, y)
                    np[idx] = tuple(int(BRIGHTNESS * c) for c in color)
        np.write()
        time.sleep(delay)

# Main Loop
def main():
    while True:
        animate_emojis(["heart", "smile", "sad", "beer", "angry", "surprised", "like"], 0.8)
        scroll_text("Hello from ESP32!", (255, 255, 255), 1)
        beep(0.1)

# Run it
main()
