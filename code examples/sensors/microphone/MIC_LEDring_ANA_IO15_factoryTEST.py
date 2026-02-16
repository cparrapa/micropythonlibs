from machine import Pin, ADC
import neopixel
import time

# Define the number of LEDs
NUM_LEDS = 13

# Define GPIO pins
SOUND_SENSOR_PIN = 15
LED_PIN = 4

# Initialize sound sensor
adc = ADC(Pin(SOUND_SENSOR_PIN))
adc.atten(ADC.ATTN_11DB)  # Set attenuation to cover 0-3.3V range
adc.width(ADC.WIDTH_12BIT)  # Set resolution to 12 bits

# Initialize LED ring
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

# Read initial value from sound sensor
previous_reading = adc.read()

# List to store differences
diffs = []

# Calculate absolute difference
def calculate_diffs(current_reading, previous_reading):
    diff = abs(current_reading - previous_reading)
    return diff

# Calculate average difference
def calculate_average_diff(diffs):
    if len(diffs) == 0:
        return 0
    return sum(diffs) / len(diffs)

# Set LED brightness
def set_leds(avg_diff):
    if avg_diff < 10:
        leds_to_light = 1  # LED0 remains lit
    elif 10 <= avg_diff < 19:
        leds_to_light = 2  # LED0 and LED1 are lit
    elif avg_diff > 130:
        leds_to_light = NUM_LEDS  # All LEDs are fully lit
    else:
        leds_to_light = int((avg_diff - 20) / (180 - 20) * (NUM_LEDS - 2)) + 2  # Proportionally light LED2 to LED12

    for i in range(NUM_LEDS):
        if i < leds_to_light:
            np[i] = (0, 0, 255)  # Blue color
        else:
            np[i] = (0, 0, 0)    # Turn off LED
    np.write()

while True:
    # Read analog value from sound sensor
    current_reading = adc.read()
    
    # Calculate difference between current and previous readings
    diff = calculate_diffs(current_reading, previous_reading)
    diffs.append(diff)
    
    # Keep diffs list length under control
    if len(diffs) > 1:
        diffs.pop(0)
    
    # Calculate average difference
    average_diff = calculate_average_diff(diffs)
    
    # Set LED brightness based on average difference
    set_leds(average_diff)
    
    # Update previous reading
    previous_reading = current_reading
    
    # Print readings and differences
    print(f'Reading: {current_reading} Diff: {diff} Avg Diff: {average_diff}')
    
    # Small delay to avoid overly frequent reads
    time.sleep(0.1)
