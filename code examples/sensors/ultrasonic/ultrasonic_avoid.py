import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottoneopixel import OttoUltrasonic
import utime
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottomotor import OttoMotor
offset = 0

led = Pin(2, Pin.OUT)                 # Built in LED
ultrasonic = OttoUltrasonic(18, 19)
io = 19     # echo input and trigger out signal

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

bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
motor = OttoMotor(13, 14)             # Connectors 10 & 11

while True:
    if (distance()) < (10):
        ultrasonic.ultrasonicRGB1("fe0000", "fe0000")
        ring.fillAllRGBRing("fe0000")
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
        ultrasonic.ultrasonicRGB1("33ff33", "33ff33")
        ring.fillAllRGBRing("33ff33")
        motor.leftServo.duty(109- offset)
        motor.rightServo.duty(43+ offset)
