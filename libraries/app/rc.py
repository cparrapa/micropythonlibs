import random, ubluetooth
import array  # Needed for polygons
from machine import Pin, Timer, PWM, ADC
from time import sleep_ms, sleep, ticks_ms, ticks_diff
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoNeoPixel, OttoUltrasonic
from ottomotor import OttoMotor
from ottosensors import FollowLine

led = Pin(2, Pin.OUT)  # Built in LED
buzzer = OttoBuzzer(25)  # Built in Buzzer
ultrasonic = OttoUltrasonic(18, 19)  # Connector 1
analog = Pin(26, Pin.IN)  # Connector 4
n = 13  # Number of LEDs in ring
ring = OttoNeoPixel(4, n)  # Connector 5
ring.setBrightness(5)  # brightness  for lights
line = FollowLine(32, 33, 27, 15)  # Connectors 6 to 9
sensorL = ADC(Pin(32))  # Connector 6 analog
sensorR = ADC(Pin(33))  # Connector 7 analog
motor = OttoMotor(13, 14)  # Connectors 10 & 11
toggleStatus = False
mode = 0
sliderR = 50
sliderL = 50
battery = ADC(Pin(39))
battery.atten(ADC.ATTN_11DB)  # 0 - 3.3v range
battery_percentage = 0

# servo duty values
loDutyL = 25
hiDutyL = 125
midDutyL = 75  # int(loDutyL + (hiDutyL - loDutyL)/2)

loDutyR = 25
hiDutyR = 125
midDutyR = 75  # int(loDutyR + (hiDutyR - loDutyR)/2)

face = ""
oled = ""
matrix = ""

def MotorsMove(right_speed, left_speed, direction, t=None):
    right_speed = int(right_speed / 2)
    left_speed = int(left_speed / 2)

    if direction == "forward":
        motor.leftServo.duty(midDutyL + left_speed)
        motor.rightServo.duty(midDutyR - right_speed)
    elif direction == "backward":
        motor.leftServo.duty(midDutyL - left_speed)
        motor.rightServo.duty(midDutyR + right_speed)
    elif direction == "right":
        motor.leftServo.duty(midDutyL + left_speed)
        motor.rightServo.duty(midDutyR + right_speed)
    elif direction == "left":
        motor.leftServo.duty(midDutyL - left_speed)
        motor.rightServo.duty(midDutyR - right_speed)
    else:
        raise ValueError("Invalid direction")

    if t is not None:
        sleep(t)
        motor.Stop(1)


def fwd():
    MotorsMove(sliderR, sliderL, "forward", 1)

def bwd():
    MotorsMove(sliderR, sliderL, "backward", 1)

def left():
    MotorsMove(sliderR, sliderL, "left", 1)

def right():
    MotorsMove(sliderR, sliderL, "right", 1)

def ndo():
    buzzer.tone(buzzer.NOTE_C4, 100, 100)

def nre():
    buzzer.tone(buzzer.NOTE_D4, 100, 100)

def nmi():
    buzzer.tone(buzzer.NOTE_E4, 100, 100)

def nfa():
    buzzer.tone(buzzer.NOTE_F4, 100, 100)
def nsol():
    buzzer.tone(buzzer.NOTE_G4, 100, 100)
def nla():
    buzzer.tone(buzzer.NOTE_A4, 100, 100)

def nsi():
    buzzer.tone(buzzer.NOTE_B4, 100, 100)

def nedo():
    buzzer.tone(buzzer.NOTE_C5, 100, 100)
