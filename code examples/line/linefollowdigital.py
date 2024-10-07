from time import sleep
from machine import Pin, PWM

led = Pin(2, Pin.OUT)                 # Built in LED
digitalL = Pin(27, Pin.IN)            # Connector 8
digitalR = Pin(15, Pin.IN)            # Connector 9
leftServo = PWM(Pin(14))
leftServo.freq(50)
rightServo = PWM(Pin(13))
rightServo.freq(50)

while True:
    if (digitalL.value()) == (1):
        leftServo.duty(45)
        rightServo.duty(45)
        led.off()
    elif (digitalR.value()) == (1):
        leftServo.duty(115)
        rightServo.duty(115)
        led.off()
    else:
        leftServo.duty(45)
        rightServo.duty(115)
        led.on()