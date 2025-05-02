import time
import random
from machine import Pin
from neopixel import NeoPixel

# Button pin setup
button = Pin(26, Pin.IN, Pin.PULL_UP)

# Neopixel setup
pixel_pin = Pin(22, Pin.OUT)
num_pixels = 64

pixels = NeoPixel(pixel_pin, num_pixels)

def colorwheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // 10) + j
            pixels[i] = colorwheel(rc_index & 255)
        pixels.write()
        time.sleep(wait)

def color_chase(c, wait):
    for i in range(num_pixels):
        pixels[i] = c
        time.sleep(wait)
        pixels.write()
    time.sleep(1)

def game_over():
    color_chase((0, 0, 0), 0.05)
    pixels.fill((255, 0, 0))
    pixels.write()
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    pixels.write()
    time.sleep(0.5)
    pixels.fill((255, 0, 0))
    pixels.write()
    time.sleep(0.5)
    pixels.fill((0, 0, 0))
    pixels.write()
    time.sleep(0.5)
    pixels.fill((255, 0, 0))
    pixels.write()
    time.sleep(1)

pixel = 0
num = 0
last_num = 0
now_color = 0
next_color = 1
speed = 1  # Increase this value to slow down the LED movement
level = 0.005
final_level = 0.001
new_target = True
button_state = False

colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 128, 128), (0, 255, 255),
          (0, 0, 255), (128, 0, 128), (255, 0, 255), (255, 215, 0), (0, 255, 255), (255, 192, 203)]

while True:
    if not button.value() and not button_state:
        button_state = True

    if new_target:
        y = int(random.randint(5, 55))
        x = int(y - 1)
        z = int(y + 1)
        new_target = False
        print(x, y, z)
    pixels[x] = (255, 255, 255)
    pixels[y] = colors[next_color]
    pixels[z] = (255, 255, 255)

    if (pixel + speed) < time.ticks_us():
        if num > 0:
            last_num = num - 1
            pixels[last_num] = (0, 0, 0)
            pixels.write()
        if last_num in (x, y, z):
            pixels[x] = (255, 255, 255)
            pixels[y] = colors[next_color]
            pixels[z] = (255, 255, 255)
        if num < num_pixels:
            pixels[num] = colors[now_color]
            pixels.write()
            num += 1
        if num == num_pixels:
            last_num = num - 1
            pixels[last_num] = (0, 0, 0)
            pixels.write()
            num = 0
        if last_num in [x, y, z] and not button.value():
            button_state = False
            pixels.fill(colors[next_color])
            pixels.write()
            print(num)
            print(x, y, z)
            num = 0
            time.sleep(1)
            pixels.fill((0, 0, 0))
            pixels.write()
            speed -= level
            next_color += 1
            if next_color > 11:
                next_color = 0
            now_color += 1
            if now_color > 11:
                now_color = 0
            new_target = True
            print("speed is", speed)
            print("button is", button.value())
        if last_num not in [x, y, z] and not button.value():
            button_state = False
            print(num)
            print(x, y, z)
            pixels.fill(colors[now_color])
            pixels.write()
            game_over()
            num = 0
            pixels.fill((0, 0, 0))
            pixels.write()
            speed = 1  # Reset speed to the slower value
            next_color = 1
            now_color = 0
            new_target = True
            print("speed is", speed)
            print("button is", button.value())
        if speed < final_level:
            rainbow_cycle(1)
            time.sleep(1)
            num = 0
            pixels.fill((0, 0, 0))
            pixels.write()
            speed = 1  # Reset speed to the slower value
            next_color = 1
            now_color = 0
            new_target = True
        pixel = time.ticks_ms()
