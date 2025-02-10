import time
import random
from machine import Pin, PWM
from neopixel import NeoPixel

# Game Configuration Colors
COLOR_BACKGROUND = (0, 0, 100)  # Blue color for moving pixel
COLOR_TARGET = (255, 0, 0)      # Red color for target pixel
COLOR_SUCCESS = (30, 150, 30)   # Green color for successful hit
COLOR_FAILURE = (50, 0, 0)      # Dark red for missed target
COLOR_LEVEL_INDICATOR = (10, 255, 50)  # Bright green for level indicator
COLOR_LEVEL_BLINK = (50, 255, 50)      # Slightly different green for blinking

button_pin = 27
pixel_pin = 22
no_pixels = 64
pixels = NeoPixel(Pin(pixel_pin), no_pixels)
button = Pin(button_pin, Pin.IN, Pin.PULL_UP)

# Variables
counter = 0
pause = 0
speed = 180
randomNumber = 0
level = 1

def random_int(a, b):
    if a > b:
        a, b = b, a
    return random.randint(a, b)

def winningSequence():
    # Rainbow color wave
    colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (143, 0, 255)   # Violet
    ]
    
    # Wave effect
    for repeat in range(3):  # Repeat the wave 3 times
        for color in colors:
            for i in range(no_pixels):
                pixels[i] = color
                pixels.write()
                time.sleep(0.05)
                pixels[i] = (0, 0, 0)
        
    # Final celebration - all pixels light up and fade
    for brightness in range(10):
        for i in range(no_pixels):
            pixels[i] = (
                int(255 * (brightness/10)), 
                int(255 * (brightness/10)), 
                int(255 * (brightness/10))
            )
        pixels.write()
        time.sleep(0.1)
    
    # Fade out
    for brightness in range(10, 0, -1):
        for i in range(no_pixels):
            pixels[i] = (
                int(255 * (brightness/10)), 
                int(255 * (brightness/10)), 
                int(255 * (brightness/10))
            )
        pixels.write()
        time.sleep(0.1)
    
    # Turn off
    pixels.fill((0, 0, 0))
    pixels.write()

def showLevel():
    global counter, level, speed
    pixels.fill((0, 0, 0))
    counter = 0
    
    # Winning sequence if level reaches 13
    if level == 13:
        winningSequence()
        # Reset game after winning
        level = 1
        speed = 180
        return

    for count in range(level - 1):
        if counter < no_pixels:
            pixels[counter] = COLOR_LEVEL_INDICATOR
            pixels.write()
            time.sleep(0.05)
            counter += 1
    if level > 16:
        level = 1
        speed = 180
    else:
        for count in range(5):
            if counter < no_pixels:
                pixels[counter] = COLOR_LEVEL_BLINK
                pixels.write()
                time.sleep(0.1)
                pixels[counter] = (0, 0, 0)
                pixels.write()
                time.sleep(0.1)
    pixels.fill((0, 0, 0))
    pixels.write()

def turnOnAll(R, G, B):
    for i in range(no_pixels):
        pixels[i] = (R, G, B)
    pixels.write()

def turnOff():
    pixels.fill((0, 0, 0))
    pixels.write()

def checkStatus():
    global counter, randomNumber, speed, level
    if button.value() == 1:
        while button.value() == 1:
            time.sleep_us(100)
        if counter == randomNumber:
            turnOnAll(*COLOR_SUCCESS)
            speed -= 10
            level += 1
            showLevel()
        else:
            turnOnAll(*COLOR_FAILURE)
        turnOff()
        randomNumber = random_int(0, no_pixels - 1)

def gameLoop(pause):
    global counter, randomNumber
    counter = 0
    for count in range(no_pixels):
        if counter < no_pixels:
            pixels[counter] = COLOR_BACKGROUND
            pixels.write()
            time.sleep_ms(speed)
            checkStatus()
            pixels[counter] = (0, 0, 0)
            pixels.write()
            counter += 1
            
            if 0 <= randomNumber < no_pixels:
                pixels[randomNumber] = COLOR_TARGET
                pixels.write()

def setup():
    global randomNumber
    pixels.fill((0, 0, 0))
    pixels.write()
    randomNumber = random_int(0, no_pixels - 1)
    showLevel()

def loop():
    gameLoop(speed)

setup()
while True:
    loop()