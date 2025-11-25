from machine import Pin, Timer, PWM, ADC, reset as machine_reset
from time import sleep
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoNeoPixel, OttoUltrasonic
from ottomotor import OttoMotor
from ottosensors import FollowLine
import os
import asyncio

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

# Sensor values
distance_sensor_enabled = False
line_sensors_enabled = False

# Color ring memory
color_ring_values = ["000000" for x in range(13)]
ultrasonic_sensors_colors = ("000000", "000000")

def motors_move(right_speed, left_speed, direction, t=None):
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
        return

    if t is not None:
        sleep(t)
        motor.Stop(1)

def handle_movement(command: str):
    if command[0] != 'M':
        return

    key = command[1:]
    if key == "f":
        motors_move(sliderR, sliderL, "forward", 1)
    elif key == "b":
        motors_move(sliderR, sliderL, "backward", 1)
    elif key == "l":
        motors_move(sliderR, sliderL, "left", 1)
    elif key == "r":
        motors_move(sliderR, sliderL, "right", 1)
    elif key == "fn":
        motors_move(sliderR, sliderL, "forward")
    elif key == "bn":
        motors_move(sliderR, sliderL, "backward")
    elif key == "ln":
        motors_move(sliderR, sliderL, "left")
    elif key == "rn":
        motors_move(sliderR, sliderL, "right")
    elif key == "X":
        motor.Stop(1)


def handle_movement_settings(command: str):
    if command[0:2] != 'MS':
        return

    key = command[2:]

    if key[0] == 's':
        global sliderL
        global sliderR
        sliderL = int(key[1:4])
        sliderR = int(key[4:])

def handle_tones(command: str):
    if command[0] != 'N':
        return

    key = command[1:]
    if key == "do":
        buzzer.tone(buzzer.NOTE_C4, 100, 100)
    elif key == "re":
        buzzer.tone(buzzer.NOTE_D4, 100, 100)
    elif key == "mi":
        buzzer.tone(buzzer.NOTE_E4, 100, 100)
    elif key == "fa":
        buzzer.tone(buzzer.NOTE_F4, 100, 100)
    elif key == "sol":
        buzzer.tone(buzzer.NOTE_G4, 100, 100)
    elif key == "la":
        buzzer.tone(buzzer.NOTE_A4, 100, 100)
    elif key == "si":
        buzzer.tone(buzzer.NOTE_B4, 100, 100)
    elif key == "edo":
        buzzer.tone(buzzer.NOTE_C5, 100, 100)


def convert_joystick_degrees(deg: int) -> int:
    rounded = round(deg / 10) * 10

    if rounded == 360:
        rounded = 0

    return rounded

def interpolate_motor_value(mid: int, target: int, speed: int) -> int:
    if speed < 1:
        speed = 1
    elif speed > 10:
        speed = 10

    difference = target - mid

    scaled_difference = difference * (speed / 10.0)

    return int(mid + scaled_difference)

def handle_joystick_motor_values(deg: int, speed: int):
    converted_degrees = convert_joystick_degrees(deg)
    motor_values = {
        "0": (125, 25), "10": (125, 31), "20": (125, 37), "30": (125, 43),
        "40": (125, 49), "50": (125, 55), "60": (125, 61), "70": (125, 67),
        "80": (125, 73), "90": (125, 125), "100": (25, 79), "110": (25, 85),
        "120": (25, 91), "130": (25, 97), "140": (25, 103), "150": (25, 109),
        "160": (25, 115), "170": (25, 121), "180": (25, 125), "190": (31, 125),
        "200": (37, 125), "210": (43, 125), "220": (49, 125), "230": (55, 125),
        "240": (61, 125), "250": (67, 125), "260": (73, 125), "270": (25, 25),
        "280": (81, 25), "290": (87, 25), "300": (93, 25), "310": (99, 25),
        "320": (105, 25), "330": (111, 25), "340": (117, 25), "350": (123, 25),
    }

    found_motor_values = motor_values[str(converted_degrees)]
    motor.leftServo.duty(interpolate_motor_value(midDutyL, found_motor_values[0], speed))
    motor.rightServo.duty(interpolate_motor_value(midDutyR, found_motor_values[1], speed))

def handle_joystick(command: str):
    if command[0] != 'J':
        return

    joystick_value = command[1:]
    if joystick_value == 'X':
        motor.Stop(1)
        return

    args = joystick_value.split("#")
    deg = int(args[0])
    speed = int(args[1])

    handle_joystick_motor_values(deg, speed)

def handle_tools(command: str):
    if command[0] != 'T':
        return

    key = command[1:]
    if key == 'rusrc':
        try:
            os.remove("usercode.py")
        except:
            pass
    elif key == 'rst':
        machine_reset()


def decode_color(color: str):
    if color == "a":
        return "000000"
    elif color == "b":
        return "FFFFFF"
    elif color == "c":
        return "FF0000"
    elif color == "d":
        return "FF8000"
    elif color == "e":
        return "FFFF00"
    elif color == "f":
        return "7DFF00"
    elif color == "g":
        return "00FF00"
    elif color == "h":
        return "00FF7D"
    elif color == "i":
        return "00FFFF"
    elif color == "j":
        return "007DFF"
    elif color == "k":
        return "0000FF"
    elif color == "l":
        return "7D00FF"
    elif color == "m":
        return "FF00FF"
    elif color == "n":
        return "FF007D"


