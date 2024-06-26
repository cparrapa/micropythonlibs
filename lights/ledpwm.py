from machine import Pin, PWM
from time import sleep

frequency = 5000
led = PWM(Pin(2), frequency)
buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512)
buzzer.duty(0)

while True:
  for duty_cycle in range(0, 1024):
    led.duty(duty_cycle)
    sleep(0.005)