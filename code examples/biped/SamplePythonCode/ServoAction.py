import utime
from SimplyServos import KitronikSimplyServos
servos = KitronikSimplyServos()
import Config
from machine import Pin

# LED definitions

led_Up=Pin(28,Pin.OUT)
led_Under=Pin(27,Pin.OUT)

# Servo Init Position

def InitPosition():
    servos.goToPosition(1,Config.S1)
    servos.goToPosition(2,Config.S2)
    servos.goToPosition(3,Config.S3)
    servos.goToPosition(4,Config.S4)
    servos.goToPosition(5,Config.S5)
    servos.goToPosition(6,Config.S6)
    servos.goToPosition(7,Config.S7)
    servos.goToPosition(8,Config.S8)


# Servo Action

SS1 = Config.S1
SS2 = Config.S2
SS3 = Config.S3
SS4 = Config.S4
SS5 = Config.S5
SS6 = Config.S6
SS7 = Config.S7
SS8 = Config.S8

def control_servo(cmd):
    if cmd == 'Exercise':
        global SS1, SS2, SS3, SS4, SS5, SS6, SS7, SS8
        InitPosition()
        # From Here Arm Motion
        for index1 in range(100):
            SS2 += 1
            servos.goToPosition(2,SS2)
            SS7 += 1
            servos.goToPosition(7,SS7)
            utime.sleep_ms(10)
        for index2 in range(100):
            SS1 -= 1
            servos.goToPosition(1,SS1)
            SS8 -= 1
            servos.goToPosition(8,SS8)
            utime.sleep_ms(10)
        for index3 in range(45):
            SS7 -= 1
            servos.goToPosition(7,SS7)
            SS8 += 1
            servos.goToPosition(8,SS8)
            utime.sleep_ms(10)
        for index4 in range(80):
            SS1 += 1
            servos.goToPosition(1,SS1)
            SS2 -= 1
            servos.goToPosition(2,SS2)
            utime.sleep_ms(10)
        # From here
        # Movement with both hands in different directions
        utime.sleep_ms(200)
        for index5 in range(45):
            SS1 += 1
            servos.goToPosition(1, SS1)
            SS2 += 1
            servos.goToPosition(2, SS2)
            utime.sleep_ms(10)
        for index6 in range(90):
            SS1 -= 1
            servos.goToPosition(1, SS1)
            SS2 -= 1
            servos.goToPosition(2, SS2)
            utime.sleep_ms(10)
        for index7 in range(45):
            SS1 += 1
            servos.goToPosition(1, SS1)
            SS2 += 1
            servos.goToPosition(2, SS2)
            utime.sleep_ms(10)
        for index8 in range(20):
            SS1 += 1
            servos.goToPosition(1, SS1)
            SS2 -= 1
            servos.goToPosition(2, SS2)
            utime.sleep_ms(10)
        # Balance With Both Hands
        led_Up.value(1)  
        led_Under.value(1)
        utime.sleep_ms(1000)
        for index9 in range(15):
            SS7 += 1
            servos.goToPosition(7, SS7)
            SS8 -= 1
            servos.goToPosition(8, SS8)
            utime.sleep_ms(10)
        # for Foot
        utime.sleep_ms(1000)
        for index10 in range(15):
            SS5 += 1
            servos.goToPosition(5, SS5)
            SS6 -= 1
            servos.goToPosition(6, SS6)
            utime.sleep_ms(15)
        utime.sleep_ms(1000)
        for index11 in range(15):
            SS5 -= 1
            servos.goToPosition(5, SS5)
            SS6 += 1
            servos.goToPosition(6, SS6)
            utime.sleep_ms(15)
        # for parallel
        utime.sleep_ms(1000)
        for index12 in range(30):
            SS3 -= 1
            servos.goToPosition(3, SS3)
            SS4 -= 1
            servos.goToPosition(4, SS4)
            utime.sleep_ms(15)
        utime.sleep_ms(1000)
        for index13 in range(30):
            SS5 -= 1
            servos.goToPosition(5, SS5)
            SS6 += 1
            servos.goToPosition(6, SS6)
            utime.sleep_ms(15)
        utime.sleep_ms(1000)
        for index14 in range(30):
            SS5 += 1
            servos.goToPosition(5, SS5)
            SS6 -= 1
            servos.goToPosition(6, SS6)
            utime.sleep_ms(15)
        utime.sleep_ms(1000)
        for index15 in range(60):
            SS3 += 1
            servos.goToPosition(3, SS3)
            SS4 += 1
            servos.goToPosition(4, SS4)
            SS7 -= 0.5
            servos.goToPosition(7, SS7)
            SS8 += 0.5
            servos.goToPosition(8, SS8)
            utime.sleep_ms(15)
        utime.sleep_ms(1000)
        for index16 in range(30):
            SS3 -= 1
            servos.goToPosition(3, SS3)
            SS4 -= 1
            servos.goToPosition(4, SS4)
            SS7 += 1
            servos.goToPosition(7, SS7)
            SS8 -= 1
            servos.goToPosition(8, SS8)
            utime.sleep_ms(15)
        # From Here Return Position
        for index19 in range(45):
            SS7 -= 1
            servos.goToPosition(7, SS7)
            SS8 += 1
            servos.goToPosition(8, SS8)
            utime.sleep_ms(10)
        for index21 in range(20):
            SS1 -= 1
            servos.goToPosition(1, SS1)
            SS2 += 1
            servos.goToPosition(2, SS2)
            utime.sleep_ms(10)
        InitPosition()
        led_Up.value(0)  
        led_Under.value(0)