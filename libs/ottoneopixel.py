# ottoneopixel v2.0 12.07.2024
import neopixel, machine, utime, time
from machine import Pin

class OttoNeoPixel:
    
    _brightness = 0.8
    
    def __init__(self, pin, ledcount):
        self._ledcount = ledcount
        self.pixels = neopixel.NeoPixel(Pin(pin), ledcount)
        
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
        print("D#" + str(self.distance) + "$")
        return self.distance

