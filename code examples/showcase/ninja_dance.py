import machine                       #importing machine libraries
import time
from time import sleep               #importing sleep class
from machine import Pin, PWM         #importing Pin and PWM classes
from ottomotor import Servo
from ottowalkroll import Ninja
from ottoneopixel import OttoUltrasonic
from neopixel import NeoPixel

p = 6  # Number of LEDs in the ultrasonic RGB
bright = 0.9				# brightness variable for lights
led = Pin(2, Pin.OUT)                 # Built in LED
ultra = NeoPixel(Pin(18), p) # Connector 1
ultrasonic = OttoUltrasonic(18, 19)
ultrasonic.ultrasonicRGB2(0, 0, 255)
buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512) # Built in Buzzer

# angle servo motors
servo_leftleg=Servo()
servo_leftleg.attach(27)	# Connector 8
servo_rightleg=Servo()
servo_rightleg.attach(15)	# Connector 9

# wheel servo motors
servo_leftfoot=Servo()
servo_leftfoot.attach(14)	# Connector 10
servo_rightfoot=Servo()
servo_rightfoot.attach(13)	# Connector 11

delay = 0.05
ninja = Ninja(27, 15, 14, 13)         # Connector 8 (Left leg), 9(Right leg), 10(Left foot), 11(Right foot)

def wheelultra():
    global WheelPos, p, L, i
    WheelPos = (255) - WheelPos
    if WheelPos < (85):
        for L in range(p):
            ultra[L] = (255 - WheelPos * 3, 0, WheelPos * 3 )
        ultra.write()
    elif WheelPos < (170):
        WheelPos -= 85
        for L in range(p):
            ultra[L] = (0, WheelPos * 3, 255 - WheelPos * 3)
        ultra.write()
    else:
        WheelPos -= 170
        for L in range(p):
            ultra[L] = (WheelPos * 3, 255 - WheelPos * 3, 0)
        ultra.write()    

def red():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(255 * bright), int(0 * bright), int(0 * bright))
        ultra.write()
        sleep(delay)

def green():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(0 * bright), int(255 * bright), int(0 * bright))
        ultra.write()
        sleep(delay)

def blue():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(0 * bright), int(0 * bright), int(255 * bright))
        ultra.write()
        sleep(delay)
        
def orange():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(255 * bright), int(128 * bright), int(0 * bright))
        ultra.write()
        sleep(delay)

def yellow():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(255 * bright), int(255 * bright), int(0 * bright))
        ultra.write()
        sleep(delay)

def lime():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(128 * bright), int(255 * bright), int(0 * bright))
        ultra.write()
        sleep(delay)

def spring():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(0 * bright), int(255 * bright), int(128 * bright))
        ultra.write()
        sleep(delay)

def cyan():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(0 * bright), int(255 * bright), int(255 * bright))
        ultra.write()
        sleep(delay)

def azure():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(0 * bright), int(128 * bright), int(255 * bright))
        ultra.write()
        sleep(delay)

def purple():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(128 * bright), int(0 * bright), int(255 * bright))
        ultra.write()
        sleep(delay)

def magenta():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(255 * bright), int(0 * bright), int(255 * bright))
        ultra.write()
        sleep(delay)

def rose():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(255 * bright), int(0 * bright), int(128 * bright))
        ultra.write()
        sleep(delay)

def white():
    global i, p, delay
    for i in range(p):
        ultra[i] = (int(255 * bright), int(255 * bright), int(255 * bright))
        ultra.write()
        sleep(delay)

buzzer.duty(512)
buzzer.freq(262)
sleep(0.125)
buzzer.freq(294)
sleep(0.125)
buzzer.freq(330)
sleep(0.125)
buzzer.freq(349)
sleep(0.125)
buzzer.freq(392)
sleep(0.125)
buzzer.freq(440)
sleep(0.125)
buzzer.freq(494)
sleep(0.125)
buzzer.freq(523)
sleep(0.125)
buzzer.duty(0)

def set_color(r, g, b):
  for i in range(p):
    ultra[i] = (r, g, b)
  ultra.write()
set_color(255, 255, 0)
time.sleep_ms(200)

def wipe(r, g, b, wait):
    for i in range(p):
        ultra[i] = (r, g, b)
        ultra.write()
        time.sleep_ms(wait)
wipe(0, 255, 0, 50)

def cycle(r, g, b, wait):
    for i in range(1 * p):
        for j in range(p):
            ultra[j] = (0, 0, 0)
        ultra[i % p] = (r, g, b)
        ultra.write()
        time.sleep_ms(wait)
