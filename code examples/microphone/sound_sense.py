# Import Pin and ADC class from the machine module
from machine import Pin, ADC
# Import the time module
import time

# Create an ADC object and associate it with pin 5
pin_adc = ADC(Pin(32))      
# Set the attenuation level to 11dB, which allows for a wider input voltage range
pin_adc.atten(ADC.ATTN_11DB)   

while True:
    sum_value = 0

    for i in range(32):
        # Read the ADC value and add it to the sum
        sum_value += pin_adc.read()   

    # Right shift the sum by 5 bits (equivalent to dividing by 32) to get the average value
    sum_value >>= 5   

    # Print the average value   
    print(sum_value)   
    # Pause for 100 milliseconds
    time.sleep_ms(100)