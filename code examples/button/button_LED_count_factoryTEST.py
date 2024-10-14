from machine import Pin
import neopixel
import time

# Define the number of LEDs
NUM_LEDS = 13

# Define GPIO pins
BUTTON_PIN = 26 # Connector 4
LED_PIN = 4 	# Connector5

# Initialize button and LED ring
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# Current LED count
led_count = 0

# Button state
last_button_state = button.value()

# Function to set LED brightness
def set_leds(count):
    for i in range(NUM_LEDS):
        if i < count:
            np[i] = (0, 0, 255)  # Blue color
        else:
            np[i] = (0, 0, 0)    # Turn off LED
    np.write()

while True:
    # Read button state
    current_button_state = button.value()
    
    # Check for button press (falling edge trigger)
    if last_button_state == 1 and current_button_state == 0:
        led_count += 1
        if led_count > NUM_LEDS:
            led_count = 0  # Reset count and turn off all LEDs
        
        set_leds(led_count)
    
    # Update button state
    last_button_state = current_button_state
    
    # Small delay to avoid overly frequent reads
    time.sleep(0.05)
