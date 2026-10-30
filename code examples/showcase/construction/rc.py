import asyncio
import gc
import json
import os
import random
from time import sleep, sleep_ms

import uhashlib
import util
from machine import ADC, Pin
from machine import reset as machine_reset
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
from ottoneopixel import OttoNeoPixel, OttoUltrasonic
from ottosensors import FollowLine

#Otto Construction additions: Timer Servo
from machine import Timer
from ottomotor import Servo

led = Pin(2, Pin.OUT)  # Built in LED
buzzer = OttoBuzzer(25)  # Built in Buzzer
ultrasonic = OttoUltrasonic(18, 19)  # Connector 1
analog = Pin(26, Pin.IN)  # Connector 4
n = 13  # Number of LEDs in ring
ring = OttoNeoPixel(4, n)  # Connector 5
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
matrix = ""

# Sensor values
active_mode = 0
distance_sensor_enabled = False
line_sensors_enabled = False

# Color ring memory
color_ring_values = ["000000" for x in range(13)]
ultrasonic_sensors_colors = ("000000", "000000")


#****************************** Otto Construction additions **********************************
#Arm and gripper
servo_arm=Servo()
servo_arm.attach(26)                   # Connector 4  lifting arm
servo_grip=Servo()
servo_grip.attach(27)                   # Connector 8  gripper
#servo starting positions
servo_arm.write(90)
servo_grip.write(90)

arm_increment = 0
arm_desired = 90
ARM_MIN = const(50)     #Adjust for your Otto  this is the angle for fully raised arms
ARM_MAX = const(120)	#Adjust for your Otto  this is the angle for fully lowered arms

grip_increment = 0
grip_desired = 90
GRIP_MIN = const(60)     #Adjust for your Otto  this is the angle for fully open gripper
GRIP_MAX = const(133)	#Adjust for your Otto  this is the angle for fully closed gripper


def tick(timer):   # we will receive the timer object when being called
    global arm_increment, arm_desired,grip_increment,grip_desired
    if (arm_increment != 0):
        arm_desired += arm_increment
        if arm_desired < ARM_MIN:
            arm_desired = ARM_MIN
        if arm_desired > ARM_MAX:
            arm_desired = ARM_MAX
        print("Arm angle: ",arm_desired)
        servo_arm.write(arm_desired)
    if (grip_increment != 0):
        grip_desired += grip_increment
        if grip_desired < GRIP_MIN:
            grip_desired = GRIP_MIN
        if grip_desired > GRIP_MAX:
            grip_desired = GRIP_MAX
        print("Grip angle: ", grip_desired)
        servo_grip.write(grip_desired)                
                    
timer3 = Timer(3)  # create a timer object using timer 3  to move the arm and the gripper
timer3.init(period=40, mode=Timer.PERIODIC, callback=tick)    
#**************************************************************************************

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
#Otto Construction additions: global
    global arm_increment, grip_increment
    key = command[1:]
    if key == "f":
        motors_move(sliderR, sliderL, "forward", 1)
    elif key == "b":
        motors_move(sliderR, sliderL, "backward", 1)
    elif key == "l":
        motors_move(sliderR, sliderL, "left", 1)
    elif key == "r":
        motors_move(sliderR, sliderL, "right", 1)
