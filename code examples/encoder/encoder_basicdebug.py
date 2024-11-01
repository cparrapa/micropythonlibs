import time
from machine import Pin

rotaryA = Pin(16, Pin.IN, Pin.PULL_DOWN) # Connector 2 Pin.OUT
rotaryB = Pin(17, Pin.IN, Pin.PULL_DOWN) # Connector 2 Pin.OUT

while True:
    print("A",rotaryA.value(), end='')
    print("B",rotaryB.value())
    time.sleep(.1)