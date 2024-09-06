import time
from time import sleep
from machine import Pin

print("Hello World")
led = Pin(2, Pin.OUT)  # Built in LED

while True:
    led.on()
    #led.value(1)
    time.sleep_ms(1000)
    #sleep(1)
    led.off()
    #led.value(0)
    time.sleep_ms(1000)
    #sleep(1)
