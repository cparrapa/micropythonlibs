import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottoneopixel import OttoUltrasonic
import utime
from ottomotor import OttoMotor
offset = 0

ultrasonic = OttoUltrasonic(18, 19)
ultrasonic.ultrasonicRGB2(255, 255, 0)
io = 19     # echo input and trigger out signal

bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5

motor = OttoMotor(13, 14)             # Connectors 10 & 11

def distance():
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
      distance = pulse_duration / 58.00;

   return distance


ring.rainbow_cycle(n, 3)
ring.fillAllRing(255, 255, 0)
sleep(1)
ring.fillRGBRing("ffffff", "ff8000", "ffff00", "80ff00", "00ff00", "00ff80", "00ffff", "0080ff", "0000ff", "7f00ff", "ff00ff", "ff007f", "ff0101")
sleep(1)
ring.bounce(n, int(254 * bright), int(0 * bright), int(0 * bright), 50)
ultrasonic.ultrasonicRGB2(0, 0, 255)
ring.cycle(n, int(254 * bright), int(0 * bright), int(0 * bright), 50)
ring.fillRGBRing("ffffff", "fe0000", "fe0000", "ffffff", "ffffff", "ffffff", "ffffff", "ffffff", "ffffff", "ffffff", "fe0000", "fe0000", "fe0000")
ultrasonic.ultrasonicRGB2(0, 255, 255)
sleep(2)

while True:
    if (distance()) < (10):
        ultrasonic.ultrasonicRGB1("fe0000", "fe0000")
        ring.fillRGBRing("ffffff", "ffffff", "ffffff", "fe0000", "fe0000", "fe0000", "fe0000", "fe0000", "fe0000", "fe0000", "ffffff", "ffffff", "ffffff")
        motor.leftServo.freq(50)
        motor.rightServo.freq(50)
        motor.leftServo.duty(43- offset)
        motor.rightServo.duty(109+ offset)
        sleep(1)
        motor.rightServo.duty(0)
        motor.leftServo.duty(0)
        motor.rightServo.duty(45+ offset)
        motor.leftServo.duty(45- offset)
        sleep(0.8)
        motor.rightServo.duty(0)
        motor.leftServo.duty(0)
    else:
        ultrasonic.ultrasonicRGB1("ffff00", "ffff00")
        ring.fillAllRGBRing("ffff00")
        motor.leftServo.duty(109- offset)
        motor.rightServo.duty(43+ offset)
