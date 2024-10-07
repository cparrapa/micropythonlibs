from machine import Pin, ADC  #importing Pin and ADC classes
from utime import sleep       #importing sleep class

led = Pin(2, Pin.OUT)    # Built in LED
pot=ADC(Pin(32))         # creating potentiometer object Connector 7

MAX_DELAY = .5 # seconds

# global variables
delay = 0

# repeat forever
while True:
    #pot_value=pot.read()  reading analog pin
    #delay= 0.1 + potentiometer_value/4095
    pot_value = pot.read_u16() # read the value from the pot
    delay = pot_value/65025 * MAX_DELAY
    print(pot_value)
    print("delay:", delay)
    if delay > 0:
        print("frequency (toggles per second):", 1/delay)
    led.on()  # turn on the LED 
    sleep(delay) # leave it on for 1/2 second
    led.off() # Turn off the LED 
    sleep(delay) # leave it off for 1/2 second
