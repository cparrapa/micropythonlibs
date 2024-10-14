import machine
import time
from machine import Pin, PWM, ADC, I2C
from ottoneopixel import OttoUltrasonic
from rotary import Rotary
import math

#--------------------------------------------
# CONNECTOR SETUP
# Encoder 4pin -> Pin 2
# Encoder 3pin -> Pin 7
# Pontetiometer 3pin -> Pin 8
#--------------------------------------------

# Initialize peripherals
rotary = Rotary(16, 17, 33)  # Rotary encoder pins
potent = ADC(Pin(27))        # Potentiometer pin
ultrasonic = OttoUltrasonic(18, 19)  # Ultrasonic RGB pins

# Initialize brightness and power state
brightness = potent.read() / 10
power = True  # Control whether the RGBs are on or off
phase = 0     # Initial phase for color cycling

# Function to handle rotary changes
def rotary_changed(change):
    global phase, power
    if change == Rotary.ROT_CW:
        phase += 0.2
    elif change == Rotary.ROT_CCW:
        phase -= 0.2
    elif change == Rotary.SW_PRESS:
        power = not power  # Toggle power when the button is pressed
    elif change == Rotary.SW_RELEASE:
        print("haha")

# Add rotary change handler
rotary.add_handler(rotary_changed)

# Convert RGB values to Hex format
def rgb_to_hex(r, g, b):
    return '%02x%02x%02x' % (r, g, b)

# Function to generate RGB values based on the current phase
def rgbphase(phase):
    r = int((math.sin(phase % (2 * math.pi)) + 1) / 2 * 255) % 255
    g = int((math.sin((phase + (1 / 3) * 2 * math.pi) % (2 * math.pi)) + 1) / 2 * 255) % 255
    b = int((math.sin((phase + (2 / 3) * 2 * math.pi) % (2 * math.pi)) + 1) / 2 * 255) % 255
    return r, g, b

# Main loop
while True:
    # Read potentiometer value and adjust brightness
    pot_val = potent.read() / 4095
    
    # If power is off, set brightness to 0
    if not power:
        pot_val = 0
    
    # Select the RGB values based on the phase
    r, g, b = rgbphase(phase)
    
    # Apply brightness scaling to the RGB values
    rx = int(r * pot_val)
    gx = int(g * pot_val)
    bx = int(b * pot_val)
    
    # Convert RGB to hex format for output
    color = rgb_to_hex(rx, gx, bx)
    
    # If power is off, set color to black (all LEDs off)
    if not power:
        color = "000000"  # RGB = (0, 0, 0) in hex format
    
    # Set the RGB color on the ultrasonic module
    ultrasonic.ultrasonicRGB1(color, color)

    # Small delay to avoid overloading the CPU
    time.sleep(0.05)