cycle(0, 255, 255, 100)    
  
def bounce(r, g, b, wait):
    for i in range(1 * p):
        for j in range(p):
            ultra[j] = (r, g, b)
        if (i // p) % 2 == 0:
            ultra[i % p] = (0, 0, 0)
        else:
            ultra[p - 1 - (i % p)] = (0, 0, 0)
        ultra.write()
        time.sleep_ms(wait)
bounce(0, 0, 255, 100)

def wheel(pos): # function to go through all colors 
  # Iringut a value 0 to 255 to get a color value.
  # The colours are a transition r - g - b - back to r.
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
    for i in range(p):
      rc_index = (i * 256 // p) + j
      ultra[i] = wheel(rc_index & 255)
    ultra.write()
    time.sleep_ms(wait)
rainbow_cycle(8)

def fadeinout():
    for i in range(0, 5 * 256, 8):
        for j in range(p):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            ultra[j] = (val, 0, 0)
        ultra.write()

def fade():
    for i in range(0, 4 * 256, 8):
        for j in range(p):
            if (i // 256) % 2 == 0:
                val = i & 0xff
            else:
                val = 255 - (i & 0xff)
            ultra[j] = (val, 0, 0)
        ultra.write()

red()
orange()
yellow()
green()
spring()
cyan()
azure()
blue()
purple()
magenta()
rose()
white()


while True:
    for i in range(255):
        WheelPos = i
        wheelultra()
        sleep(0.01)
    ninja.walkset()
    sleep(0.5)
    ninja.walk(1,3) #forward, fast
    ninja.walk(-1,3) #backward, fast
    sleep(0.5)
    ninja.walkset()
    ultrasonic.ultrasonicRGB2(255, 0, 0)
    ninja.rollset()
    sleep(0.5)
    ninja.roll(-1, 3)
    sleep(0.5)
    ninja.roll(1, 3)
    sleep(1)
    ninja.rollstop()
    sleep(0.4)
    ninja.rollrotate(1)  #right
    ninja.rollrotate(1)
    ninja.rollrotate(-1)  #left
    ninja.rollrotate(-1)
    sleep(0.4)
    ninja.rollset()
    sleep(0.4)
    ninja.roll(1, 1)
    ninja.roll(1, 2)
    ninja.roll(1, 3)
    sleep(0.6)
    ninja.rollstop()
    sleep(0.2)
    ultrasonic.ultrasonicRGB2(255, 0, 255)
    ninja.walkset()
    sleep(0.4)
    fadeinout()
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(0.3)
    servo_rightleg.write(100)
    servo_leftleg.write(100)
    sleep(0.3)
    servo_rightfoot.write(55)
    sleep(0.3)
    servo_rightfoot.write(90)
    sleep(0.3)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    sleep(0.5)
    servo_rightfoot.write(40)
    servo_leftfoot.write(40)
    sleep(2)
    servo_rightfoot.write(90)
    servo_leftfoot.write(90)
    sleep(0.4)
    servo_rightleg.write(65)
    servo_leftleg.write(75)
    sleep(0.3)
    servo_leftfoot.write(125)
    sleep(0.3)
    servo_leftfoot.write(90)
    sleep(0.3)
    servo_rightleg.write(90)
    servo_leftleg.write(90)
    fade()
    sleep(0.3)
    servo_rightleg.write(120)
    servo_leftleg.write(100)
    sleep(0.3)
    servo_rightleg.write(110)
    servo_leftleg.write(95) 
    sleep(0.3)
    servo_rightleg.write(90) 
    servo_leftleg.write(90) 
    sleep(0.3)
    servo_rightleg.write(140)
    servo_leftleg.write(110)
    sleep(0.3)
    servo_leftfoot.write(50)
    sleep(3)
    servo_leftfoot.write(90)
    servo_rightleg.write(90) 
    servo_leftleg.write(90) 
    sleep(0.3)
    servo_rightleg.write(65)
    servo_leftleg.write(40)
    sleep(0.3)
    servo_rightfoot.write(50)
    sleep(5)
    servo_rightfoot.write(90)
    servo_rightleg.write(90) 
    servo_leftleg.write(90) 
    sleep(0.3)
    servo_rightleg.write(100) 
    servo_leftleg.write(120) 
    sleep(0.3)
    servo_rightleg.write(90) 
    servo_leftleg.write(90) 
    sleep(1)
    