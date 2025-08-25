from machine import Pin, time_pulse_us  # Import Pin class and time_pulse_us for timing ultrasonic signal
import time  # Import time module for delays

# Initialize pins
TRIG = Pin(3, Pin.OUT)   # Trigger pin of ultrasonic sensor (GPIO 3)
ECHO = Pin(2, Pin.IN)    # Echo pin of ultrasonic sensor (GPIO 2)
buzzer = Pin(15, Pin.OUT)  # Buzzer connected to GPIO 15
led = Pin(25, Pin.OUT)     # Onboard LED for visual feedback (GPIO 25)

# Function to measure distance using ultrasonic sensor
def get_distance():
    TRIG.low()           # Ensure trigger is LOW
    time.sleep_us(2)     # Short delay for stability
    TRIG.high()          # Send a 10 microsecond HIGH pulse
    time.sleep_us(10)
    TRIG.low()

    # Measure the time duration that ECHO is HIGH (max timeout 30 ms)
    pulse_time = time_pulse_us(ECHO, 1, 30000)

    # Calculate distance in cm: speed of sound is ~343 m/s → 29.1 µs/cm round-trip
    distance_cm = (pulse_time / 2) / 29.1
    return distance_cm

# Main loop
while True:
    dist = get_distance()  # Measure distance
    print("Distance:", dist, "cm")  # Print it for debugging

    if dist < 30:  # If object is within 50 cm
        if dist < 5:
            # If object is very close (<5 cm), buzzer and LED stay ON
            buzzer.value(1)
            led.value(1)
        else:
            # For distances between 5–50 cm, blink buzzer and LED faster as object gets closer
            delay = max(0.01, dist / 1000)  # Delay between buzzes: closer = faster

            buzzer.value(1)
            led.value(1)
            time.sleep(delay)

            buzzer.value(0)
            led.value(0)
            time.sleep(delay)
    else:
        # If object is far away (>50 cm), turn everything off
        buzzer.value(0)
        led.value(0)

    time.sleep(0.2)  # Small pause before next measurement

