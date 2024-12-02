import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ultrasonic = NeoPixel(Pin(18), 6)     # Connector 1
io = 19                               # echo input and trigger out signal
bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
analogL=ADC(Pin(32))                  # Connector 6
analogR=ADC(Pin(33))                  # Connector 7
digitalL = Pin(27, Pin.IN)            # Connector 8
digitalR = Pin(15, Pin.IN)            # Connector 9
motor = OttoMotor(13, 14)             # Connectors 10 & 11
offsetL = 0                           # Calibration for left servo motor
offsetR = 0                           # Calibration for right servo motor

def wheel(pos):
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
       for i in range(n):
           rc_index = (i * 256 // n) + j
           ring.pixels[i] = wheel(rc_index & 255)
       ring.pixels.write()
       time.sleep_ms(wait)

while True:
        
    ultrasonic[0] = int(0 * bright), int(255 * bright), int(0 * bright)
    ultrasonic[1] = int(0 * bright), int(255 * bright), int(0 * bright)
    ultrasonic[2] = int(0 * bright), int(255 * bright), int(0 * bright)
    ultrasonic[3] = int(0 * bright), int(255 * bright), int(0 * bright)
    ultrasonic[4] = int(0 * bright), int(255 * bright), int(0 * bright)
    ultrasonic[5] = int(0 * bright), int(255 * bright), int(0 * bright)
    ultrasonic.write()
    buzzer.playEmoji("S_happy")
    rainbow_cycle(5)
    buzzer.playNote(262, 250)
    buzzer.playNote(349, 250)
    ring.fillAllRGBRing("00FF00")
    time.sleep((0.2))
    buzzer.playNote(349, 250)
    buzzer.playNote(392, 250)
    buzzer.playNote(349, 250)
    buzzer.playNote(329, 250)
    buzzer.playNote(293, 250)
    ring.fillAllRGBRing("fe0000")
    ultrasonic[0] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[1] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[2] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[3] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[4] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[5] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic.write()
    time.sleep((0.2))
    buzzer.playNote(294, 250)
    time.sleep((0.2))
    ring.fillAllRGBRing("00FF00")
    ultrasonic[0] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[1] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[2] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[3] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[4] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[5] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic.write()
    buzzer.playNote(294, 250)
    time.sleep((0.2))
    buzzer.playNote(392, 250)
    ultrasonic[0] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[1] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[2] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[3] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[4] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[5] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic.write()
    ring.fillAllRGBRing("fe0000")
    time.sleep((0.2))
    buzzer.playNote(392, 250)
    buzzer.playNote(440, 250)
    buzzer.playNote(392, 250)
    buzzer.playNote(349, 250)
    time.sleep((0.2))
    buzzer.playNote(330, 250)
    ultrasonic[0] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[1] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[2] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[3] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[4] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[5] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic.write()
    ring.fillAllRGBRing("00FF00")
    buzzer.playNote(262, 250)
    time.sleep((0.2))
    buzzer.playNote(440, 250)
    ring.fillAllRGBRing("fe0000")
    ultrasonic[0] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[1] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[2] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[3] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[4] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[5] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic.write()
    time.sleep((0.2))
    buzzer.playNote(440, 250)
    time.sleep((0.2))
    ring.fillAllRGBRing("00FF00")
    ultrasonic[0] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[1] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[2] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[3] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[4] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[5] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic.write()
    buzzer.playNote(494, 250)
    time.sleep((0.2))
    buzzer.playNote(440, 250)
    buzzer.playNote(392, 250)
    buzzer.playNote(349, 250)
    buzzer.playNote(293, 250)
    buzzer.playNote(261, 250)
    buzzer.playNote(261, 250)
    buzzer.playNote(293, 250)
    buzzer.playNote(392, 250)
    ultrasonic[0] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[1] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[2] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[3] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[4] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[5] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic.write()
    ring.fillAllRGBRing("fe0000")
    time.sleep((0.2))
    buzzer.playNote(330, 250)
    buzzer.playNote(349, 250)

    buzzer.execute_RTTTL('SilentNight')
    ring.fillAllRGBRing("00FF00")
    ultrasonic[0] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[1] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[2] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[3] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[4] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[5] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic.write()
    buzzer.execute_RTTTL('JingleBell')
    ring.fillAllRGBRing("fe0000")
    ultrasonic[0] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[1] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[2] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[3] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[4] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[5] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic.write()
    buzzer.execute_RTTTL('WeWishYou')
    ultrasonic[0] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[1] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[2] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[3] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[4] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[5] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic.write()
    buzzer.execute_RTTTL('Toccata')