#this section replaced for COnstruction Otto        
#    elif key == "fn":
#        motors_move(sliderR, sliderL, "forward")
#    elif key == "bn":
#        motors_move(sliderR, sliderL, "backward")
#    elif key == "ln":
#        motors_move(sliderR, sliderL, "left")
#    elif key == "rn":
#        motors_move(sliderR, sliderL, "right")
#    elif key == "X":
#        motor.Stop(1)
    elif key == "fn":
        print("Raise arm")
        arm_increment = -1
    elif key == "bn":
        print("Lower arm")
        arm_increment = 1
    elif key == "ln":
        print("Open grip")
        grip_increment = -1
    elif key == "rn":
        print("Close grip")
        grip_increment = 1
    elif key == "X":
        arm_increment = 0
        grip_increment = 0
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
    if command[1] == ":":
        freq = float(command[2:])
        buzzer.tone_on(freq)
        return

    if key == "do":
        buzzer.tone_on(buzzer.NOTE_C4)
    elif key == "re":
        buzzer.tone_on(buzzer.NOTE_D4)
    elif key == "mi":
        buzzer.tone_on(buzzer.NOTE_E4)
    elif key == "fa":
        buzzer.tone_on(buzzer.NOTE_F4)
    elif key == "sol":
        buzzer.tone_on(buzzer.NOTE_G4)
    elif key == "la":
        buzzer.tone_on(buzzer.NOTE_A4)
    elif key == "si":
        buzzer.tone_on(buzzer.NOTE_B4)
    elif key == "edo":
        buzzer.tone_on(buzzer.NOTE_C5)
    elif key == "off":
        buzzer.tone_off()


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

    if speed == 0:
        motor.Stop(1)
        return


    handle_joystick_motor_values(deg, speed)

def handle_tools(command: str, exec_running: bool, ble_print):
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
    elif key == 'blcklrst':
        buzzer.clear_buzzer()
        ring.clearRGB()
        ultrasonic.clearultrasonicRGB()

        if exec_running:
            ble_print("r:t") # as in restarting - true
            sleep_ms(10)
            machine_reset()
        else:
            ble_print("r:f") # as in restarting - false
    elif "sex" in key: # as in Set EXtension ;)
        # Command looks like Tsex:sense, Tsex:interact, ...
        extension = key.split(':')[1]
        available_extensions = [util.EXTENSION_SENSE, util.EXTENSION_INTERACT, util.EXTENSION_INVENT, util.EXTENSION_EMOTE]

        if extension in available_extensions:
            util.set_nvs_value(util.EXTENSION_NVS_KEY, extension)
    elif "gn": # As in get name
        otto_ble_name = util.get_ble_name()
        ble_print(f"n:{otto_ble_name}")


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

def handle_library_tools(command: str, ble_print):
    if command[0] != 'L':
        return

    key = command[1:]
    if key == "L":
        asyncio.create_task(transmit_library_versions(ble_print))


async def transmit_library_versions(ble_print):
    try:
        with open("lock.json", "r") as f:
            libraries = json.load(f)["libraries"]

        for library in libraries:
            gc.collect()
            lib_info = libraries[library]

            # Frozen libraries can't be read or tampered with
            if lib_info.get("frozen", False):
                tampered_with = False
            else:
                # Filesystem library - verify checksum
                try:
                    with open(library, "rb") as f:
                        content = f.read()
                        sha256 = uhashlib.sha256()
                        sha256.update(content)
                        checksum = sha256.digest()
                        checksum_hex = ''.join('{:02x}'.format(b) for b in checksum)
                        tampered_with = checksum_hex != lib_info["digest"]
                except OSError:
                    # File missing from filesystem
                    tampered_with = True

            await asyncio.sleep(0)
            ble_print(format_library_version_message(library, lib_info["version"], tampered_with))
    except Exception as e:
        ble_print(e)

    await asyncio.sleep(0)

    # Get installed extension from NVS or return default
    nvs_extension = util.get_nvs_value(util.EXTENSION_NVS_KEY)
    extension = util.EXTENSION_NONE

    if nvs_extension:
        extension = nvs_extension

    ble_print(f"e:{extension}")

    ble_print("l:finito")


def format_library_version_message(library: str, version: str, tampered: bool) -> str:
    return f'l:{library}:{version}:{'true' if tampered else 'false'}'

def format_sensor_message(sensor, value):
    return f's:{sensor}:{value}'


def handle_modes(command: str):
    if command[0] != 'X':
        return

    global active_mode
    mode = int(command[1])

    if mode == 0:
        active_mode = 0
    elif mode == 1 and active_mode != 1:
        asyncio.create_task(start_mode_1())
    elif mode == 2 and active_mode != 2:
        asyncio.create_task(start_mode_2())
    elif mode == 3 and active_mode != 3:
        asyncio.create_task(start_mode_3())


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

