# Controller sender 4 buttons with button green pcb v4
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

# b'\xb0\xa72#\xc9h' colombia
peer = b'\xfc\xb4g}\xb7\xe0'
esp.add_peer(peer)

# Set up buttons, buzzer, and LED
buttonA_pin = Pin(26, Pin.IN, Pin.PULL_UP) # Connector 4 UP forward
buttonB_pin = Pin(32, Pin.IN, Pin.PULL_UP) # Connector 6 DOWN backward
buttonC_pin = Pin(4 , Pin.IN, Pin.PULL_UP) # Connector 5 LEFT turn
buttonD_pin = Pin(33, Pin.IN, Pin.PULL_UP) # Connector 7 RIGTH turn
buttonE_pin = Pin(15, Pin.IN, Pin.PULL_UP) # Connector 9
buttonF_pin = Pin(13, Pin.IN, Pin.PULL_UP) # Connector 11
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
        if current_buttonA_state == 0: # CHANGE TO 0 if button is Normally Open
            message = "A" # Press UP
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
            message = "B" # Press DOWN
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
            message = "C" # Press LEFT
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
            message = "D" # Press RIGHT
        else:
            message = "Doff"
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonD_state = current_buttonD_state
        
    # Check for button combinations
    if buttonA_pin.value() == 0 and buttonC_pin.value() == 0:
        message = "AC"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)  # Prevent multiple triggers

    elif buttonA_pin.value() == 0 and buttonD_pin.value() == 0:
        message = "AD"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)

    elif buttonB_pin.value() == 0 and buttonC_pin.value() == 0:
        message = "BC"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)

    elif buttonB_pin.value() == 0 and buttonD_pin.value() == 0:
        message = "BD"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)
        
    elif buttonA_pin.value() == 0 and buttonB_pin.value() == 0:
        message = "AB"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)
        
    elif buttonC_pin.value() == 0 and buttonD_pin.value() == 0:
        message = "CD"
        print(f"Sending combo command: {message}")
        esp.send(peer, message.encode())
        utime.sleep_ms(300)
"""
    # Debounce Button E
    current_buttonE_state = buttonE_pin.value()
    if current_buttonE_state != last_buttonE_state:
        utime.sleep_ms(debounce_delay)
        current_buttonE_state = buttonE_pin.value()
        if current_buttonE_state == 1:
            message = "E"
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
        if current_buttonF_state == 1:
            message = "F"
        else:
            message = "Foff"
        print(f"Sending command: {message}")
        esp.send(peer, message.encode())
        last_buttonF_state = current_buttonF_state
"""

