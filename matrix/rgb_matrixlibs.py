from time import sleep
from machine import Pin
from neopixel import NeoPixel

class LedDisplay:
    def __init__(self, pin=16, num_pixels=128, brg=0.1):
        self.brg = brg
        self.pixels = NeoPixel(Pin(pin), num_pixels)
        self.default_color = (int(102 * self.brg), int(0 * self.brg), int(204 * self.brg))
        
        self.bits_happy = "00000000000000000011110000111100010000100100001001000010010000100100001001000010010000100100001001000010010000100000000000000000"
        self.bits_sad = "10000100001000011000010000100001100001000010000110000100001000010111100000011110000000000000000000000000000000000000000000000000"
        self.bits_angry = "11100000000001111111100000011111011111000011111001111100001111100011100000011100000000000000000000000000000000000000000000000000"
        self.bits_love = "01001000000100101111110000111111111111000011111101111000000111100011000000001100000000000000000000000000000000000000000000000000"
        self.bits_sleep = "11111000000111110001000000000010001000000000010001000000000010001111100000011111000000000000000000000000000000000000000000000000"
        self.bits_confused = "01111100001111101000001001000001100100100100100110101010010101011010101001010101101100100101100110011100010011100000000000000000"
        self.bits_dizzy = "01111100001111101000001001000001100100100100100110101010010101011010101001010101101100100101100110011100010011100000000000000000"
        self.bits_wave = "00000000000000000000000000000000000000000000000000100010000100010101010000101010100010000100010000000000000000000000000000000000"
        self.bits_fail = "11011111111110111100111010100001101111111100010111000011001101101111001100110011111000100011000110001111111110111111111111110101"
        self.bits_xx = "10000001100000010100001001000010001001000010010000011000000110000001100000011000001001000010010001000010010000101000000110000001"
        self.bits_eyes = [self.bits_happy, self.bits_sad, self.bits_angry, self.bits_love, self.bits_sleep, self.bits_confused, self.bits_dizzy, self.bits_wave, self.bits_fail, self.bits_xx]
        
        self.top_right = "00000000000000000011110000111100010011100100111001110010011100100111111001111110011111100111111000111100001111000000000000000000"
        self.top_center = "00000000000000000011110000111100011001100110011001100110011001100111111001111110011111100111111000111100001111000000000000000000"
        self.top_left = "00000000000000000011110000111100011100100111001001001110010011100111111001111110011111100111111000111100001111000000000000000000"
        self.left = "00000000000000000011110000111100011111100111111001001110010011100111001001110010011111100111111000111100001111000000000000000000"
        self.bottom_left = "00000000000000000011110000111100011111100111111001111110011111100111001001110010010011100100111000111100001111000000000000000000"
        self.bottom_center = "00000000000000000011110000111100011111100111111001111110011111100110011001100110011001100110011000111100001111000000000000000000"
        self.bottom_right = "00000000000000000011110000111100011111100111111001111110011111100100111001001110011100100111001000111100001111000000000000000000"
        self.right = "00000000000000000011110000111100011111100111111001110010011100100100111001001110011111100111111000111100001111000000000000000000"
        self.center = "00000000000000000011110000111100011111100111111001100110011001100110011001100110011111100111111000111100001111000000000000000000"
        self.squinting = "00000000000000000011110000111100011111100111111001111110011111100111001001001110011100100100111000111100001111000000000000000000"
        
    def setColor(self, r, g, b):
        self.default_color = (int(r * self.brg), int(g * self.brg), int(b * self.brg))
    
    def setPixel(self, pixel, state=1):
        if state in ["on", 1]:
            self.pixels[pixel] = self.default_color
        elif state in ["off", 0]:
            # Assuming self.default_color represents the "off" state, modify it accordingly
            self.pixels[pixel] = 0  # Change default_off_color to the appropriate value
        else:
            raise ValueError("Invalid state parameter. Use 'on' or 1 for ON state, 'off' or 0 for OFF state.")
        
        self.pixels.write()
        sleep(0.01)
    
    def setRow(self, row, state):
        if row < 1 or row > 8:
            print("Invalid row number. Row should be between 1 and 8.")
            return
        row -= 1
        start_index = row * 16
        end_index = start_index + 16
        value = 1 if state.lower() == 'on' else 0
        for i in range(start_index, end_index):
            if value == 1:
                self.pixels[i] = self.default_color
        self.pixels.write()
            
    def eyes(self, bits):
        bits = self.bits_eyes[bits]
        for i, bit in enumerate(bits):
            if bit == '1':
                self.pixels[i] = self.default_color
        self.pixels.write()
        sleep(0.01)
        
    def lookAt(self, direction):
        if direction == "top-right":
            self.draw(self.top_right)
        elif direction == "top-center":
            self.draw(self.top_center)
        elif direction == "top-left":
            self.draw(self.top_left)
        elif direction == "left":
            self.draw(self.left)
        elif direction == "bottom-center":
            self.draw(self.bottom_center)
        elif direction == "bottom-left":
            self.draw(self.bottom_left)
        elif direction == "bottom-right":
            self.draw(self.bottom_right)
        elif direction == "right":
            self.draw(self.right)
        elif direction == "center":
            self.draw(self.center)
        elif direction == "squinting":
            self.draw(self.squinting)
        else:
            print("Invalid direction!")
            return
    
    def draw(self, bits):
        for i, bit in enumerate(bits):
            if bit == '1':
                self.pixels[i] = self.default_color
        self.pixels.write()
        sleep(0.01)

    def clearDisplay(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.write()
        sleep(0.01)
        
# -------------------------------------------------------------------------------
# LedDisplay Class
# -------------------------------------------------------------------------------
#
# This class provides a simple interface for controlling a NeoPixel LED display.
#
# Class Methods:
#   - __init__(self, pin=16, num_pixels=128, brg=0.1): Initializes the LedDisplay instance.
#     - pin: GPIO pin connected to the NeoPixel strip.
#     - num_pixels: Number of pixels in the NeoPixel strip.
#     - brg: Brightness factor for adjusting the default color.
#
#   Because we are testing with a RGB LED display of 128 pixels with the HP Otto board,
#   I opted to use default values of 16, 128 and 0.1 for this method init.
#
#   - setColor(self, r, g, b): Sets the default color for the LED display.
#     - r, g, b: Red, green, and blue components of the color (0-255).
#
#   - setPixel(self, pixel, state=1): Sets the state of an individual pixel.
#     - pixel: Index of the pixel to be modified.
#     - state: State of the pixel; can be 'on', 1 for ON state, 'off', or 0 for OFF state.
#
#   If a state is not specified, the function will simply turn on the specified pixel.
#
#   - setRow(self, row, state): Sets the state of an entire row of pixels.
#     - row: Row number (1-8) to be modified.
#     - state: State of the row; can be 'on' or 'off'.
#
#   - eyes(self, bits): Displays predefined eye patterns on the LED display.
#     - bits: Index of the eye pattern (0-10).
#
#   - lookAt(self, direction): Displays predefined eye patterns in specific direction on the LED display.
#     - direction: String with the desired direction. If direction include two words, must be separated with -
#
#   - draw(self, bits): Draws a custom pattern on the LED display based on the provided bit string.
#     - bits: Bit string representing the pattern to be drawn.
#
#   - clearDisplay(self): Clears the LED display by turning off all pixels.
#
# Example Usage:
led_display = LedDisplay()
led_display.setColor(102, 0, 204)
led_display.setPixel(5, 'on')
led_display.setRow(1, 'on')
led_display.eyes(0)
led_display.lookAt("squinting")
led_display.draw('0101010101010101')
#led_display.clearDisplay()
# -------------------------------------------------------------------------------