from machine import ADC, Pin
import neopixel
import utime

# Define the number of LEDs
NUM_LEDS = 13

# Define the GPIO pins
LIGHT_SENSOR_PIN = 14 #PORT 10
LED_PIN = 4 #PORT 5

# Initialize the light sensor
adc_pin = Pin(LIGHT_SENSOR_PIN)
adc = ADC(adc_pin)
adc.atten(ADC.ATTN_11DB)  # Full range: 3.3v
adc.width(ADC.WIDTH_12BIT)  # 12-bit resolution

# Initialize the LED ring
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

def set_leds(brightness):
    """Set the number of LEDs based on the brightness value."""
    leds_to_light = int((brightness / 2000) * NUM_LEDS)
    for i in range(NUM_LEDS):
        if i < leds_to_light:
            np[i] = (0, 0, 255)  # Blue color
        else:
            np[i] = (0, 0, 0)    # Turn off LED
    np.write()

while True:
    # Read the light sensor value
    adc_value = adc.read()
    
    # Ensure adc_value is capped at 2100 for proper scaling
    adc_value = min(adc_value, 2100)
    
    # Set the LEDs based on the light sensor value
    set_leds(adc_value)
    
    # Small delay to debounce sensor reading
    utime.sleep(0.1)
