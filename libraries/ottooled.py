# ottooled.py v0.1.3 7.9.2026 fixed faces

import time
import framebuf
import array

from machine import I2C, Pin
from ssd1306 import SSD1306_I2C


class OttoOled:

    WIDTH = 128
    HEIGHT = 64

    # Face geometry
    EYE_LEFT_X = 32
    EYE_RIGHT_X = 96
    EYE_Y = 16
    EYE_SIZE = 16
    PUPIL_SIZE = 10

    def __init__(self, sda, scl, width=128, height=64):
        self.width = width
        self.height = height

        self.i2c = I2C(
            sda=Pin(sda),
            scl=Pin(scl)
        )

        self.display = SSD1306_I2C(
            width,
            height,
            self.i2c
        )

    # =========================================================
    # DISPLAY
    # =========================================================

    def show(self):
        """Send the current framebuffer to the OLED."""
        self.display.show()

    def clear(self):
        """Clear the entire display."""
        self.display.fill(0)

    def fill(self, value=0):
        """Fill the entire display with 0 or 1."""
        self.display.fill(value)

    # =========================================================
    # BASIC DRAWING
    # =========================================================

    def pixel(self, x, y, value=1):
        self.display.pixel(x, y, value)

    def line(self, x1, y1, x2, y2, value=1):
        self.display.line(
            x1, y1,
            x2, y2,
            value
        )

    def rect(self, x, y, width, height, value=1, fill=False):
        self.display.rect(x, y,width, height,value,fill)

    def fillRect(self, x, y, width, height, value=1):
        self.display.fill_rect(
            x, y,
            width, height,
            value
        )

    def ellipse(self, x, y, width, height, value=1, fill=False):
        self.display.ellipse(
            x, y,
            width, height,
            value,
            fill
        )

    # =========================================================
    # TEXT
    # =========================================================

    def text(self, value, x, y, color=1):
        self.display.text(
            str(value),
            x,
            y,
            color
        )

    # =========================================================
    # POLYGONS
    # =========================================================

    def polygon(self, points, value=1, fill=True):
        """
        Draw a polygon.

        Example:
            oled.polygon([
                (10, 10),
                (30, 10),
                (20, 30)
            ])
        """

        data = array.array('i')

        for x, y in points:
            data.append(x)
            data.append(y)

        self.display.poly(
            0,
            0,
            data,
            value,
            fill
        )

    # =========================================================
    # BITMAPS
    # =========================================================

    def bitmap(self, cells, cols=16, cell=8,
               x=0, y=0, value=1, show=True):
        """
        Draw a bitmap made from square cells.

        '1' = filled cell
        '0' = empty cell

        Example:
            oled.bitmap(
                "00111100"
                "01111110"
                "11111111"
                "11111111",
                cols=8,
                cell=1
            )
        """

        for i, bit in enumerate(cells):

            if bit == '1':

                px = x + (i % cols) * cell
                py = y + (i // cols) * cell

                self.fillRect(
                    px,
                    py,
                    cell,
                    cell,
                    value
                )

        if show:
            self.show()

    def pixels(self, cells, cols=128,
               x=0, y=0, value=1, show=True):
        """
        Draw a 1-bit pixel bitmap.

        Example:
            oled.pixels("010101...")
        """

        for i, bit in enumerate(cells):

            if bit == '1':

                px = x + (i % cols)
                py = y + (i // cols)

                self.pixel(
                    px,
                    py,
                    value
                )

        if show:
            self.show()

    def icon(self, data, x, y, width, height,
             format=framebuf.MONO_HLSB, show=True):
        """
        Draw a raw framebuf bitmap.
        """

        fb = framebuf.FrameBuffer(
            data,
            width,
            height,
            format
        )

        self.display.blit(
            fb,
            x,
            y
        )

        if show:
            self.show()

    # =========================================================
    # FACE HELPERS
    # =========================================================

    def _clearEyes(self):
        """Clear the normal eye area."""
        self.fillRect(16, 0,96, 33,0)

    def _eye(self, x, y, pupil_x=0, pupil_y=0):
        """
        Draw one eye.
        x/y = top-left of eye.
        pupil_x/y = pupil offset inside eye.
        """
        self.ellipse(x,y,self.EYE_SIZE,self.EYE_SIZE,1,True)
        self.ellipse(x + pupil_x,y + pupil_y,self.PUPIL_SIZE,self.PUPIL_SIZE,0,True)

    def _eyes(self, y, pupil_y=0):
        """Draw both eyes."""
        self._clearEyes()
        self._eye(self.EYE_LEFT_X ,self.EYE_Y,0,pupil_y)
        self._eye(self.EYE_RIGHT_X ,self.EYE_Y,0,pupil_y)

    # =========================================================
    # EYE EXPRESSIONS
    # =========================================================

    def eyes(self):
        """Normal eyes."""
        self._eyes(16,0)

    def eyesClosed(self):
        """Closed eyes."""
        self._clearEyes()

        self.fillRect(
            16, 16,
            32, 6,
            1
        )

        self.fillRect(
            80, 16,
            32, 6,
            1
        )

    def eyesUp(self):
        """Eyes looking upward."""
        self._eyes(16, 0)

        self.fillRect(
            0, 16,
            128, 17,
            0
        )
        
    def eyesUp2(self):
        self.rect(16,0,96,33,0,True)
        self.ellipse(32,32,16,16,1,1)  
        self.ellipse(32,32,10,10,0,1)  
        self.ellipse(96,32,16,16,1,1) 
        self.ellipse(96,32,10,10,0,1)  
        self.rect(0,32,128,17,0,True)

    def eyesDown(self):
        """Eyes looking downward."""
        self._eyes(0, 0)
        self.fillRect(0, 0,128, 16,0)
        
    def eyesDown2(self):
        self.ellipse(32,0,16,16,1,1) 
        self.ellipse(32,0,10,10,0,1) 
        self.ellipse(96,0,16,16,1,1)  
        self.ellipse(96,0,10,10,0,1)  

    def eyesWinkLeft(self):
        self.eyes()
        self.rect(64,0,128,16,0,True)

    def eyesWinkRight(self):
        self.eyes()
        self.rect(0,0,64,16,0,True)

    def eyesAngry(self):
        """Angry eyebrows / eye shape."""
        self.eyes()

        self.polygon([
            (16, 0),
            (48, 0),
            (48, 32)
        ], 0, True)

        self.polygon([
            (80, 0),
            (112, 0),
            (80, 32)
        ], 0, True)

    def eyesWorry(self):
        """Worried eye shape."""
        self.eyes()

        self.polygon([
            (16, 0),
            (48, 0),
            (16, 32)
        ], 0, True)

        self.polygon([
            (80, 0),
            (112, 0),
            (112, 32)
        ], 0, True)

    # =========================================================
    # MOUTHS
    # =========================================================

    def mouthClosed(self):
        self.rect(32,32,64,32,0,True)
        self.rect(32,42,64,6,1,True)

    def mouth(self):
        self.rect(32,32,64,32,0,True)
        self.ellipse(64,48,16,16,1,1) 
        self.ellipse(64,48,10,10,0,1)
        
    def mouthSmile(self):
        self.mouth()
        self.rect(48,32,33,16,0,True)
        
    def mouthUp(self):
        self.rect(32,32,64,32,0,True)
        self.ellipse(64,32,16,16,1,1) 
        self.ellipse(64,32,10,10,0,1)
        self.rect(48,16,33,16,0,True)
        
    def mouthSad(self):
        self.mouth()
        self.rect(48,48,33,16,0,True)

    def mouthDown(self):
        self.rect(32,32,64,32,0,True)
        self.ellipse(64,64,16,16,1,1) 
        self.ellipse(64,64,10,10,0,1)
        
    def mouthLeft(self):
        self.mouthClosed()
        self.ellipse(80,53,15,11,1,1)
        self.rect(64,48,32,5,1,True)
        
    def mouthRight(self):
        self.mouthClosed()
        self.ellipse(48,53,15,11,1,1)
        self.rect(32,48,32,5,1,True)
        
    def mouthHappy(self):
        self.rect(32,32,64,32,0,True)
        self.ellipse(64,48,15,15,1,1)
        self.rect(48,32,32,16,1,True)
        
    def mouthWorry(self):
        self.rect(32,32,64,32,0,True)
        self.ellipse(64,48,15,10,1,1)


    # =========================================================
    # COMPLETE FACES
    # =========================================================

    def face(self, expression):
        """
        Draw a complete named Otto face.

        Available:
            neutral
            happy
            surprised
            sleepy
            angry
            worried
            wink_left
            wink_right
        """

        self.clear()

        if expression == "neutral":
            self.eyes()
            self.mouth()

        elif expression == "happy":
            self.eyes()
            self.mouthSmile()

        elif expression == "surprised":
            self.eyes()
            self.mouth()

        elif expression == "sleepy":
            self.eyesClosed()
            self.mouth()

        elif expression == "angry":
            self.eyesAngry()
            self.mouth()

        elif expression == "worried":
            self.eyesWorry()
            self.mouth()

        elif expression == "wink_left":
            self.eyesWinkLeft()
            self.mouthSmile()

        elif expression == "wink_right":
            self.eyesWinkRight()
            self.mouthSmile()

        else:
            raise ValueError(
                "Unknown face: " + str(expression)
            )

    # =========================================================
    # ANIMATIONS
    # =========================================================

    def animate(self, animation, speed=0.1,
                repeat=1, show=True):
        """
        Play a named animation.

        Available:
            blink
            wink_left
            wink_right
            look_up
            look_down
            surprise
            happy
        """

        for _ in range(repeat):

            if animation == "blink":

                self.eyes()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyesClosed()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyes()
                if show:
                    self.show()

            elif animation == "wink_left":

                self.eyesWinkLeft()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyes()
                if show:
                    self.show()

            elif animation == "wink_right":

                self.eyesWinkRight()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyes()
                if show:
                    self.show()

            elif animation == "look_up":

                self.eyesDown()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyesUp()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyes()
                if show:
                    self.show()

            elif animation == "look_down":

                self.eyesUp()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyesDown()
                if show:
                    self.show()

                time.sleep(speed)

                self.eyes()
                if show:
                    self.show()

            elif animation == "surprise":

                self.face("neutral")
                if show:
                    self.show()

                time.sleep(speed)

                self.face("surprised")
                if show:
                    self.show()

                time.sleep(speed * 2)

                self.face("neutral")
                if show:
                    self.show()

            elif animation == "happy":

                self.face("happy")
                if show:
                    self.show()

                time.sleep(speed)

                self.face("neutral")
                if show:
                    self.show()

            else:
                raise ValueError(
                    "Unknown animation: " + str(animation)
                )

    # =========================================================
    # FRAME CONTROL
    # =========================================================

    def frame(self, draw_function, show=True):
        """
        Helper for creating a frame.

        Example:

            oled.frame(
                lambda: oled.face("happy")
            )
        """

        self.clear()
        draw_function()

        if show:
            self.show()





