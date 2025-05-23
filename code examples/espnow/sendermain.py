import network
from machine import Pin
import espnow
import utime
from ottobuzzer import OttoBuzzer

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Define the MAC address of the receiving ESP32 (ESP32 B)
peer = b'\x08\xd1\xf9\xfb\xf5\xc8'
esp.add_peer(peer)

# Create a function to send data when a button is pressed (optional)
buttonA_pin = Pin(26, Pin.IN, Pin.PULL_UP)
buttonB_pin = Pin(27, Pin.IN, Pin.PULL_UP)
buttonC_pin = Pin(15, Pin.IN, Pin.PULL_UP)
buzzer = OttoBuzzer(25)
led = Pin(2, Pin.OUT) 

# Initialize variables for debouncing
last_button_state = 1  # Assuming the button is not pressed initially
debounce_delay = 50  # Adjust this value to your needs (milliseconds)

while True:
    # Read the current state of the button
    current_button_state = buttonA_pin.value()
    
    if buttonB_pin.value() == 0:
                led.on()
                buzzer.playEmoji("S_happy")
                message = "Bon"
                print(f"Sending command : {message}")
                esp.send(peer, message)
    else:
        led.off()
        message = "Boff"
        print(f"Sending command : {message}")
        esp.send(peer, message)
    # Check if the button state has changed
    if current_button_state != last_button_state:
        # Wait for a short time to debounce the button
        utime.sleep_ms(debounce_delay)
        
        # Read the button state again to make sure it's stable
        current_button_state = buttonA_pin.value()
                
        # If the button state is still different, it's a valid press
        if current_button_state != last_button_state:
            if current_button_state == 0:
                message = "ledOn"
                print(f"Sending command : {message}")
                esp.send(peer, message)
            else:
                message = "ledOff"
                print(f"Sending command : {message}")
                esp.send(peer, message)
        # Update the last button state
        last_button_state = current_button_state
