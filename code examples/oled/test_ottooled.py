# ============================================================
# test_ottooled.py
# OttoOled v0.3 test program
# ============================================================

import time
from ottooled import OttoOled


# ------------------------------------------------------------
# CHANGE THESE TO YOUR ESP32 PINS
# ------------------------------------------------------------

SDA_PIN = 21
SCL_PIN = 22


oled = OttoOled(
    sda=SDA_PIN,
    scl=SCL_PIN
)


# ------------------------------------------------------------
# TEST HELPERS
# ------------------------------------------------------------

def wait(seconds=1):
    time.sleep(seconds)


def title(text):
    oled.clear()
    oled.text(
        text,
        64,
        0,
        size=1,
        align="center"
    )
    oled.show()
    wait(1)


# ============================================================
# 1. BASIC PIXELS
# ============================================================

title("PIXELS")

oled.pixel(0, 0, 1)
oled.pixel(127, 0, 1)
oled.pixel(0, 63, 1)
oled.pixel(127, 63, 1)
oled.pixel(64, 32, 1)

oled.show()
wait(2)


# ============================================================
# 2. LINES
# ============================================================

title("LINES")

oled.line(0, 0, 127, 63)
oled.line(127, 0, 0, 63)
oled.line(0, 32, 127, 32)
oled.line(64, 0, 64, 63)

oled.show()
wait(2)


# ============================================================
# 3. RECTANGLES
# ============================================================

title("RECT")

oled.rect(10, 20, 30, 20)
oled.rect(88, 20, 30, 20)
oled.fillRect(48, 24, 32, 16)

oled.show()
wait(2)


# ============================================================
# 4. ELLIPSES
# ============================================================

title("ELLIPSES")

oled.ellipse(10, 20, 25, 15)
oled.ellipse(50, 20, 28, 20)
oled.ellipse(95, 20, 25, 15)

oled.show()
wait(2)


# ============================================================
# 5. ORIGINAL OTTO CIRCLES
# ============================================================

title("OTTO CIRCLES")

oled.circleDisplay(30, 17, 17)
oled.circleBlackDisplay(30, 14, 10)

oled.circleDisplay(98, 17, 17)
oled.circleBlackDisplay(98, 14, 10)

oled.show()
wait(2)


# ============================================================
# 6. POLYGON
# ============================================================

title("POLYGON")

oled.polygon([
    (20, 50),
    (40, 20),
    (60, 50)
])

oled.show()
wait(2)


# ============================================================
# 7. MULTIPLE POLYGONS
# ============================================================

title("POLYGONS")

oled.polygon([
    (10, 50),
    (25, 20),
    (40, 50)
])

oled.polygon([
    (88, 50),
    (103, 20),
    (118, 50)
])

oled.show()
wait(2)


# ============================================================
# 8. CELL BITMAP
# ============================================================

title("CELL BITMAP")

bitmap = (
    "0000000000000000"
    "0011110000111100"
    "0111111001111110"
    "1111111111111111"
    "1111111111111111"
    "0111111001111110"
    "0011110000111100"
    "0001100000011000"
)

oled.bitmap(
    bitmap,
    cols=16,
    cell=4,
    x=32,
    y=20
)

oled.show()
wait(2)


# ============================================================
# 9. RAW PIXEL DATA
# ============================================================

title("PIXELS DATA")

pixels = (
    "000000000000000000000000"
    "000000111111000000111111"
    "000001111111100001111111"
    "000011111111110011111111"
    "000001111111100001111111"
    "000000111111000000111111"
)

oled.pixels(
    pixels,
    cols=24,
    x=40,
    y=20
)

oled.show()
wait(2)


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
wait(2)


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
wait(2)


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
wait(2)


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
wait(2)


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
wait(2)


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
wait(2)


# ============================================================
# 16. ORIGINAL EYE SET
# ============================================================

title("EYES 1")

oled.clear()
oled.Eyes1Draw()
oled.show()
wait(2)


title("EYES 2")

oled.clear()
oled.Eyes2Draw()
oled.show()
wait(2)


title("EYES 3")

oled.clear()
oled.Eyes3Draw()
oled.show()
wait(2)


title("EYES 4")

oled.clear()
oled.Eyes4Draw()
oled.show()
wait(2)


title("EYES 5")

oled.clear()
oled.Eyes5Draw()
oled.show()
wait(2)


title("EYES 6")

oled.clear()
oled.Eyes6Draw()
oled.show()
wait(2)


# ============================================================
# 17. ORIGINAL MOUTH SET
# ============================================================

