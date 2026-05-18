from ottoneopixel import OttoNeoPixel

__version__ = "1.0.0"

class OttoNeoPixelKB(OttoNeoPixel):
    def __init__(self, n=13, bright=0.8):
        super().__init__(4, n)
        self.bright = bright
        self.n = n
    
    def rainbow_cycle(self, effect):
        super().rainbow_cycle(self.n, effect)

    def bounce(self, rgb, effect):
        super().bounce(self.n, int(rgb[0]*self.bright), int(rgb[1]*self.bright), int(rgb[2]*self.bright), effect)
    
    def cycle(self, rgb, effect):
        super().cycle(self.n, int(rgb[0]*self.bright), int(rgb[1]*self.bright), int(rgb[2]*self.bright), effect)
    
    def fillRGBRing(self,index1,index2,index3,index4,index5,index6,index7,index8,index9,index10,index11,index12,index13):
        colors = [index1,index2,index3,index4,index5,index6,index7,index8,index9,index10,index11,index12,index13]
        hex_colors = []
        for i in colors:
            rgb888 = i[0] << 16 | i[1] << 8 | i[2]
            rgb888 = hex(rgb888)[2:]
            for _ in range(6-len(rgb888)):
                rgb888 = '0' + rgb888
            hex_colors.append(rgb888)
        super().fillRGBRing(*hex_colors)
    
    def fillAllRGBRing(self, rgb):
        hex_color = rgb[0] << 16 | rgb[1] << 8 | rgb[2]
        hex_color = hex(hex_color)[2:]
        for _ in range(6-len(hex_color)):
            hex_color = '0' + hex_color
        super().fillAllRGBRing(hex_color)

    def setRGBring(self, index, rgb):
        hex_color = rgb[0] << 16 | rgb[1] << 8 | rgb[2]
        hex_color = hex(hex_color)[2:]
        for _ in range(6-len(hex_color)):
            hex_color = '0' + hex_color
        super().setRGBring(index, hex_color)

# o = OttoNeoPixelKB()
# o.fillRGBRing((0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0),(0,255,0))