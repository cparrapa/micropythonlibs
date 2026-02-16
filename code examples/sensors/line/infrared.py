import machine
import time

# Define the GPIO pin where the IR sensor is connected
ir_pin = machine.Pin(14, machine.Pin.IN)  # Change the pin number as per your connection

# Initialize variables
last_time = 0
time_differences = []

while True:
    # Read the value from the IR sensor
    ir_value = ir_pin.value()
    
    if ir_value == 0:
        current_time = time.ticks_us()  # Get the current time in microseconds
        
        if last_time != 0:
            # Calculate the time difference between consecutive 0 values
            time_diff = time.ticks_diff(current_time, last_time)
            time_differences.append(time_diff)
            print("Time difference:", time_diff, "microseconds")
        
        # Update the last_time to the current time
        last_time = current_time
        
    # Add a small delay to avoid high CPU usage
    time.sleep_ms(1)