def handle_ultrasonic_color(command: str):
    global ultrasonic_sensors_colors
    if command[0:2] != 'UC':
        return

    key = command[2:]

    if key == '!':
        ultrasonic.clearultrasonicRGB()
        return

    if key == '*':
        ultrasonic.ultrasonicRGB1(ultrasonic_sensors_colors[0], ultrasonic_sensors_colors[1])
        return

    left_color = key[0:6]
    right_color = key[6:]
    ultrasonic_sensors_colors = (left_color, right_color)
    ultrasonic.ultrasonicRGB1(left_color, right_color)



def handle_color_ring(command: str):
    global color_ring_values

    if command[0] != 'C':
        return

    key = command[1:]

    if key == '!':
        ring.clearRGB()
        return

    if key == '*':
        ring.fillRGBRing(*color_ring_values)
        return

    if key[0] == '#':
        led_index = int(key[1:3])
        hex_color = key[3:9]
        color_ring_values[led_index] = hex_color
        ring.setRGBring(led_index, hex_color)
        return

    color1 = decode_color(key[0:1])
    color13 = decode_color(key[1:2])
    color2 = decode_color(key[2:3])
    color3 = decode_color(key[3:4])
    color4 = decode_color(key[4:5])
    color5 = decode_color(key[5:6])
    color6 = decode_color(key[6:7])
    color7 = decode_color(key[7:8])
    color8 = decode_color(key[8:9])
    color9 = decode_color(key[9:10])
    color10 = decode_color(key[10:11])
    color11 = decode_color(key[11:12])
    color12 = decode_color(key[12:13])
    color_ring_values = [color1, color2, color3, color4, color5,
        color6, color7, color8, color9, color10, color11,
        color12, color13]
    ring.fillRGBRing(*color_ring_values)


def handle_sound_emotes(command: str):
    if command[0] != 'E':
        return

    key = command[1:]
    buzzer.play_emoji(key)


def handle_dance_moves(command: str):
    if command[0] != 'W':
        return

    key = command[1:]
    if key == "d":
        motors_move(sliderR, 0, "forward", 0.2)
        motors_move(0, sliderL, "forward", 0.2)
        motors_move(sliderR, 0, "backward", 0.2)
        motors_move(0, sliderL, "backward", 0.2)
        return

    if key == "mwl":
        for _ in range(2):
            motors_move(sliderR, 0, "backward", 0.4)
            motors_move(0, sliderL, "backward", 0.4)
        return

    if key == "mwr":
        for _ in range(2):
            motors_move(sliderR, 0, "forward", 0.4)
            motors_move(0, sliderL, "forward", 0.4)
        return

    if key == "cl":
        motors_move(90, 90, "left", 0.3)
        motors_move(0, 90, "forward", 0.6)
        return

    if key == "cr":
        motors_move(90, 90, "right", 0.3)
        motors_move(90, 0, "forward", 0.6)
        return


def format_sensor_message(sensor, value):
    return f's:{sensor}:{value}'

def handle_sensors(command: str, ble_print):
    if command[0] != 'R':
        return


    global distance_sensor_enabled
    global line_sensors_enabled

    sensor = int(command[1:3])
    status = int(command[3])

    if sensor == 0:
        if status == 1 and not distance_sensor_enabled:
            period = float(command[4:])
            asyncio.create_task(start_ultrasonic_sensor(ble_print, period))
        else:
            distance_sensor_enabled = False
    elif sensor == 1:
        if status == 1 and not line_sensors_enabled:
            period = float(command[4:])
            asyncio.create_task(start_line_sensors(ble_print, period))
        else:
            line_sensors_enabled = False


async def start_line_sensors(ble_print, period: float):
    global line_sensors_enabled
    line_sensors_enabled = True

    while line_sensors_enabled:
        digital_left = line.detectLineLeft()
        digital_right = line.detectLineRight()
        analog_left = line.readLineLeft()
        analog_right = line.readLineRight()

        ble_print(format_sensor_message(1, digital_left))
        ble_print(format_sensor_message(2, digital_right))
        ble_print(format_sensor_message(3, analog_left))
        ble_print(format_sensor_message(4, analog_right))

        await asyncio.sleep(period)


async def start_ultrasonic_sensor(ble_print, period: float):
    global distance_sensor_enabled
    distance_sensor_enabled = True

    while distance_sensor_enabled:
        ultrasonic_value = ultrasonic.readultrasonicRGB(1)
        ble_print(format_sensor_message(0, ultrasonic_value))
        await asyncio.sleep(period)


def remote_control(key, ble_print):
    handle_sensors(key, ble_print)
    handle_movement(key)
    handle_tones(key)
    handle_joystick(key)
    handle_tools(key)
    handle_color_ring(key)
    handle_ultrasonic_color(key)
    handle_movement_settings(key)
    handle_sound_emotes(key)
    handle_dance_moves(key)
