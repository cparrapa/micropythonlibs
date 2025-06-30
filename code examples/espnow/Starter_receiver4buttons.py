from machine import Pin, ADC, PWM, SoftI2C
from neopixel import NeoPixel
from time import sleep
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
from ottoneopixel import OttoUltrasonic
import network, espnow, machine

offset = 0

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

led_pin = machine.Pin(2, machine.Pin.OUT)
buzzer = OttoBuzzer(25)
motor = OttoMotor(13, 14)             # Connectors 10 & 11
ultrasonic = OttoUltrasonic(18, 19)   # Connector 1
motor.leftServo.freq(50)
motor.rightServo.freq(50)
ring = OttoNeoPixel(4, 13)             # Connector 5
ring.fillAllRing(0, 255, 255)
ultrasonic.ultrasonicRGB2(0, 255, 255)

while True:
    _, msg = esp.recv()
    if msg:             # msg == None if timeout in recv()
        if msg == b'AOn':
            print("Turning on LED")
            led_pin.on()
            ring.fillAllRing(255, 0, 0)
            buzzer.playNote(261, 125)
            motor.leftServo.duty(127- offset)
            motor.rightServo.duty(29+ offset)
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
            motor.rightServo.duty(100+ offset)
            motor.leftServo.duty(100- offset)
        elif msg == b'Coff':
            ring.fillAllRing(0, 0, 0)
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'Don':
            ring.fillAllRing(0, 255, 0)
            buzzer.playNote(349, 125)
            motor.rightServo.duty(70+ offset)
            motor.leftServo.duty(70- offset)
        elif msg == b'Doff':
            ring.fillAllRing(0, 0, 0)
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        else:
            print("Unknown message!")
