import time
import random
from machine import Pin, PWM
from neopixel import NeoPixel

button_pin = 26
pixel_pin = 4
no_pixels = 12
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

def showLevel():
    global counter, level, speed
    pixels.fill((0, 0, 0))
    counter = 0
    for count in range(level - 1):
        if counter < no_pixels:
            pixels[counter] = (10, 255, 50)
            pixels.write()
            time.sleep(0.05)
            counter += 1
    if level > 16:
        level = 1
        speed = 180
    else:
        for count in range(5):
            if counter < no_pixels:
                pixels[counter] = (50, 255, 50)
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
    if button.value() == 0:
        while button.value() == 0:
            time.sleep_us(100)
        if counter == randomNumber:
            turnOnAll(30, 150, 30)
            speed -= 10
            level += 1
            showLevel()
        else:
            turnOnAll(50, 0, 0)
        turnOff()
        randomNumber = random_int(0, no_pixels - 1)

def gameLoop(pause):
    global counter, randomNumber
    counter = 0
    for count in range(no_pixels):  # Changed to no_pixels instead of 11
        if counter < no_pixels:
            pixels[counter] = (0, 0, 100)
            pixels.write()
            time.sleep_ms(speed)
            checkStatus()
            pixels[counter] = (0, 0, 0)
            pixels.write()
            counter += 1
            
            # Always ensure randomNumber is within valid range before accessing
            if 0 <= randomNumber < no_pixels:
                pixels[randomNumber] = (255, 0, 0)
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