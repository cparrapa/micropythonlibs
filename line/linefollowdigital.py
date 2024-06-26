from time import sleep
from machine import Pin
from neopixel import NeoPixel
from machine import PWM
import machine

brg = 0.75
pixels = NeoPixel(Pin(12), 13)
leftServo = PWM(Pin(2))
leftServo.freq(50)
rightServo = PWM(Pin(15))
rightServo.freq(50)
pin_led = machine.Pin(2, machine.Pin.OUT)
digital_pin_L = machine.Pin(13, machine.Pin.IN)
digital_pin_R = machine.Pin(0, machine.Pin.IN)

pin_led.off()
while True:
    if (digital_pin_L.value()) == (1):
        leftServo.duty(45)
        rightServo.duty(45)
    elif (digital_pin_R.value()) == (1):
        leftServo.duty(115)
        rightServo.duty(115)
    else:
        leftServo.duty(45)
        rightServo.duty(115)