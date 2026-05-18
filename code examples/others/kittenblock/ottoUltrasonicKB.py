from ottoneopixel import OttoUltrasonic

__version__ = "1.0.0"

class OttoUltrasonicKB(OttoUltrasonic):
    def __init__(self,pin1=18,pin2=19):
        super().__init__(pin1,pin2)

    def ultrasonicRGB1(self, rgb1, rgb2):
        hex_color1 = rgb1[0] << 16 | rgb1[1] << 8 | rgb1[2]
        hex_color1 = hex(hex_color1)[2:]
        for _ in range(6-len(hex_color1)):
            hex_color1 = '0' + hex_color1
        
        hex_color2 = rgb2[0] << 16 | rgb2[1] << 8 | rgb2[2]
        hex_color2 = hex(hex_color2)[2:]
        for _ in range(6-len(hex_color2)):
            hex_color2 = '0' + hex_color2

        super().ultrasonicRGB1(hex_color1, hex_color2)
    
    def setultrasonicRGBLed1(self, rgb, index):
        hex_color = rgb[0] << 16 | rgb[1] << 8 | rgb[2]
        hex_color = hex(hex_color)[2:]
        for _ in range(6-len(hex_color)):
            hex_color = '0' + hex_color
        super().setultrasonicRGBLed1(hex_color, index)

    def setultrasonicRGBLed2(self, rgb, index):
        super().setultrasonicRGBLed2(rgb[0], rgb[1], rgb[2], index)