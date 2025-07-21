from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
import utime
import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

led = Pin(2, Pin.OUT)                 # Built in LED
bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
offset = 0
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

motor = OttoMotor(13, 14)             # Connectors 10 & 11

def search():
    global right_black, left_black
    while (distance()) > (15):
        ring.fillRGBRing("ff0101", "ff8000", "ffff00", "80ff00", "00ff00", "00ff80", "00ffff", "0080ff", "0000ff", "7f00ff", "ff00ff", "ff007f", "ffffff")
        ultrasonic.ultrasonicRGB2(0, 0, 255)
        motor.rightServo.duty(45+ offset)
        motor.leftServo.duty(45- offset)
        sleep(0.2)
        motor.rightServo.duty(0)
        motor.leftServo.duty(0)
    motor.Stop(1)

analogL=ADC(Pin(32))                  # Connector 6
analogR=ADC(Pin(33))                  # Connector 7

def takeout():
    global right_black, left_black
    while (analogL.read()) > left_black or (analogR.read()) > right_black:
        motor.leftServo.duty(109- offset)
        motor.rightServo.duty(43+ offset)
    ring.fillAllRing(255, 0, 0)
    ultrasonic.ultrasonicRGB2(255, 0, 0)
    motor.leftServo.freq(50)
    motor.rightServo.freq(50)
    motor.leftServo.duty(43- offset)
    motor.rightServo.duty(109+ offset)
    sleep(0.5)
    motor.rightServo.duty(0)
    motor.leftServo.duty(0)

ring.cycle(n, int(0 * bright), int(255 * bright), int(255 * bright), 150)
while True:
    right_black = 4094
    left_black = 4094
    search()
    takeout()