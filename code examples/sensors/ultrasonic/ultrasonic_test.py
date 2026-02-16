import machine, time, utime
from time import sleep
from machine import Pin
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ultrasonic = NeoPixel(Pin(18), 6)     # Connector 1
io = 19                               # echo input and trigger out signal
bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
buzzer.playNote(261, 125)
buzzer.playNote(293, 125)
buzzer.playNote(329, 125)
buzzer.playNote(349, 125)
buzzer.playNote(392, 125)
buzzer.playNote(440, 125)
buzzer.playNote(493, 125)
buzzer.playNote(523, 125)

def measure_distance():
   io_pin = Pin(io, Pin.OUT)
   io_pin.off()
   utime.sleep_us(2)
   io_pin.on()
   utime.sleep_us(20)
   io_pin.off()
   io_pin = Pin(io, Pin.IN)
   pulse_duration = machine.time_pulse_us(io_pin, 1)
   distance = 0
   if ((pulse_duration < 60000) and (pulse_duration > 1)):
      distance = pulse_duration / 58.00; #45.6? or 58.00 for mm, 147.32 for in
   return distance

def map(value, in_min, in_max, out_min, out_max):
   map = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   return map

ultrasonic[0] = (0, 0, 255)
ultrasonic[1] = (0, 0, 255)
ultrasonic[2] = (0, 0, 255)
ultrasonic[3] = (255, 0, 0)
ultrasonic[4] = (255, 0, 0)
ultrasonic[5] = (255, 0, 0)
ultrasonic.write()
print(measure_distance())

while True:
    distance=measure_distance()
    print("Distance in cm: ", distance)
    time.sleep(0.1)
    #ring.setRGBLed(0, 255, 0, round(map(int(distance), 0, 100, 0, 12)))
    #ring.clearRGB()
    if (distance) < (3):
        buzzer.playNote(523, 40)
        ultrasonic[0] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[1] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[2] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[3] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[4] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[5] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic.write()
        ring.fillAllRing(255, 0, 0)
    elif (distance) < (6):
        buzzer.playNote(493, 40)
        ring.fillAllRing(255, 64, 0)
    elif (distance) < (9):
        buzzer.playNote(440, 40)
        ring.fillAllRing(255, 128, 0)
    elif (distance) < (12):
        buzzer.playNote(392, 40)
        ring.fillAllRing(255, 255, 0)
    elif (distance) < (15):
        buzzer.playNote(349, 40)
        ring.fillAllRing(128, 255, 0)
    elif (distance) < (18):
        buzzer.playNote(329, 40)
        ring.fillAllRing(64, 255, 0)
    elif (distance) < (21):
        buzzer.playNote(393, 40)
        ring.fillAllRing(30, 255, 0)
    else:
        buzzer.playNote(261, 40)
        ultrasonic[0] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[1] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[2] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[3] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[4] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[5] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic.write()
        ring.fillAllRing(0, 255, 0)