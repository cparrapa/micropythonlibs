
# ============================================================
# OttoOled v0.2.0
# Complete Library Test
# ESP32 + SSD1306 128x64 OLED
# ============================================================

from ottooled import OttoOled
import time


# ------------------------------------------------------------
# SETUP
# ------------------------------------------------------------

oled = OttoOled(
    sda=21,
    scl=22
)


# ------------------------------------------------------------
# HELPER
# ------------------------------------------------------------

def title(text):
    oled.clear()
    oled.text(text, 0, 0)
    oled.show()

def wait():
    time.sleep(0.4)


# ============================================================
# 11. TEXT - SIZE 2
# ============================================================

title("TEXT SIZE 2")

oled.clear()

oled.text(
    "OTTO",
    64,
    10,
    size=2,
    align="center"
)

oled.show()
wait()


# ============================================================
# 12. TEXT - SIZE 3
# ============================================================

title("TEXT SIZE 3")

oled.clear()

oled.text(
    "OK",
    64,
    12,
    size=3,
    align="center"
)

oled.show()
wait()


# ============================================================
# 13. TEXT ALIGNMENT
# ============================================================

title("ALIGN")

oled.clear()

oled.text(
    "LEFT",
    0,
    12,
    align="left"
)

oled.text(
    "CENTER",
    64,
    28,
    align="center"
)

oled.text(
    "RIGHT",
    128,
    44,
    align="right"
)

oled.show()
wait()


# ============================================================
# 14. MULTILINE TEXT
# ============================================================

title("TEXT BOX")

oled.clear()

oled.textBox(
    "HELLO\nOTTO!",
    64,
    10,
    size=2,
    align="center",
    line_spacing=2
)

oled.show()
wait()


# ============================================================
# 15. TEXT + GRAPHICS
# ============================================================

title("TEXT + GRAPHICS")

oled.clear()

oled.text(
    "OTTO",
    64,
    2,
    size=2,
    align="center"
)

oled.rect(
    4,
    22,
    120,
    38
)

oled.text(
    "ROBOT",
    64,
    38,
    align="center"
)

oled.show()
wait()



# ============================================================
# TEST 1 — PIXELS
# ============================================================

title("TEST 1: PIXELS")

oled.pixel(0, 0)
oled.pixel(127, 0)
oled.pixel(0, 63)
oled.pixel(127, 63)

oled.pixel(64, 32)

oled.show()

wait()

oled.clear()


# ============================================================
# TEST 2 — LINES
# ============================================================

title("TEST 2: LINES")

oled.line(0, 10, 127, 10)
oled.line(0, 20, 127, 50)
oled.line(0, 50, 127, 20)

oled.line(10, 15, 10, 55)
oled.line(118, 15, 118, 55)

oled.show()

wait()


# ============================================================
# TEST 3 — RECTANGLES
# ============================================================

title("TEST 3: RECT")

oled.rect(
    5, 15,
    35, 25
)

oled.rect(
    50, 15,
    35, 25,
    1,
    True
)

oled.fillRect(
    95, 15,
    25, 25,
    1
)

oled.show()

wait()


# ============================================================
# TEST 4 — ELLIPSES
# ============================================================

title("TEST 4: ELLIPSE")

# Outline circle
oled.ellipse(
    5, 15,
    25, 25
)

# Filled circle
oled.ellipse(
    38, 15,
    25, 25,
    1,
    True
)

# Wide ellipse
oled.ellipse(
    72, 15,
    50, 25
)

oled.show()

wait()


# ============================================================
# TEST 5 — TEXT
# ============================================================

title("TEST 5: TEXT")

oled.text(
    "OttoOled",
    25,
    15
)

oled.text(
    "v0.2.0",
    40,
    30
)

oled.text(
    "TEST OK",
    32,
    48
)

oled.show()

wait()


# ============================================================
# TEST 6 — POLYGON
# ============================================================

title("TEST 6: POLYGON")

# Triangle
oled.polygon([
    (64, 12),
    (90, 45),
    (38, 45)
])

oled.show()

wait()


# ============================================================
# TEST 7 — MULTIPLE POLYGONS
# ============================================================

title("TEST 7: POLYGONS")

# Diamond
oled.polygon([
    (64, 8),
    (90, 32),
    (64, 56),
    (38, 32)
])

# Small triangle
oled.polygon([
    (20, 20),
    (30, 30),
    (10, 30)
])

oled.show()

wait()


# ============================================================
# TEST 8 — PIXEL BITMAP
# ============================================================

title("TEST 8: PIXELS")

# Small pixel-art heart
heart = (
    "01100110"
    "11111111"
    "11111111"
    "01111110"
    "00111100"
    "00011000"
)

oled.pixels(
    heart,
    cols=8,
    x=60,
    y=15
)

wait()
oled.pixels(
    "0000000000000000"
    "0011111111111100"
    "0110000000000110"
    "1100110000110011"
    "1100110000110011"
    "1100000000000011"
    "0110001111000110"
    "0011111111111100",
    cols=16,
    x=48,
    y=10
)

time.sleep(0.5)


# =========================================================
# 7. CELL BITMAP
# =========================================================

oled.clear()

oled.bitmap(
    "00111100"
    "01111110"
    "11111111"
    "11111111"
    "11011011"
    "11111111"
    "01111110"
    "00111100",
    cols=8,
    cell=4,
    x=48,
    y=16
)

time.sleep(0.5)



# ============================================================
# TEST 9 — CELL BITMAP
# ============================================================

