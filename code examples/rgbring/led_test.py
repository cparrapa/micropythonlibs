from machine import Pin, PWM
from time import sleep

led = Pin(2, Pin.OUT)

for i in range(10):
    led.on()
    sleep(0.5)
    led.off()
    sleep(0.5)

pwm = PWM(Pin(2))
pwm.freq(1)
pwm.duty(896)
sleep(1)
pwm.duty(512)
sleep(1)
pwm.duty(0)