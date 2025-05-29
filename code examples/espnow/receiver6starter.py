from machine import Pin, ADC, PWM, SoftI2C #importing classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from time import sleep
from ottomotor import OttoMotor
offset = 0

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
buzzer = OttoBuzzer(25)
motor = OttoMotor(13, 14)             # Connectors 10 & 11

motor.leftServo.freq(50)
motor.rightServo.freq(50)

n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5

ring.fillAllRing(0, 255, 0)

while True:
    _, msg = esp.recv()
    if msg:             # msg == None if timeout in recv()
        if msg == b'AOn':
            print("Turning on LED")
            led_pin.on()
            ring.fillAllRing(255, 0, 0)
            buzzer.playNote(261, 125)
            motor.leftServo.duty(109- offset)
            motor.rightServo.duty(43+ offset)
        elif msg == b'AOff':
            print("Turning off LED")
            led_pin.off()
            ring.fillAllRing(0, 0, 0)
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'Bon':
            ring.fillAllRing(255, 130, 0)
            buzzer.playNote(293, 125)
            motor.leftServo.duty(43- offset)
            motor.rightServo.duty(109+ offset)
            sleep(0.1)
        elif msg == b'Boff':
            ring.fillAllRing(0, 0, 0)
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'Con':
            ring.fillAllRing(255, 255, 0)
            buzzer.playNote(329, 125)
            motor.rightServo.duty(115+ offset)
            motor.leftServo.duty(115- offset)
        elif msg == b'Coff':
            ring.fillAllRing(0, 0, 0)
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'Don':
            ring.fillAllRing(0, 255, 0)
            buzzer.playNote(349, 125)
            motor.rightServo.duty(45+ offset)
            motor.leftServo.duty(45- offset)
        elif msg == b'Doff':
            ring.fillAllRing(0, 0, 0)
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'Eon':
            ring.fillAllRing(0, 255, 130)
            buzzer.playNote(392, 125)
        elif msg == b'Eoff':
            ring.fillAllRing(0, 0, 0)
        elif msg == b'Fon':
            ring.fillAllRing(0, 120, 255)
            buzzer.playNote(440, 125)
        elif msg == b'Foff':
            ring.fillAllRing(0, 0, 0)
        else:
            print("Unknown message!")