async def start_mode_1():
    global active_mode
    active_mode = 1

    while active_mode == 1:
        distance = ultrasonic.readultrasonicRGB(1)

        if distance <= 10:
            ultrasonic.ultrasonicRGB1("ff0000", "ff0000")
            buzzer.tone(buzzer.NOTE_C5, 100, 100)
        elif distance < 20:
            ultrasonic.ultrasonicRGB1("ff6666", "ff6666")
            buzzer.tone(buzzer.NOTE_B4, 100, 100)
        elif  distance < 30:
            ultrasonic.ultrasonicRGB1("ff9966", "ff9966")
            buzzer.tone(buzzer.NOTE_A4, 100, 100)
        elif distance < 40:
            ultrasonic.ultrasonicRGB1("ffff66", "ffff66")
            buzzer.tone(buzzer.NOTE_G4, 100, 100)
        elif distance < 50:
            ultrasonic.ultrasonicRGB1("ffff33", "ffff33")
            buzzer.tone(buzzer.NOTE_F4, 100, 100)
        elif distance < 60:
            ultrasonic.ultrasonicRGB1("66ff99", "66ff99")
            buzzer.tone(buzzer.NOTE_E4, 100, 100)
        elif distance < 70:
            ultrasonic.ultrasonicRGB1("33ffff", "33ffff")
            buzzer.tone(buzzer.NOTE_D4, 100, 100)
        elif distance < 80:
            ultrasonic.ultrasonicRGB1("66ffff", "66ffff")
            buzzer.tone(buzzer.NOTE_C4, 100, 100)
        elif distance < 90:
            ultrasonic.ultrasonicRGB1("9999ff", "9999ff")
            buzzer.tone(buzzer.NOTE_A3, 100, 100)
        else:
            ultrasonic.ultrasonicRGB1("000000", "000000")

        await asyncio.sleep_ms(100)
    else:
        ultrasonic.ultrasonicRGB1("000000", "000000")


async def start_mode_2():
    global active_mode
    active_mode = 2

    while active_mode == 2:
        if (ultrasonic.readultrasonicRGB(1)) <= (15):
            ultrasonic.ultrasonicRGB1("cc0000", "cc0000")
            ring.fillAllRGBRing("cc0000")
            motor.Stop(1)
            await asyncio.sleep_ms(100)

            if (random.randint(1, 2)) == (1):
                motors_move(sliderR, sliderL, "right", 0.5)
            else:
                motors_move(sliderR, sliderL, "left", 0.5)
        else:
            ultrasonic.ultrasonicRGB1("ffffff", "ffffff")
            ring.fillAllRGBRing("ffffff")
            motors_move(sliderR, sliderL, "forward")

        await asyncio.sleep_ms(100)
    else:
        ultrasonic.ultrasonicRGB1("000000", "000000")
        ring.fillAllRGBRing("000000b  ")
        motor.Stop(1)


async def start_mode_3():
    global active_mode
    active_mode = 3

    while active_mode == 3:
        sensorL_value = line.readLineLeft()
        sensorR_value = line.readLineRight()
        print(sensorL_value, sensorR_value)
        if (sensorR_value) < (1400):
            print("L")
            motors_move(15, 15, "left")
        elif (sensorL_value) < (1400):
            print("R")
            motors_move(15, 15, "right")
        else:
            motors_move(sliderR, sliderL, "forward")
            print("F")

        await asyncio.sleep_ms(40)
    else:
        motor.Stop(1)

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


def remote_control(key, ble_print, exec_running: bool = False):
    handle_sensors(key, ble_print)
    handle_library_tools(key, ble_print)
    handle_movement(key)
    handle_tones(key)
    handle_joystick(key)
    handle_tools(key, exec_running, ble_print)
    handle_color_ring(key)
    handle_ultrasonic_color(key)
    handle_movement_settings(key)
    handle_sound_emotes(key)
    handle_dance_moves(key)
    handle_modes(key)
