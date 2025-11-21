import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
import rtttl

jingle ='JingleBell:d=8,o=5,b=112:a,a,4a,a,a,4a,a,c6,f.,16g,2a,a#,a#,a#.,16a#,a#,a,a.,16a,a,g,g,a,4g,4c6,16p,a,a,4a,a,a,4a,a,c6,f.,16g,2a,a#,a#,a#.,16a#,a#,a,a.,16a,c6,c6,a#,g,2f'
silent= 'SilentNight:d=4,o=5,b=112:g.,8a,g,2e.,g.,8a,g,2e.,2d6,d6,2b.,2c6,c6,2g.,2a,a,c6.,8b,a,g.,8a,g,2e.,2a,a,c6.,8b,a,g.,8a,g,2e.,2d6,d6,f6.,8d6,b,2c6.,2e6.,c6,g,e,g.,8f,d,2c.'
wish = 'WeWishYou:d=4,o=5,b=200:d,g,8g,8a,8g,8f#,e,e,e,a,8a,8b,8a,8g,f#,d,d,b,8b,8c6,8b,8a,g,e,d,e,a,f#,2g,d,g,8g,8a,8g,8f#,e,e,e,a,8a,8b,8a,8g,f#,d,d,b,8b,8c6,8b,8a,g,e,d,e,a,f#,1g,d,g,g,g,2f#,f#,g,f#,e,2d,a,b,8a,8a,8g,8g,d6,d,d,e,a,f#,2g'
toccata= 'Toccata:d=4,o=5,b=160:16a4,16g4,1a4,16g4,16f4,16d4,16e4,2c#4,16p,d.4,2p,16a4,16g4,1a4,8e.4,8f.4,8c#.4,2d4'

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
    #buzzer.execute_RTTTL('SilentNight')
    rtttl.play(silent)
    ring.fillAllRGBRing("00FF00")
    ultrasonic[0] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[1] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[2] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[3] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[4] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic[5] = (int(0 * bright), int(255 * bright), int(0 * bright))
    ultrasonic.write()
    #buzzer.execute_RTTTL('JingleBell')
    rtttl.play(jingle)
    ring.fillAllRGBRing("fe0000")
    ultrasonic[0] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[1] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[2] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[3] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[4] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic[5] = (int(255 * bright), int(0 * bright), int(0 * bright))
    ultrasonic.write()
    #buzzer.execute_RTTTL('WeWishYou')
    rtttl.play(wish)
    ultrasonic[0] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[1] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[2] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[3] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[4] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic[5] = (int(0 * bright), int(0 * bright), int(255 * bright))
    ultrasonic.write()
    #buzzer.execute_RTTTL('Toccata')
    rtttl.play(toccata)
    