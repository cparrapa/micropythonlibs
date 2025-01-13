from time import sleep
from machine import Pin, PWM
from neopixel import NeoPixel

bright = 0.5				# brightness variable for lights
n = 13 						# Number of LEDs in the ring
ring = NeoPixel(Pin(4), n)  #Connector 5
pin_led = Pin(2, Pin.OUT) 	# Built in LED
buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512) # Built in Buzzer

def red():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(255 * bright), int(0 * bright), int(0 * bright))
        ring.write()
        sleep(delay)

def green():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(0 * bright), int(255 * bright), int(0 * bright))
        ring.write()
        sleep(delay)

def blue():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(0 * bright), int(0 * bright), int(255 * bright))
        ring.write()
        sleep(delay)
        
def orange():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(255 * bright), int(128 * bright), int(0 * bright))
        ring.write()
        sleep(delay)

def yellow():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(255 * bright), int(255 * bright), int(0 * bright))
        ring.write()
        sleep(delay)

def lime():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(128 * bright), int(255 * bright), int(0 * bright))
        ring.write()
        sleep(delay)

def spring():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(0 * bright), int(255 * bright), int(128 * bright))
        ring.write()
        sleep(delay)

def cyan():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(0 * bright), int(255 * bright), int(255 * bright))
        ring.write()
        sleep(delay)

def azure():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(0 * bright), int(128 * bright), int(255 * bright))
        ring.write()
        sleep(delay)

def purple():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(128 * bright), int(0 * bright), int(255 * bright))
        ring.write()
        sleep(delay)

def magenta():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(255 * bright), int(0 * bright), int(255 * bright))
        ring.write()
        sleep(delay)

def rose():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(255 * bright), int(0 * bright), int(128 * bright))
        ring.write()
        sleep(delay)

def white():
    global i, n, delay
    for i in range(n):
        ring[i] = (int(255 * bright), int(255 * bright), int(255 * bright))
        ring.write()
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
buzzer.duty(0)
buzzer.duty(512)
buzzer.freq(392)
sleep(0.125)
buzzer.freq(440)
sleep(0.125)
buzzer.freq(494)
sleep(0.125)
buzzer.freq(523)
sleep(0.125)
buzzer.duty(0)
ring[0] = (int(255 * bright), int(255 * bright), int(255 * bright))
ring[1] = (int(255 * bright), int(128 * bright), int(0 * bright))
ring[2] = (int(255 * bright), int(255 * bright), int(0 * bright))
ring[3] = (int(128 * bright), int(255 * bright), int(0 * bright))
ring[4] = (int(0 * bright), int(255 * bright), int(0 * bright))
ring[5] = (int(0 * bright), int(255 * bright), int(128 * bright))
ring[6] = (int(0 * bright), int(255 * bright), int(255 * bright))
ring[7] = (int(0 * bright), int(128 * bright), int(255 * bright))
ring[8] = (int(0 * bright), int(0 * bright), int(255 * bright))
ring[9] = (int(127 * bright), int(0 * bright), int(255 * bright))
ring[10] = (int(255 * bright), int(0 * bright), int(255 * bright))
ring[11] = (int(255 * bright), int(0 * bright), int(127 * bright))
ring[12] = (int(255 * bright), int(0 * bright), int(0 * bright))
ring.write()
sleep(0.5)
pin_led.off()
sleep(1)
pin_led.on()
sleep(0.5)

delay = (1) / (20)
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