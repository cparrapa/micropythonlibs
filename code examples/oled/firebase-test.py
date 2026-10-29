import network
import urequests
import time
import machine

# Firebase URL and secret key
FIREBASE_URL = "https://controlesp32-e47b3-default-rtdb.firebaseio.com/commands.json"
CHECK_INTERVAL = 5  # Check every 5 seconds

# Connect to WiFi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("ssid", "password")

    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)

    print("Connected to WiFi:", wlan.ifconfig())

# Fetch command from Firebase
def fetch_command():
    try:
        response = urequests.get(FIREBASE_URL)
        if response.status_code == 200:
            data = response.json()
            if data:
                # Get the last command entry
                last_command = list(data.values())[-1]
                command = last_command.get('command')
                return command
            else:
                print("No commands found")
        else:
            print("Failed to fetch command:", response.status_code)
    except Exception as e:
        print("Error fetching command:", e)

# Control LED
def control_led(command):
    if command == "LED ON":
        led.value(1)  # Turn LED on
        print("LED turned ON")
    elif command == "LED OFF":
        led.value(0)  # Turn LED off
        print("LED turned OFF")
    else:
        print("Unknown command:", command)

# Main loop
def main():
    global led
    led = machine.Pin(2, machine.Pin.OUT)  # GPIO2 for the built-in LED

    ssid = "@@"
    password = "@@"

    connect_wifi(ssid, password)

    while True:
        command = fetch_command()
        if command:
            control_led(command)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

