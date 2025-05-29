import network
from machine import Pin
import espnow
import utime
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
buttonA_pin = Pin(26, Pin.IN, Pin.PULL_UP)
buttonB_pin = Pin(27, Pin.IN, Pin.PULL_UP)
buttonC_pin = Pin(4, Pin.IN, Pin.PULL_UP)
buttonD_pin = Pin(33, Pin.IN, Pin.PULL_UP)
buttonE_pin = Pin(15, Pin.IN, Pin.PULL_UP)
buttonF_pin = Pin(13, Pin.IN, Pin.PULL_UP)
buzzer = OttoBuzzer(25)
led = Pin(2, Pin.OUT)

debounce_delay = 50

# Store last known states for all buttons
last_buttonA_state = buttonA_pin.value()
last_buttonB_state = buttonB_pin.value()
last_buttonC_state = buttonC_pin.value()
last_buttonD_state = buttonD_pin.value()
last_buttonE_state = buttonE_pin.value()
last_buttonF_state = buttonF_pin.value()

while True:
    # Debounce Button A
    current_buttonA_state = buttonA_pin.value()
    if current_buttonA_state != last_buttonA_state:
        utime.sleep_ms(debounce_delay)
        current_buttonA_state = buttonA_pin.value()
        if current_buttonA_state == 0:
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
        if current_buttonB_state == 0:
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

    # Debounce Button E
    current_buttonE_state = buttonE_pin.value()
    if current_buttonE_state != last_buttonE_state:
        utime.sleep_ms(debounce_delay)
        current_buttonE_state = buttonE_pin.value()
        if current_buttonE_state == 0:
            message = "Eon"
        else:
            message = "Eoff"
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonE_state = current_buttonE_state
        
    # Debounce Button F
    current_buttonF_state = buttonF_pin.value()
    if current_buttonF_state != last_buttonF_state:
        utime.sleep_ms(debounce_delay)
        current_buttonF_state = buttonF_pin.value()
        if current_buttonF_state == 0:
            message = "Fon"
        else:
            message = "Foff"
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonF_state = current_buttonF_state