title("MOUTH 1")

oled.clear()
oled.Mouth1Draw()
oled.show()
wait(1)


title("MOUTH 2")

oled.clear()
oled.Mouth2Draw()
oled.show()
wait(1)


title("MOUTH 3")

oled.clear()
oled.Mouth3Draw()
oled.show()
wait(1)


title("MOUTH 4")

oled.clear()
oled.Mouth4Draw()
oled.show()
wait(1)


title("MOUTH 5")

oled.clear()
oled.Mouth5Draw()
oled.show()
wait(1)


title("MOUTH 6")

oled.clear()
oled.Mouth6Draw()
oled.show()
wait(2)


# ============================================================
# 18. NEW PERSONALITY PARTS
# ============================================================

title("HAPPY EYES")
oled.clear()
oled.EyesHappyDraw()
oled.show()
wait(1)

title("SLEEPY EYES")
oled.clear()
oled.EyesSleepyDraw()
oled.show()
wait(1)

title("WORRIED EYES")
oled.clear()
oled.EyesWorriedDraw()
oled.show()
wait(1)

title("ANGRY EYES")
oled.clear()
oled.EyesAngryDraw()
oled.show()
wait(1)

title("COOL EYES")
oled.clear()
oled.EyesCoolDraw()
oled.show()
wait(1)

title("WINK EYES")
oled.clear()
oled.EyesWinkDraw()
oled.show()
wait(1)

title("LOVE EYES")
oled.clear()
oled.EyesLoveDraw()
oled.show()
wait(1)

title("CONFUSED EYES")
oled.clear()
oled.EyesConfusedDraw()
oled.show()
wait(1)

title("SAD EYES")
oled.clear()
oled.EyesSadDraw()
oled.show()
wait(1)

title("ROBOT EYES")
oled.clear()
oled.EyesRobotDraw()
oled.show()
wait(2)


# ============================================================
# 19. COMPLETE PERSONALITIES
# ============================================================

faces = [
    "neutral",
    "happy",
    "excited",
    "sleepy",
    "worried",
    "angry",
    "surprised",
    "cool",
    "wink",
    "love",
    "confused",
    "sad",
    "robot"
]

for expression in faces:

    title("FACE " + expression.upper())

    oled.face(expression)
    oled.show()

    wait(2)


# ============================================================
# 20. BLINK
# ============================================================

title("BLINK")

oled.animate(
    "blink",
    speed=0.15,
    repeat=3
)

wait(1)


# ============================================================
# 21. WINK
# ============================================================

title("WINK")

oled.animate(
    "wink",
    speed=0.3,
    repeat=3
)


# ============================================================
# 22. LOOK UP
# ============================================================

title("LOOK UP")

oled.animate(
    "look_up",
    speed=0.3,
    repeat=3
)


# ============================================================
# 23. LOOK DOWN
# ============================================================

title("LOOK DOWN")

oled.animate(
    "look_down",
    speed=0.3,
    repeat=3
)


# ============================================================
# 24. SQUINT
# ============================================================

title("SQUINT")

oled.animate(
    "squint",
    speed=0.3,
    repeat=3
)


# ============================================================
# 25. SURPRISE
# ============================================================

title("SURPRISE")

oled.animate(
    "surprise",
    speed=0.25,
    repeat=3
)


# ============================================================
# 26. HAPPY
# ============================================================

title("HAPPY")

oled.animate(
    "happy",
    speed=0.25,
    repeat=3
)


# ============================================================
# 27. SLEEP
# ============================================================

title("SLEEP")

oled.animate(
    "sleep",
    speed=0.5
)

wait(2)


# ============================================================
# 28. CONFUSED
# ============================================================

title("CONFUSED")

oled.animate(
    "confused",
    speed=0.5,
    repeat=3
)


# ============================================================
# 29. LOVE
# ============================================================

title("LOVE")

oled.animate(
    "love",
    speed=0.3,
    repeat=3
)


# ============================================================
# 30. FINAL FACE
# ============================================================

oled.clear()

oled.text(
    "OTTO",
    64,
    2,
    size=2,
    align="center"
)

oled.face("happy")

oled.text(
    "READY!",
    64,
    55,
    align="center"
)

oled.show()

wait(3)


# ============================================================
# 31. SUCCESS
# ============================================================

oled.clear()

oled.text(
    "TEST",
    64,
    8,
    size=2,
    align="center"
)

oled.text(
    "COMPLETE",
    64,
    32,
    size=2,
    align="center"
)

oled.show()

print("OttoOled v0.3 test complete.")
