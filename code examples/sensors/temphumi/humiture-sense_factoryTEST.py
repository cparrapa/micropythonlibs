import dht
import machine
import time

# Initialize the DHT11 sensor PORT 5
dht_pin = machine.Pin(4, machine.Pin.IN)
dht_sensor = dht.DHT11(dht_pin)

# Initialize the LED (DON)
led_pin = machine.Pin(2, machine.Pin.OUT)

# Function to read from the DHT11 sensor and control the LED
def read_dht11_and_control_led():
    while True:
        try:
            # Set pin to input for DHT11
            dht_pin.init(machine.Pin.IN)
            dht_sensor.measure()
            temperature = dht_sensor.temperature()
            humidity = dht_sensor.humidity()
            print('Temperature:', temperature, 'C')
            print('Humidity:', humidity, '%')

            # Set pin to output for LED and turn it on
            led_pin.init(machine.Pin.OUT)
            led_pin.on()  # Turn on the LED
            time.sleep(0.5)  # Keep the LED on for a short duration
            led_pin.off()  # Turn off the LED
        except OSError as e:
            print('Failed to read sensor. Retrying...')
            led_pin.off()  # Ensure the LED is off if there's an error
        time.sleep(2)  # Delay for 2 seconds

# Allow time for sensor to stabilize
time.sleep(2)

# Start the process
read_dht11_and_control_led()
