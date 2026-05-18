# Robot receiver 4 buttons with speed normalization & combo support
from machine import Pin
from time import sleep
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel, OttoUltrasonic
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
import network, espnow

# ---------------- Calibration ----------------
STOP_LEFT = 80     # stop duty for left servo (tune experimentally)
STOP_RIGHT = 82    # stop duty for right servo (tune experimentally)
SCALE = 40         # scale factor: duty change per 100% speed
OFFSET = -10       # fine tuning to keep robot straight

def set_speed(left_speed, right_speed):
    """
    Set motor speeds in range [-100, 100].
    Positive = forward, Negative = backward.
    """
    left_duty = STOP_LEFT + int(left_speed * SCALE / 100)
    right_duty = STOP_RIGHT - int(right_speed * SCALE / 100) + OFFSET
    
    motor.leftServo.duty(left_duty)
    motor.rightServo.duty(right_duty)

# ---------------- Wi-Fi / ESP-NOW Setup ----------------
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.config(channel=1)   # Force fixed channel on both devices
sta.disconnect()

esp = espnow.ESPNow()
esp.active(True)

# ---------------- Hardware Setup ----------------
led_pin = Pin(2, Pin.OUT)
buzzer = OttoBuzzer(25)
motor = OttoMotor(13, 14)             # Connectors 10 & 11
ultrasonic = OttoUltrasonic(18, 19)   # Connector 1
motor.leftServo.freq(50)
motor.rightServo.freq(50)

ring = OttoNeoPixel(4, 13)            # Connector 5
ring.setRGBring(0, "fe0000")
ultrasonic.ultrasonicRGB2(255, 0, 0)  # just some color at startup

# Boot-up tones and lights
boot_notes = [261, 293, 329, 349, 392, 440, 493, 523, 261, 293, 329, 349, 392]
for i, note in enumerate(boot_notes):
    ring.setRGBring(i % 13, "fe0000")
    buzzer.playNote(note, 75)

# ---------------- Main Loop ----------------
while True:
    # Blocking wait for next ESP-NOW message
    host, msg = esp.recv()

    if not msg:
        continue

    # ------------ Single-button commands ------------
    if msg == b'A':   # UP forward
        set_speed(95, 100)

    elif msg == b'AOff':
        set_speed(0, 0)

    elif msg == b'B':  # DOWN backward
        set_speed(-100, -100)

    elif msg == b'Boff':
        set_speed(0, 0)

    elif msg == b'C':  # Turn LEFT on spot
        set_speed(-60, 60)

    elif msg == b'Coff':
        set_speed(0, 0)

    elif msg == b'D':  # Turn RIGHT on spot
        set_speed(60, -60)

    elif msg == b'Doff':
        set_speed(0, 0)

    # ------------ Combo commands ------------
    elif msg == b'AC':   # forward + left -> forward arc left
        set_speed(60, 100)

    elif msg == b'AD':   # forward + right -> forward arc right
        set_speed(100, 60)

    elif msg == b'BC':   # back + left -> backward arc left
        set_speed(-60, -100)

    elif msg == b'BD':   # back + right -> backward arc right
        set_speed(-100, -60)

    elif msg == b'AB':   # forward + back -> contradict -> stop
        set_speed(0, 0)

    elif msg == b'CD':   # left + right -> contradict -> stop
        set_speed(0, 0)

    else:
        print("Unknown message:", msg)
