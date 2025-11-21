# Robot receiver 4 buttons
from machine import Pin, ADC, PWM, SoftI2C
from time import sleep
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottoneopixel import OttoUltrasonic
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
import network, espnow, machine

offset = 0

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

led_pin = Pin(2, Pin.OUT)
buzzer = OttoBuzzer(25)
motor = OttoMotor(13, 14)             # Connectors 10 & 11
ultrasonic = OttoUltrasonic(18, 19)   # Connector 1
motor.leftServo.freq(50)
motor.rightServo.freq(50)
ring = OttoNeoPixel(4, 13)             # Connector 5
ring.setRGBring(0, "fe0000")
ultrasonic.ultrasonicRGB2(255, 0, 0)
buzzer.playNote(261, 75)
ring.setRGBring(1, "fe0000")
ring.setRGBring(2, "fe0000")
buzzer.playNote(293, 75)
ring.setRGBring(3, "fe0000")
ring.setRGBring(4, "fe0000")
buzzer.playNote(329, 75)
ring.setRGBring(5, "fe0000")
ring.setRGBring(6, "fe0000")
buzzer.playNote(349, 75)
ring.setRGBring(7, "fe0000")
ring.setRGBring(8, "fe0000")
buzzer.playNote(392, 75)
ring.setRGBring(9, "fe0000")
buzzer.playNote(440, 75)
ring.setRGBring(10, "fe0000")
buzzer.playNote(493, 75)
ring.setRGBring(11, "fe0000")
buzzer.playNote(523, 75)
ring.setRGBring(12, "fe0000")

while True:
    _, msg = esp.recv()
    if msg:             # msg == None if timeout in recv()
        if msg == b'A': # UP pressed forward
            print("Turning on LED")
            #led_pin.on()
                            # 0			1		2			3		4			5			6		7			8		9			10		11			12
            ring.fillRGBRing("fe0000", "fe0000", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "fe0000", "fe0000")
            buzzer.playNote(261, 125)
            motor.leftServo.duty(127- offset)
            motor.rightServo.duty(29+ offset)
        elif msg == b'AOff':
            #print("Turning off LED")
            ring.fillAllRing(0, 0, 0)
            ring.setRGBring(0, "fe0000")
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'B': # DOWN oressed backward
            ring.fillRGBRing("fe0000", "000000", "000000", "000000", "000000", "fe0000", "fe0000", "fe0000", "000000", "000000", "000000", "000000", "000000")
            buzzer.playNote(293, 125)
            motor.leftServo.duty(43- offset)
            motor.rightServo.duty(109+ offset)
            sleep(0.1)
        elif msg == b'Boff':
            ring.fillAllRing(0, 0, 0)
            ring.setRGBring(0, "fe0000")
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'C': # Turn LEFT pressed
            ring.fillRGBRing("fe0000", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "fe0000", "fe0000", "fe0000", "000000", "000000")
            buzzer.playNote(329, 125)
            motor.rightServo.duty(60+ offset)
            motor.leftServo.duty(60- offset)
        elif msg == b'Coff':
            ring.fillAllRing(0, 0, 0)
            ring.setRGBring(0, "fe0000")
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
        elif msg == b'D': # Turn RIGHT pressed
            ring.fillRGBRing("fe0000", "000000", "fe0000", "fe0000", "fe0000", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000000")
            buzzer.playNote(349, 125)
            motor.rightServo.duty(100+ offset)
            motor.leftServo.duty(100- offset)
        elif msg == b'Doff':
            ring.fillAllRing(0, 0, 0)
            ring.setRGBring(0, "fe0000")
            motor.rightServo.duty(0)
            motor.leftServo.duty(0)
            """
        elif msg == b'E':
            ring.fillAllRing(0, 255, 130)
            buzzer.playNote(392, 125)
            ultrasonic.ultrasonicRGB2(0, 255, 130)
            motor.rightServo.duty(60+ offset)
            motor.leftServo.duty(60- offset)
        elif msg == b'Eoff':
            led_pin.off()
            ring.fillAllRing(0, 0, 0)
        elif msg == b'F':
            ring.fillAllRing(0, 120, 255)
            ultrasonic.ultrasonicRGB2(0, 120, 255)
            buzzer.playNote(440, 125)
            motor.rightServo.duty(95+ offset)
            motor.leftServo.duty(95- offset)
        elif msg == b'Foff':
            led_pin.off()
            ring.fillAllRing(0, 0, 0)
            """
