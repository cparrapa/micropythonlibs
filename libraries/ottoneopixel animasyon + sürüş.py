
# ottoneopixel v2.0 12.07.2024
import neopixel, machine, utime, time
from machine import Pin,Timer

class OttoNeoPixel:
    
    _brightness = 0.8
    
    def __init__(self, pin, ledcount):
        self.pixels = neopixel.NeoPixel(Pin(pin), ledcount)
        self._ledcount = ledcount
        self._timer = None
        self._step = 0
        self._active = False
        self._bounce_params = {
            'active': False,
            'step': 0,
            'n': 0,
            'color': (0,0,0),
            'interval': 50,
            'brightness': 1.0
        }
        self._cycle_params = {
            'active': False,
            'pos': 0,
            'n': 0,
            'color': (0,0,0),
            'interval': 50
        }
        
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
        self._active = False 
        if self._timer:
            self._timer.deinit()
            self._timer = None
        for i in range(self._ledcount):
            self.pixels[i] = (0, 0, 0)
        self.pixels.write()

    def HexColorToRGB(self, colourValue):
        hexRed = colourValue[0:2]
        hexGreen = colourValue[2:4]
        hexBlue = colourValue[4:6]
        
        red = int(hexRed, 16)
        green = int(hexGreen, 16)
        blue = int(hexBlue, 16)

        return (int(red * self._brightness), int(green * self._brightness), int(blue * self._brightness))

    def bounce(self, n, r, g, b, wait, brightness=1.0):
  
        if self._timer:
            self._timer.deinit()
            
        self._bounce_params = {
            'active': True,
            'pos': n-1,  #
            'n': min(n, self._ledcount),
            'color': (
                int(r * brightness),
                int(g * brightness),
                int(b * brightness)
            ),
            'interval': wait,
            'brightness': brightness
        }
        
 
        for i in range(self._bounce_params['n']):
            self.pixels[i] = self._bounce_params['color']
        self.pixels.write()
        

        try:
            self._timer = Timer(0) 
        except:
            self._timer = Timer()   
            
        self._timer.init(
            period=self._bounce_params['interval'],
            mode=Timer.PERIODIC,
            callback=self._bounce_update
        )

    def _bounce_update(self, timer):
        if not self._bounce_params['active']:
            return
            
        params = self._bounce_params
        n = params['n']
        
     
        self.pixels[params['pos']] = params['color']
        
    
        params['pos'] = (params['pos'] - 1) % n
        
     
        self.pixels[params['pos']] = (0, 0, 0)
        self.pixels.write()
        
    def cycle(self, n, r, g, b, interval):
        if self._timer:
            self._timer.deinit()
            
        self._cycle_params = {
            'active': True,
            'pos': n-1,  
            'n': min(n, self._ledcount),
            'color': (r, g, b),
            'interval': interval
        }
        
       
        try:
            self._timer = Timer(0) 
        except:
            self._timer = Timer()   
            
        self._timer.init(
            period=self._cycle_params['interval'],
            mode=Timer.PERIODIC,
            callback=self._update_cycle
        )

    def _update_cycle(self, timer):
        if not self._cycle_params['active']:
            return
            
        params = self._cycle_params
        n = params['n']
        
        for j in range(n):
            self.pixels[j] = (0, 0, 0)
        
        self.pixels[params['pos']] = params['color']
        self.pixels.write()
        
        params['pos'] = (params['pos'] - 1) % n

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
    
    def _update_rainbow(self, timer):
        if not self._active:
            return
        for i in range(self._ledcount):
            rc_index = (i * 256 // self._ledcount) + self._step
            self.pixels[i] = self.wheel(rc_index & 255)
        self.pixels.write()
        self._step = (self._step + 1) % 256

    def rainbow_cycle(self, n, interval):
        self._ledcount = n
        self._active = True  
        if self._timer:
            self._timer.deinit()
        self._timer = Timer(0)
        self._timer.init(period=interval, mode=Timer.PERIODIC, callback=self._update_rainbow)

    def stop_rainbow(self):
        self._active = False
        if self._timer:
            self._timer.deinit()
        self.pixels.fill((0, 0, 0))
        self.pixels.write()

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

        return (int(green * self._brightness), int(red * self._brightness), int(blue * self._brightness))
            
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
