from machine import Pin
import time

# GPIO is the internal built-in LED
led = Pin(2, Pin.OUT)
# input on the lower left of the Pico using a built-in pull-down resistor to keep the value from floating
button = Pin(26, Pin.IN, Pin.PULL_DOWN)

while True:
    if button.value(): # if the value changes
        led.value(not led.value())  # Toggle the LED state
        time.sleep(0.1)  # Debounce delay
