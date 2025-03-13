from time import sleep
from machine import Pin, PWM

led = Pin(2, Pin.OUT)                 # Built in LED
digitalL = Pin(27, Pin.IN)            # Connector 8
digitalR = Pin(15, Pin.IN)            # Connector 9

while True:
    if (digitalL.value()) == (1):
        leftServo.duty(60)
        rightServo.duty(60)
        led.off()
    elif (digitalR.value()) == (1):
        leftServo.duty(100)
        rightServo.duty(100)
        led.off()
    else:
        leftServo.duty(100)
        rightServo.duty(60)
        led.on()