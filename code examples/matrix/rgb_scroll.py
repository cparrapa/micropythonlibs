# LED Matrix message scroller demo.
import bitmapfont
from machine import Pin
import utime
from neopixel import NeoPixel

ROWS = 8
COLS = 32
NUMBER_PIXELS = ROWS * COLS
matrix = NeoPixel(Pin(22), NUMBER_PIXELS) # Connector 3

def fill(val):
    for i in range(0, NUMBER_PIXELS):
        matrix[i] = val

# Configuration:
DISPLAY_WIDTH  = 8      # Display width in pixels.
DISPLAY_HEIGHT = 8       # Display height in pixels.
SPEED          = 20.0    # Scroll speed in pixels per second.

def show():
    matrix.write()

def write_pixel_value(x, y, value):
    if y >= 0 and y < ROWS and x >=0 and x < COLS:

            matrix[x*ROWS + y] = value

def write_pixel(x, y):
    write_pixel_value(x, y, (1,1,2))

def scroll_text(message):

    with bitmapfont.BitmapFont(DISPLAY_WIDTH, DISPLAY_HEIGHT, write_pixel) as bf:
        # Global state:
        pos = DISPLAY_WIDTH                 # X position of the message start.
        message_width = bf.width(message)   # Message width in pixels.
        last = utime.ticks_ms()             # Last frame millisecond tick time.
        speed_ms = SPEED / 1000.0           # Scroll speed in pixels/ms.
        # Main loop:
        while True:
            # Compute the time delta in milliseconds since the last frame.
            current = utime.ticks_ms()
            delta_ms = utime.ticks_diff(current, last)
            last = current
            # Compute position using speed and time delta.
            pos -= speed_ms*delta_ms
            if pos < -message_width:
                pos = DISPLAY_WIDTH
            # Clear the matrix and draw the text at the current position.
            fill((0,0,0))
            bf.text(message, int(pos), 0)
            # Update the matrix LEDs.
            show()
            # Sleep a bit to give USB mass storage some processing time (quirk
            # of SAMD21 firmware right now).
            utime.sleep_ms(20)

write_pixel(0,0)
show()
#scroll_text('Dan Loves Ann!')
scroll_text('MicroPython Rocks')
