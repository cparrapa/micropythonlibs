# ottoneopixel v2.3 01.09.2024

# v2.1 07.08.2024 Alex Etchells: addition of colorHSV, set_pixel_line_gradient,  rotate_left, rotate_right
# v2.2 30.08.2024 Alex Etchells: Additon of 4x4 Matrix Functions
# setMatrixPixel, setMatrixRow, setMatrixCol, drawLine, drawTriangle, drawRectangle, drawRectangleFill, drawCircle
# v2.3 01.09.2024 Alex Etchells: Additon of 4x4 Matrix Functions
# Created OttoRGBMatrix subclass

import neopixel, machine, utime, time
from machine import Pin

class OttoNeoPixel:
    
    _brightness = 0.8
    
    def __init__(self, pin, ledcount):
        self._ledcount = ledcount
        self.pixels = neopixel.NeoPixel(Pin(pin), ledcount)
        self.pixValues = [(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0),(0, 0, 0)]
        
    def setBrightness(self, brightness):
        self._brightness = brightness

    def fillRGBRing(self, colour1, colour2, colour3, colour4, colour5, colour6, colour7, colour8, colour9, colour10, colour11, colour12, colour13):
        self.pixels[0] = self.HexColorToRGB(colour1)
        self.pixels[1] = self.HexColorToRGB(colour2)
        self.pixels[2] = self.HexColorToRGB(colour3) 
        self.pixels[3] = self.HexColorToRGB(colour4)
        self.pixels[4] = self.HexColorToRGB(colour5)
        self.pixels[5] = self.HexColorToRGB(colour6)
        self.pixels[6] = self.HexColorToRGB(colour7)
        self.pixels[7] = self.HexColorToRGB(colour8)
        self.pixels[8] = self.HexColorToRGB(colour9)
        self.pixels[9] = self.HexColorToRGB(colour10)
        self.pixels[10] = self.HexColorToRGB(colour11)
        self.pixels[11] = self.HexColorToRGB(colour12)
        self.pixels[12] = self.HexColorToRGB(colour13)
        self.pixels.write()
    
    def fillAllRGBRing(self, colourValue):
        for count in range(self._ledcount):
            self.pixels[count] = self.HexColorToRGB(colourValue)
        self.pixels.write()

    def fillAllRing(self, red, green, blue):
        for count in range(self._ledcount):
            self.pixels[count] = (int( red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels.write()

    def setRGBring(self, lednumber, colourValue):
        self.pixels[lednumber] = self.HexColorToRGB(colourValue)
        self.pixels.write()

    def setRGBLed(self, red, green, blue, lednumber):
        self.pixels[lednumber] = (int( red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels.write()

    def clearRGB(self):
        for count in range(self._ledcount):
            self.pixels[count] = (0, 0, 0)
        self.pixels.write()

    def HexColorToRGB(self, colourValue):
        hexRed = colourValue[0:2]
        hexGreen = colourValue[2:4]
        hexBlue = colourValue[4:6]
        
        red = int(hexRed, 16)
        green = int(hexGreen, 16)
        blue = int(hexBlue, 16)

        return (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))

    def bounce(self, n, r, g, b, wait):
        for i in range(2 * n):
            for j in range(n):
                self.pixels[j] = (r, g, b)
            if (i / n) % 2 == 0:
                self.pixels[i % n] = (0, 0, 0)
            else: 
                self.pixels[n - 1 - (i % n)] = (0, 0, 0)
            self.pixels.write()
            time.sleep_ms(wait)

    def cycle(self, n, r, g, b, wait): 
       for i in range(n): 
           for j in range(n): 
               self.pixels[j] = (0, 0, 0) 
           self.pixels[i % n] = (r, g, b) 
           self.pixels.write() 
           time.sleep_ms(wait)

    def wheel(self, pos):
       if pos < 0 or pos > 255:
          return (0, 0, 0)
       if pos < 85:
          return (255 - pos * 3, pos * 3, 0)
       if pos < 170:
           pos -= 85
           return (0, 255 - pos * 3, pos * 3)
       pos -= 170
       return (pos * 3, 0, 255 - pos * 3)
    
    def rainbow_cycle(self, n, wait):
       for j in range(255):
           for i in range(n):
               rc_index = (i * 256 // n) + j
               self.pixels[i] = self.wheel(rc_index & 255)
           self.pixels.write()
           time.sleep_ms(wait)

    def mazeCollect(self, colourValue):
        self.fillAllRGBRing(colourValue)
        time.sleep(2)
        self.clearRGB()

    def colorHSV(self, hue, sat, val):
        """
        Converts HSV color to rgb tuple and returns it.
        The logic is almost the same as in Adafruit NeoPixel library:
        https://github.com/adafruit/Adafruit_NeoPixel so all the credits for that
        go directly to them (license: https://github.com/adafruit/Adafruit_NeoPixel/blob/master/COPYING)

        :param hue: Hue component. Should be on interval 0..65535
        :param sat: Saturation component. Should be on interval 0..255
        :param val: Value component. Should be on interval 0..255
        :return: (r, g, b) tuple
        """
        if hue >= 65536:
            hue %= 65536

        hue = (hue * 1530 + 32768) // 65536
        if hue < 510:
            b = 0
            if hue < 255:
                r = 255
                g = hue
            else:
                r = 510 - hue
                g = 255
        elif hue < 1020:
            r = 0
            if hue < 765:
                g = 255
                b = hue - 510
            else:
                g = 1020 - hue
                b = 255
        elif hue < 1530:
            g = 0
            if hue < 1275:
                r = hue - 1020
                b = 255
            else:
                r = 255
                b = 1530 - hue
        else:
            r = 255
            g = 0
            b = 0

        v1 = 1 + val
        s1 = 1 + sat
        s2 = 255 - sat

        r = ((((r * s1) >> 8) + s2) * v1) >> 8
        g = ((((g * s1) >> 8) + s2) * v1) >> 8
        b = ((((b * s1) >> 8) + s2) * v1) >> 8

        return r, g, b


    def set_pixel_line_gradient(self, pixel1, pixel2, left_rgb, right_rgb):
        """
        Create a gradient with two RGB colors between "pixel1" and "pixel2" (inclusive)

        :param pixel1: Index of starting pixel (inclusive)
        :param pixel2: Index of ending pixel (inclusive)
        :param left_rgb: Tuple of form (r, g, b) representing starting color
        :param right_rgb: Tuple of form (r, g, b)  ending color        
        :return: None
        """
        if pixel2 - pixel1 == 0:
            return
        right_pixel = max(pixel1, pixel2)
        left_pixel = min(pixel1, pixel2)

        r_diff = right_rgb[0] - left_rgb[0]
        g_diff = right_rgb[1] - left_rgb[1]
        b_diff = right_rgb[2] - left_rgb[2]
        for i in range(right_pixel - left_pixel + 1):
            fraction = i / (right_pixel - left_pixel)
            red = round(r_diff * fraction + left_rgb[0])
            green = round(g_diff * fraction + left_rgb[1])
            blue = round(b_diff * fraction + left_rgb[2])
            self.setRGBLed(red, green, blue, left_pixel + i)

    def rotate_left(self, num_of_pixels=None):
        """
        Rotate <num_of_pixels> pixels to the left

        :param num_of_pixels: Number of pixels to be shifted to the left. If None, it shifts for 1.
        :return: None
        """
        n = self._ledcount
        if num_of_pixels is None:
            num_of_pixels = 1
        if num_of_pixels < 1:
            num_of_pixels = 1
        if num_of_pixels > n-1:
            num_of_pixels = n-1
        for i in range(n):
            self.pixValues[i] = self.pixels[i]
        for i in range(n):
            newIndex = i - num_of_pixels
            if newIndex < 0:
                newIndex += n
            self.pixels[newIndex] = self.pixValues[i]
        self.pixels.write()



    def rotate_right(self, num_of_pixels=None):
        """
        Rotate <num_of_pixels> pixels to the right

        :param num_of_pixels: Number of pixels to be shifted to the right. If None, it shifts for 1.
        :return: None
        """
        n = self._ledcount
        if num_of_pixels is None:
            num_of_pixels = 1
        if num_of_pixels < 1:
            num_of_pixels = 1
        if num_of_pixels > n-1:
            num_of_pixels = n-1
        for i in range(n):
            self.pixValues[i] = self.pixels[i]
        for i in range(n):
            newIndex = i + num_of_pixels
            if newIndex >= n:
                newIndex -= n
            self.pixels[newIndex] = self.pixValues[i]
        self.pixels.write()
        
    """  8x8 RGB matrix functions   """
class OttoRGBMatrix(OttoNeoPixel):
    
    def __init__(self, pin, ledcount):
        super().__init__(pin, ledcount)       
        
    def setMatrixPixel(self,x,y,r,g,b):
        if x>7 or x<0 or y>7 or y<0:
            return        
        r = int(r  * self._brightness)
        g = int(g  * self._brightness)
        b = int(b  * self._brightness)        
        pixelPos = x + (y*8)
        self.pixels[pixelPos] = (r,g,b)
        self.pixels.write()

    def setMatrixRow(self, row, rgb = [(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0)], drawNow = False):
        for i in range(8):
            r = int(rgb[i][0]  * self._brightness)
            g = int(rgb[i][1]  * self._brightness)
            b = int(rgb[i][2]  * self._brightness)         
            pixelPos = i + (row*8)
            self.pixels[pixelPos] = (r,g,b) 
        if drawNow:
            self.pixels.write()

    def setMatrixCol(self, col, rgb = [(0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0), (0,0,0)], drawNow = False):
        for i in range(8):
            r = int(rgb[i][0]  * self._brightness)
            g = int(rgb[i][1]  * self._brightness)
            b = int(rgb[i][2]  * self._brightness)         
            pixelPos = col + (i*8)
            self.pixels[pixelPos] = (r,g,b) 
        if drawNow:
            self.pixels.write()


    def drawLine(self, x0: int, y0: int, x1: int, y1: int, r: int,g: int,b: int):
        """
        draws a line from x0,y0 to x1,y1 of colour r,g,b
        """
        steep = abs(y1-y0) > abs(x1-x0)
        
        if steep:
            # Swap x/y
            tmp = x0
            x0 = y0
            y0 = tmp
            
            tmp = y1
            y1 = x1
            x1 = tmp
        
        if x0 > x1:
            # Swap start/end
            tmp = x0
            x0 = x1
            x1 = tmp
            tmp = y0
            y0 = y1
            y1 = tmp
        
        dx = x1 - x0;
        dy = int(abs(y1-y0))
        
        err = dx >> 1 # Divide by 2
        
        if(y0 < y1):
            ystep = 1
        else:
            ystep = -1
            
        while x0 <= x1:
            if steep:
                self.setMatrixPixel(y0, x0, r,g,b)
            else:
                self.setMatrixPixel(x0, y0, r,g,b)
            err -= dy
            if err < 0:
                y0 += ystep
                err += dx
            x0 += 1


    def drawTriangle(self, x0,y0, x1, y1, x2, y2, r,g,b):
        """
        Draws a triangle with corners at (x0,y0), (x1, y1), and (x2,y2). All lines are drawn with the specified r,g,b
        :param x0 The x coordinate of the first vertex
        :param y0 The y coordinate of the first vertex
        :param x1 The x coordinate of the second vertex
        :param y1 The y coordinate of the second vertex
        :param x2 The x coordinate of the third vertex
        :param y2 The y coordinate of the third vertex
        :params r,g,b  rgb values
        """
        self.drawLine(x0, y0, x1, y1, r,g,b)
        self.drawLine(x1, y1, x2, y2, r,g,b)
        self.drawLine(x2, y2, x0, y0, r,g,b)
     
    def drawRectangle(self, x0, y0, x1, y1, r,g,b):
        """
        Draws a rectangle with upper-left corner (x0,y0) and lower right corner (x1, y1). All edge lines are drawn with the specified r,g,b.
        Pixels inside the rectangle are left unmodified.

        :param x0 The x coordinate of the upper left corner
        :param y0 The y coordinate of the upper left corner
        :param x1 The x coordinate of the lower right corner
        :param y1 The y coordinate of the lower right corner
        :params r,g,b  rgb values
        """
        self.drawLine(x0, y0, x1, y0, r,g,b)
        self.drawLine(x1, y0, x1, y1, r,g,b)
        self.drawLine(x1, y1, x0, y1, r,g,b)
        self.drawLine(x0, y1, x0, y0, r,g,b)
        


    def drawRectangleFill(self, x0: int, y0: int, x1: int, y1: int, r,g,b):
        """
        Draws a rectangle with upper-left corner (x0,y0) and lower right corner (x1, y1). The rectangle is then filled to form a solid block of the specified r,g,b.
        
        :param x0 The x coordinate of the upper left corner
        :param y0 The y coordinate of the upper left corner
        :param x1 The x coordinate of the lower right corner
        :param y1 The y coordinate of the lower right corner
        :params r,g,b  rgb values
        """
        for x in range(x0, x1+1):
            for y in range(y0, y1+1):
                self.setMatrixPixel(x,y,r,g,b)


    def drawCircle(self, x0, y0, rad, r,g,b):
        """
        Draws a circle with center (self, x0,y0) and radius rad. The circle outline is drawn in the specified r,g,b. Pixels inside the circle are not modified.
         
        :param x0 The x coordinate of the circle center
        :param y0 The y coordinate of the circle center
        :params r,g,b  rgb values
        """
        f = 1-rad
        ddf_x = 1
        ddf_y = -2*rad
        x = 0
        y = rad
        self.setMatrixPixel(x0, y0 + rad, r,g,b)
        self.setMatrixPixel(x0, y0 - rad, r,g,b)
        self.setMatrixPixel(x0 + rad, y0, r,g,b)
        self.setMatrixPixel(x0 - rad, y0, r,g,b)
        
        while x < y:
            if f >= 0: 
                y -= 1
                ddf_y += 2
                f += ddf_y
            x += 1
            ddf_x += 2
            f += ddf_x
            self.setMatrixPixel(x0 + x, y0 + y, r,g,b)
            self.setMatrixPixel(x0 - x, y0 + y, r,g,b)
            self.setMatrixPixel(x0 + x, y0 - y, r,g,b)
            self.setMatrixPixel(x0 - x, y0 - y, r,g,b)
            self.setMatrixPixel(x0 + y, y0 + x, r,g,b)
            self.setMatrixPixel(x0 - y, y0 + x, r,g,b)
            self.setMatrixPixel(x0 + y, y0 - x, r,g,b)
            self.setMatrixPixel(x0 - y, y0 - x, r,g,b)

class OttoUltrasonic:
    
    _brightness = 1
    _io = 0
    distance = 0

    def __init__(self, rgb, io):
        self.pixels = neopixel.NeoPixel(Pin(rgb), 6)
        self._io = io
    
    def setBrightness(self, brightness):
        self._brightness = brightness
        
    def ultrasonicRGB1(self, colourLeft, colourRight):
        self.pixels[0] = self.HexColorToRGB(colourLeft)
        self.pixels[1] = self.HexColorToRGB(colourLeft)
        self.pixels[2] = self.HexColorToRGB(colourLeft)
        self.pixels[3] = self.HexColorToRGB(colourRight)
        self.pixels[4] = self.HexColorToRGB(colourRight)
        self.pixels[5] = self.HexColorToRGB(colourRight)
        self.pixels.write()
    
    def ultrasonicRGB2(self, red, green, blue):
        self.pixels[0] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels[1] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels[2] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels[3] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels[4] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels[5] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels.write()
    
    def setultrasonicRGBEye(self, red, green, blue, eyenumber):
        if(eyenumber == 0):
            self.pixels[0] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
            self.pixels[1] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
            self.pixels[2] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        else:
            self.pixels[3] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
            self.pixels[4] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
            self.pixels[5] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels.write()
                
    def setultrasonicRGBLed1(self, colour, lednumber):
        self.pixels[lednumber] = self.HexColorToRGB(colour)
        self.pixels.write()
        
    def setultrasonicRGBLed2(self, red, green, blue, lednumber):
        self.pixels[lednumber] = (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
        self.pixels.write()
        
    def clearultrasonicRGB(self):
        for count in range(6):
            self.pixels[count] = (0, 0, 0)
        self.pixels.write()

    def HexColorToRGB(self, colourValue):
        hexRed = colourValue[0:2]
        hexGreen = colourValue[2:4]
        hexBlue = colourValue[4:6]
        
        red = int(hexRed, 16)
        green = int(hexGreen, 16)
        blue = int(hexBlue, 16)

        return (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
            
    def readultrasonicRGBBasic(self, unit):
        io_pin = Pin(self._io, Pin.OUT)
        io_pin.off()
        utime.sleep_us(2)
        io_pin.on()
        utime.sleep_us(20)
        io_pin.off()
        io_pin = Pin(self._io, Pin.IN)
        pulse_duration = machine.time_pulse_us(io_pin, 1)
        
        if ((pulse_duration < 60000) and (pulse_duration > 1)):
            if (unit == 0):
                self.distance = pulse_duration / 147.32
            else:
                self.distance = pulse_duration / 58.00
        print("D#" + str(self.distance) + "$")
        return self.distance

    def readultrasonicRGB(self, unit):
        io_pin = Pin(self._io, Pin.OUT)
        io_pin.off()
        utime.sleep_us(2)
        io_pin.on()
        utime.sleep_us(20)
        io_pin.off()
        io_pin = Pin(self._io, Pin.IN)
        pulse_duration = machine.time_pulse_us(io_pin, 1)
        
        if ((pulse_duration < 60000) and (pulse_duration > 1)):
            if (unit == 0):
                self.distance = pulse_duration / 147.32
            else:
                self.distance = pulse_duration / 58.00
        return self.distance
