import network, espnow, utime
from machine import Pin
from ottobuzzer import OttoBuzzer

# Set up Wi-Fi for ESP-NOW
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

# Define receiving ESP32 MAC address
peer = b'\x08\xd1\xf9\xfb\xf5\xc8'
esp.add_peer(peer)

# Set up buttons, buzzer, and LED
buttonA_pin = Pin(26, Pin.IN, Pin.PULL_UP) # Connector 4
buttonB_pin = Pin(32, Pin.IN, Pin.PULL_UP) # Connector 6
buttonC_pin = Pin(4, Pin.IN, Pin.PULL_UP)  # Connector 5
buttonD_pin = Pin(33, Pin.IN, Pin.PULL_UP) # Connector 7

buzzer = OttoBuzzer(25)
led = Pin(2, Pin.OUT)

debounce_delay = 50

# Store last known states for all buttons
last_buttonA_state = buttonA_pin.value()
last_buttonB_state = buttonB_pin.value()
last_buttonC_state = buttonC_pin.value()
last_buttonD_state = buttonD_pin.value()

while True:
    # Debounce Button A
    current_buttonA_state = buttonA_pin.value()
    if current_buttonA_state != last_buttonA_state:
        utime.sleep_ms(debounce_delay)
        current_buttonA_state = buttonA_pin.value()
        if current_buttonA_state == 1:
            message = "AOn"
        else:
            message = "AOff"
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonA_state = current_buttonA_state

    # Debounce Button B
    current_buttonB_state = buttonB_pin.value()
    if current_buttonB_state != last_buttonB_state:
        utime.sleep_ms(debounce_delay)
        current_buttonB_state = buttonB_pin.value()
        if current_buttonB_state == 1:
            message = "Bon"
            led.on()
        else:
            message = "Boff"
            led.off()
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonB_state = current_buttonB_state

    # Debounce Button C
    current_buttonC_state = buttonC_pin.value()
    if current_buttonC_state != last_buttonC_state:
        utime.sleep_ms(debounce_delay)
        current_buttonC_state = buttonC_pin.value()
        if current_buttonC_state == 0:
            message = "Con"
        else:
            message = "Coff"
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonC_state = current_buttonC_state
        
    # Debounce Button D
    current_buttonD_state = buttonD_pin.value()
    if current_buttonD_state != last_buttonD_state:
        utime.sleep_ms(debounce_delay)
        current_buttonD_state = buttonD_pin.value()
        if current_buttonD_state == 0:
            message = "Don"
        else:
            message = "Doff"
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonD_state = current_buttonD_state
        
    # Check for button combinations
    if buttonA_pin.value() == 1 and buttonC_pin.value() == 0:
        message = "Eon"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)  # Prevent multiple triggers

    elif buttonA_pin.value() == 1 and buttonD_pin.value() == 0:
        message = "Fon"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)

    elif buttonB_pin.value() == 1 and buttonC_pin.value() == 0:
        message = "Gon"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)

    elif buttonB_pin.value() == 1 and buttonD_pin.value() == 0:
        message = "Hon"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)