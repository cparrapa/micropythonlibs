from time import sleep
from machine import Pin

led = Pin(2, Pin.OUT) # Built in LED

while True:
 led.on()
 sleep(1)
 led.off()
 sleep(1)
