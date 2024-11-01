from machine import Pin
import neopixel
import time

# Define the number of LEDs
NUM_LEDS = 13

# Define the GPIO pins
LED_PIN = 4 #PORT 5
DT_PIN = 17 #PORT 2
CLK_PIN = 16 #PORT 2
BTN_PIN = 26 #PORT 4

# Initialize the LED ring
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# Initialize the encoder pins
dt = Pin(DT_PIN, Pin.IN)
clk = Pin(CLK_PIN, Pin.IN)
btn = Pin(BTN_PIN, Pin.IN, Pin.PULL_UP)

# Variables to keep track of the encoder state
last_clk = clk.value()
encoder_value = 0

def update_leds(value):
    """Update the LEDs based on the encoder value."""
    led_index = value % NUM_LEDS
    for i in range(NUM_LEDS):
        if i == led_index:
            np[i] = (0, 0, 255)  # Blue color
        else:
            np[i] = (0, 0, 0)    # Turn off LED
    np.write()

def all_leds_on():
    """Turn all LEDs on."""
    for i in range(NUM_LEDS):
        np[i] = (0, 0, 255)  # Blue color
    np.write()

while True:
    clk_value = clk.value()
    dt_value = dt.value()

    # Detect rotation
    if clk_value != last_clk:
        if dt_value != clk_value:
            encoder_value += 1
        else:
            encoder_value -= 1
        update_leds(encoder_value)
    
    # Check if button is pressed
    if btn.value() == 0:
        all_leds_on()
    else:
        update_leds(encoder_value)
    
    last_clk = clk_value
    time.sleep(0.01)
