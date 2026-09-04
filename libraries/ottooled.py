# ottooled.py v0.1.2 4.9.2026 unified oled
import framebuf
import array
import time
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

class OttoOled:

    WIDTH = 128
    HEIGHT = 64

    def __init__(self, sda, scl):
        self.i2c = I2C(sda=Pin(sda), scl=Pin(scl))
        self.display = SSD1306_I2C(
            self.WIDTH,
            self.HEIGHT,
            self.i2c
        )

    # --------------------------------------------------
    # BASIC DISPLAY
    # --------------------------------------------------

    def showDisplay(self):
        self.display.show()

    def clearDisplay(self):
        self.display.fill(0)

    def pixelDisplay(self, xPos, yPos, value=1):
        self.display.pixel(xPos, yPos, value)

    def lineDisplay(self, xPos1, yPos1, xPos2, yPos2):
        self.display.line(
            xPos1, yPos1,
            xPos2, yPos2,
            1
        )

    def writeTextDisplay(self, writeValue, xPos, yPos):
        self.display.text(
            "{}".format(writeValue),
            xPos,
            yPos,
            1
        )

    # --------------------------------------------------
    # SHAPES
    # --------------------------------------------------

    def squareDisplay(self, x, y, width, height):
        self.display.rect(
            x, y, width, height, 1
        )

    def squareBlackDisplay(self, x, y, width, height):
        self.display.rect(
            x, y, width, height, 0
        )

    def squareFillDisplay(self, x, y, width, height, value):
        self.display.fill_rect(
            x, y, width, height, value
        )

    def drawCircle(self, x, y, width, height, color=1, fill=1):
        self.display.ellipse(
            x, y,
            width, height,
            color,
            fill
        )

    # Compatibility with old API
    def circleDisplay(self, x, y, r):
        self.drawCircle(x, y, r, r, 1, 1)

    def circleBlackDisplay(self, x, y, r):
        self.drawCircle(x, y, r, r, 0, 1)

    def ringDisplay(self, x, y, r):
        self.drawCircle(x, y, r, r, 1, 0)

    # --------------------------------------------------
    # POLYGONS
    # --------------------------------------------------

    def polygonDisplay(self, points, color=1, fill=True):
        """
        Draw polygon from:
        [(x1,y1), (x2,y2), (x3,y3), ...]
        """

        data = []

        for x, y in points:
            data.append(x)
            data.append(y)

        polygon = array.array('I', data)

        self.display.poly(
            0,
            0,
            polygon,
            color,
            fill
        )

    # --------------------------------------------------
    # ICON
    # --------------------------------------------------

    def ShowIcon(self, icono, x, y, w, h):
        fb = framebuf.FrameBuffer(
            icono,
            w,
            h,
            framebuf.MONO_HLSB
        )

        self.display.blit(
            fb,
            x,
            y
        )

    # ==================================================
    # OTTO FACE
    # ==================================================

    # --------------------------------------------------
    # FACE CLEARING
    # --------------------------------------------------

    def _clearEyes(self):
        self.display.fill_rect(
            16, 0,
            96, 33,
            0
        )

    def _clearFace(self):
        self.display.fill_rect(
            0, 0,
            128, 64,
            0
        )

    # --------------------------------------------------
    # EYES
    # --------------------------------------------------

    def eyes(self):
        """
        Normal Otto eyes
        """

        self._clearEyes()

        self.display.ellipse(
            32, 16,
            16, 16,
            1,
            1
        )

        self.display.ellipse(
            32, 16,
            10, 10,
            0,
            1
        )

        self.display.ellipse(
            96, 16,
            16, 16,
            1,
            1
        )

        self.display.ellipse(
            96, 16,
            10, 10,
            0,
            1
        )

    def eyesClosed(self):
        """
        Closed eyes
        """

        self._clearEyes()

        self.display.fill_rect(
            16, 16,
            32, 6,
            1
        )

        self.display.fill_rect(
            80, 16,
            32, 6,
            1
        )

    def eyesUp(self):
        self.eyes()

        self.display.fill_rect(
            0, 16,
            128, 17,
            0
        )

    def eyesUp2(self):
        self._clearEyes()

        self.display.ellipse(
            32, 32,
            16, 16,
            1,
            1
        )

        self.display.ellipse(
            32, 32,
            10, 10,
            0,
            1
        )

        self.display.ellipse(
            96, 32,
            16, 16,
            1,
            1
        )

        self.display.ellipse(
            96, 32,
            10, 10,
            0,
            1
        )

        self.display.fill_rect(
            0, 32,
            128, 17,
            0
        )

    def eyesDown(self):
        self.eyes()

        self.display.fill_rect(
            0, 0,
            128, 16,
            0
        )

    def eyesDown2(self):
        self._clearEyes()

        self.display.ellipse(
            32, 0,
            16, 16,
            1,
            1
        )

        self.display.ellipse(
            32, 0,
            10, 10,
            0,
            1
        )

        self.display.ellipse(
            96, 0,
            16, 16,
            1,
            1
        )

        self.display.ellipse(
            96, 0,
            10, 10,
            0,
            1
        )

    # --------------------------------------------------
    # WINKS
    # --------------------------------------------------

    def eyesWinkLeft(self):
        self.eyes()

        self.display.fill_rect(
            64, 0,
            64, 16,
            0
        )

    def eyesWinkRight(self):
        self.eyes()

        self.display.fill_rect(
            0, 0,
            64, 16,
            0
        )

    # --------------------------------------------------
    # EMOTIONS
    # --------------------------------------------------

    def eyesAngry(self):
        self.eyes()

        self.polygonDisplay([
            (16, 0),
            (48, 0),
            (48, 32)
        ], 0, True)

        self.polygonDisplay([
            (80, 0),
            (112, 0),
            (80, 32)
        ], 0, True)

    def eyesWorry(self):
        self.eyes()

        self.polygonDisplay([
            (16, 0),
            (48, 0),
            (16, 32)
        ], 0, True)

        self.polygonDisplay([
            (80, 0),
            (112, 0),
            (112, 32)
        ], 0, True)

    # ==================================================
    # MOUTH
    # ==================================================

    def mouth1(self):
        self.display.ellipse(
            64, 50,
            14, 14,
            1,
            1
        )

        self.display.ellipse(
            64, 50,
            10, 10,
            0,
            1
        )

        self.display.fill_rect(
            0, 36,
            128, 14,
            0
        )

    def mouth2(self):
        self.display.ellipse(
            64, 50,
            14, 14,
            1,
            1
        )

    def mouth3(self):
        self.display.ellipse(
            64, 60,
            20, 20,
            1,
            1
        )

    def mouth4(self):
        self.display.fill_rect(
            39, 54,
            50, 7,
            1
        )

    def mouth5(self):
        self.display.fill_rect(
            44, 44,
            50, 7,
            1
        )

        self.display.ellipse(
            84, 54,
            10, 10,
            1,
            1
        )

    def mouth6(self):
        self.display.fill_rect(
            44, 44,
            50, 7,
            1
        )

        self.display.ellipse(
            53, 54,
            10, 10,
            1,
            1
        )

    # ==================================================
    # SIMPLE ANIMATIONS
    # ==================================================

    def blink(self, speed=0.08):
        """
        Blink animation.
        """

        self.eyes()
        self.showDisplay()

        time.sleep(speed)

        self.eyesClosed()
        self.showDisplay()

        time.sleep(speed)

        self.eyes()
        self.showDisplay()

    def winkLeft(self, speed=0.15):
        self.eyesWinkLeft()
        self.showDisplay()

        time.sleep(speed)

        self.eyes()
        self.showDisplay()

    def winkRight(self, speed=0.15):
        self.eyesWinkRight()
        self.showDisplay()

        time.sleep(speed)

        self.eyes()
        self.showDisplay()

    def lookUp(self, speed=0.08):
        self.eyesUp2()
        self.showDisplay()

        time.sleep(speed)

        self.eyesUp()
        self.showDisplay()

    def lookDown(self, speed=0.08):
        self.eyesDown2()
        self.showDisplay()

        time.sleep(speed)

        self.eyesDown()
        self.showDisplay()

    # ==================================================
    # OLD COMPATIBILITY API
    # ==================================================

    def Draw2Eyes(self):
        self.circleDisplay(30, 17, 17)
        self.circleBlackDisplay(30, 14, 10)

        self.circleDisplay(98, 17, 17)
        self.circleBlackDisplay(98, 14, 10)

    def Eyes1Draw(self):
        self.Draw2Eyes()

    def Eyes2Draw(self):
        self.Draw2Eyes()

        self.display.fill_rect(
            0, 17,
            128, 17,
            0
        )

    def Eyes3Draw(self):
        self.Draw2Eyes()

        self.display.fill_rect(
            0, 0,
            128, 17,
            0
        )

    def Eyes4Draw(self):
        self.Draw2Eyes()

        self.display.fill_rect(
            0, 0,
            64, 17,
            0
        )

    def Eyes5Draw(self):
        self.Draw2Eyes()

        self.display.fill_rect(
            0, 0,
            36, 17,
            0
        )

        self.display.fill_rect(
            92, 0,
            36, 20,
            0
        )

    def Eyes6Draw(self):
        self.Draw2Eyes()

        self.display.fill_rect(
            24, 0,
            74, 20,
            0
        )

    def Mouth1Draw(self):
        self.mouth1()

    def Mouth2Draw(self):
        self.mouth2()

    def Mouth3Draw(self):
        self.mouth3()

    def Mouth4Draw(self):
        self.mouth4()

    def Mouth5Draw(self):
        self.mouth5()

    def Mouth6Draw(self):
        self.mouth6()