title("TEST 9: BITMAP")

# 8x8 smiley
smiley = (
    "00111100"
    "01111110"
    "11011011"
    "11111111"
    "11100111"
    "11111111"
    "01111110"
    "00111100"
)

oled.bitmap(
    smiley,
    cols=8,
    cell=4,
    x=48,
    y=15
)

wait()


# ============================================================
# TEST 10 — NORMAL EYES
# ============================================================

title("TEST 10: EYES")

oled.eyes()

oled.show()

wait()


# ============================================================
# TEST 11 — CLOSED EYES
# ============================================================

title("TEST 11: CLOSED")

oled.eyesClosed()

oled.show()

wait()


# ============================================================
# TEST 12 — LOOK UP
# ============================================================

title("TEST 12: UP")

oled.eyesUp()
oled.show()
wait()
oled.eyesUp2()
oled.show()
wait()

# ============================================================
# TEST 13 — LOOK DOWN
# ============================================================

title("TEST 13: DOWN")

oled.eyesDown()
oled.show()
wait()
oled.eyesDown2()
oled.show()
wait()

# ============================================================
# TEST 14 — WINK LEFT
# ============================================================

title("TEST 14: WINK L")

oled.eyesWinkLeft()

oled.show()

wait()


# ============================================================
# TEST 15 — WINK RIGHT
# ============================================================

title("TEST 15: WINK R")

oled.eyesWinkRight()

oled.show()

wait()


# ============================================================
# TEST 16 — ANGRY
# ============================================================

title("TEST 16: ANGRY")

oled.eyesAngry()

oled.show()

wait()


# ============================================================
# TEST 17 — WORRIED
# ============================================================

title("TEST 17: WORRIED")

oled.eyesWorry()

oled.show()

wait()


# ============================================================
# TEST 18 — MOUTHS
# ============================================================

title("TEST 18: MOUTHS")

oled.eyes()
oled.mouth()

oled.show()

wait()


title("SMILE")

oled.eyes()
oled.mouthSmile()

oled.show()

wait()


title("OPEN")

oled.eyes()
oled.mouthSad()

oled.show()

wait()


title("BIG SMILE")

oled.eyes()
oled.mouthHappy()

oled.show()

wait()


title("MOUTH LEFT")

oled.eyes()
oled.mouthLeft()

oled.show()

wait()


title("MOUTH RIGHT")

oled.eyes()
oled.mouthRight()

oled.show()

wait()


# ============================================================
# TEST 19 — COMPLETE FACES
# ============================================================

faces = [
    "neutral",
    "happy",
    "surprised",
    "sleepy",
    "angry",
    "worried",
    "wink_left",
    "wink_right"
]

for expression in faces:

    oled.clear()

    oled.face(expression)

    oled.show()

    time.sleep(1)


# ============================================================
# TEST 20 — BLINK
# ============================================================

oled.clear()
oled.face("neutral")
oled.show()

time.sleep(1)

oled.animate(
    "blink",
    speed=0.15
)

wait()


# ============================================================
# TEST 21 — WINK ANIMATIONS
# ============================================================

oled.face("neutral")
oled.show()

time.sleep(0.5)

oled.animate(
    "wink_left",
    speed=0.2
)

time.sleep(0.5)

oled.animate(
    "wink_right",
    speed=0.2
)

wait()


# ============================================================
# TEST 22 — LOOK AROUND
# ============================================================

oled.face("neutral")
oled.show()

time.sleep(0.5)

oled.animate(
    "look_up",
    speed=0.15
)

time.sleep(0.5)

oled.animate(
    "look_down",
    speed=0.15
)

wait()


# ============================================================
# TEST 23 — SURPRISE
# ============================================================

oled.animate(
    "surprise",
    speed=0.15
)

wait()


# ============================================================
# TEST 24 — HAPPY
# ============================================================

oled.animate(
    "happy",
    speed=0.2,
    repeat=3
)

wait()


# ============================================================
# TEST 25 — ANIMATION SEQUENCE
# ============================================================

oled.face("neutral")
oled.show()

time.sleep(1)

oled.animate("blink", 0.1)
oled.animate("look_up", 0.1)
oled.animate("look_down", 0.1)
oled.animate("wink_left", 0.15)
oled.animate("wink_right", 0.15)
oled.animate("surprise", 0.15)
oled.animate("happy", 0.2)

wait()

# =========================================================
# 12. ANIMATIONS
# =========================================================

oled.animate(
    "blink",
    speed=0.15,
    repeat=3
)

oled.animate(
    "wink_left",
    speed=0.2
)

oled.animate(
    "wink_right",
    speed=0.2
)

oled.animate(
    "look_up",
    speed=0.15
)

oled.animate(
    "look_down",
    speed=0.15
)

oled.animate(
    "surprise",
    speed=0.15
)

oled.animate(
    "happy",
    speed=0.2
)

# ============================================================
# TEST 27 — FINAL FACE
# ============================================================

oled.clear()

oled.face("happy")

oled.show()

time.sleep(2)


# ============================================================
# DONE
# ============================================================

oled.clear()

oled.text(
    "ALL TESTS",
    30,
    15
)

oled.text(
    "COMPLETE!",
    25,
    35
)

oled.show()

time.sleep(3)

oled.clear()
oled.show()

# ============================================================
# 10. TEXT - NORMAL
# ============================================================

title("TEXT")

oled.clear()

oled.text(
    "Hello",
    10,
    10
)

oled.text(
    "Otto!",
    10,
    25
)

oled.show()
wait()

