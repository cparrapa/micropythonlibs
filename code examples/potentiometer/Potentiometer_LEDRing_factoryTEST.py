import machine
import neopixel
import utime

# Define the number of LEDs
NUM_LEDS = 13

# Define the GPIO pins
POT_PIN = 26
LED_PIN = 4

# Initialize the potentiometer
pot = machine.ADC(machine.Pin(POT_PIN))
pot.atten(machine.ADC.ATTN_11DB)  # Set the attenuation for full range

# Initialize the LED ring
np = neopixel.NeoPixel(machine.Pin(LED_PIN), NUM_LEDS)

def set_leds(brightness):
    """Set the number of LEDs based on the brightness value."""
    leds_to_light = int((brightness / 3900) * NUM_LEDS)
    for i in range(NUM_LEDS):
        if i < leds_to_light:
            np[i] = (0, 0, 255)  # Blue color
        else:
            np[i] = (0, 0, 0)    # Turn off LED
    np.write()

while True:
    # Read the potentiometer value
    pot_value = pot.read()
    
    # Set the LEDs based on the potentiometer value
    set_leds(pot_value)
    
    # Small delay to debounce potentiometer
    utime.sleep(0.1)
