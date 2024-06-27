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
    print("Distance in cm: ", distance,)
    time.sleep(0.3)
    #ring.setRGBLed(0, 255, 0, round(map(int(distance), 0, 100, 0, 12)))
    #ring.clearRGB()
    if (distance) < (3):
        ultrasonic[0] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[1] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[2] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[3] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[4] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[5] = int(255 * bright), int(0 * bright), int(0 * bright)
        ultrasonic.write()
        ring.fillAllRing(255, 0, 0)
    elif (distance) < (7):
        ring.fillAllRing(255, 128, 0)
    elif (distance) < (10):
        ring.fillAllRing(255, 255, 0)
    elif (distance) < (14):
        ring.fillAllRing(128, 255, 0)
    else:
        ultrasonic[0] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[1] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[2] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[3] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[4] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[5] = int(51 * bright), int(255 * bright), int(0 * bright)
        ultrasonic.write()
        ring.fillAllRing(0, 255, 0)
