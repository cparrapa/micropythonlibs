# ottoneopixel v01 11.03.2024
import neopixel
import machine
import utime
from machine import Pin

class OttoNeoPixel:
    
    _brightness = 1
    
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

class OttoUltrasonic:
    
    _brightness = 1
    
    def __init__(self, rgb, io):
        self.pixels = neopixel.NeoPixel(Pin(rgb), 6)
        
    def ultrasonicRGB(self, colourLeft, colourRight):
        self.pixels[0] = self.HexColorToRGB(colourLeft)
        self.pixels[1] = self.HexColorToRGB(colourLeft)
        self.pixels[2] = self.HexColorToRGB(colourLeft)
        self.pixels[3] = self.HexColorToRGB(colourRight)
        self.pixels[4] = self.HexColorToRGB(colourRight)
        self.pixels[5] = self.HexColorToRGB(colourRight)
        self.pixels.write()
    
    def setultrasonicRGB(self, red, green, blue, lednumber):
        self.pixels[lednumber] = (int( red * self._brightness), int(green * self._brightness), int(blue * self._brightness))
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
        io=19
        io_pin = Pin(io, Pin.OUT)
        io_pin.off()
        utime.sleep_us(2)
        io_pin.on()
        utime.sleep_us(20)
        io_pin.off()
        io_pin = Pin(io, Pin.IN)
        pulse_duration = machine.time_pulse_us(io_pin, 1)
        distance = 0
        if ((pulse_duration < 60000) and (pulse_duration > 1)):
            if (unit == 0):
                distance = pulse_duration / 147.32
            else:
                distance = pulse_duration / 58.00
          
        return distance
