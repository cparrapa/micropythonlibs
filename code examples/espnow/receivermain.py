from machine import Pin, ADC, PWM, SoftI2C #importing classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
import network
import espnow
import machine

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()      # For ESP8266

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

led_pin = machine.Pin(2, machine.Pin.OUT)

bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5

ring.fillAllRing(0, 255, 0)

while True:
    _, msg = esp.recv()
    if msg:             # msg == None if timeout in recv()
        if msg == b'ledOn':
            print("Turning on LED")
            led_pin.on()
            ring.fillAllRing(255, 0, 0)
        elif msg == b'ledOff':
            print("Turning off LED")
            led_pin.off()
            ring.fillAllRing(0, 0, 255)
        elif msg == b'Bon':
            print("Turning off LED")
            led_pin.on()
            ring.fillAllRing(0, 255, 255)
        elif msg == b'Boff':
            print("Turning off LED")
            led_pin.off()
            ring.fillAllRing(0, 255, 0)
        else:
            print("Unknown message!")

