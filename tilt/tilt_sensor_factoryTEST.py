from machine import Pin
import neopixel
import time

# Define the number of LEDs
NUM_LEDS = 13

# Define GPIO pins
TILT_SENSOR_PIN = 14 #PORT 10
LED_PIN = 4 #port 5

# Initialize tilt sensor and LED ring
tilt_sensor = Pin(TILT_SENSOR_PIN, Pin.IN, Pin.PULL_UP)
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# Current LED count
led_count = 0

# Tilt sensor state
last_tilt_state = tilt_sensor.value()

# Function to set LED brightness
def set_leds(count):
    for i in range(NUM_LEDS):
        if i < count:
            np[i] = (0, 0, 255)  # Blue color
        else:
            np[i] = (0, 0, 0)    # Turn off LED
    np.write()

while True:
    # Read tilt sensor state
    current_tilt_state = tilt_sensor.value()
    
    # Check for tilt activity (falling edge trigger)
    if last_tilt_state == 1 and current_tilt_state == 0:
        led_count += 1
        print(f"Tilt detected! LED count: {led_count}")
        if led_count > NUM_LEDS:
            led_count = 0  # Reset count and turn off all LEDs
        
        set_leds(led_count)
    
    # Update tilt sensor state
    last_tilt_state = current_tilt_state
    
    # Small delay to avoid overly frequent reads
    time.sleep(0.05)
