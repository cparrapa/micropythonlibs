from machine import Pin
import time

led = Pin(25, Pin.OUT)  # Pico W: Pin("LED")

while True:
    led.toggle()
    time.sleep(0.5)
