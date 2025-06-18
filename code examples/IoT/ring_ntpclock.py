import network
import ntptime
import time
import machine
import neopixel

# CONFIGURATION
WIFI_SSID = 'ssid'
WIFI_PASS = 'password'
NEOPIXEL_PIN = 4  # Changed to GPIO 4
NUM_LEDS = 13
CENTER_LED = 0
TIMEZONE_OFFSET = -5 * 3600  # Set your timezone offset in seconds (e.g., -3 for UTC-3)

LED_OFFSET = -1  # adjust this until 12 o'clock lines up visually

# Setup NeoPixel
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_LEDS)

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASS)
        while not wlan.isconnected():
            time.sleep(0.5)
    print("Connected:", wlan.ifconfig())

# Sync time using NTP
def sync_time():
    try:
        ntptime.settime()
        print("Time synced via NTP.")
    except:
        print("Failed to sync time.")

# Apply timezone offset manually
def get_local_time():
    t = time.time() + TIMEZONE_OFFSET
    return time.localtime(t)

# Map time to LED position (1–12)
def time_to_led(val, max_val):
    """Maps a time value (e.g., 15 seconds) to an LED index 1-12 with offset"""
    position = int((val / max_val) * 12)
    led_index = (position + LED_OFFSET) % 12 + 1
    return led_index
    
def set_fading_hand(position, max_value, color):
    """
    Draws a hand with fading between two LEDs.
    `position` = current time value (seconds, minutes)
    `max_value` = 60 for seconds/minutes
    `color` = tuple (R, G, B)
    """
    
    led_float = (position / max_value) * 12
    base_led = int(led_float)
    next_led = (base_led + 1) % 12

    # Apply offset and wrap
    base_led = (base_led + LED_OFFSET) % 12 + 1
    next_led = (next_led + LED_OFFSET) % 12 + 1

    fraction = led_float - int(led_float)

    def scale(c, f): return int(c * f)

    base_color = tuple(scale(c, 1 - fraction) for c in color)
    next_color = tuple(scale(c, fraction) for c in color)

    def add_color(led, add):
        r, g, b = np[led]
        ar, ag, ab = add
        np[led] = (min(255, r + ar), min(255, g + ag), min(255, b + ab))

    add_color(base_led, base_color)
    add_color(next_led, next_color)


# Show time on NeoPixel ring
def show_time():
    while True:
        t = time.localtime()
        hour = t[3] % 12 +2 # +2 since offset did not work
        minute = t[4]
        second = t[5]

        # Serial print
        print("Local Time: {:02}:{:02}:{:02}".format(hour if hour != 0 else 12, minute, second))

        # Clear LEDs
        np.fill((0, 0, 0))
        np[CENTER_LED] = (10, 10, 10)  # Center LED on

        # Hour LED - no fading
        hour_led = time_to_led(hour + minute / 60, 12)
        np[hour_led] = (50, 0, 0)

        # Minute and Second - fading hands
        set_fading_hand(minute, 60, (0, 50, 0))  # Green
        set_fading_hand(second, 60, (0, 0, 50))  # Blue

        np.write()


# Main program
connect_wifi()
sync_time()
show_time()

