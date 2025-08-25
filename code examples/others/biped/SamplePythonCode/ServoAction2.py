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

def control_servo2(cmd):
    if cmd == 'Forward':
        global SS1, SS2, SS3, SS4, SS5, SS6, SS7, SS8
        InitPosition()
        for index20 in range(25):
            SS7 += 1
            servos.goToPosition(7, SS7)
            SS8 -= 1
            servos.goToPosition(8, SS8)
            utime.sleep_ms(15)
        # Right Foot Forward
        utime.sleep_ms(200)
        for index21 in range(36):
            SS6 -= 1
            servos.goToPosition(6, SS6)
            SS5 -= 0.5
            servos.goToPosition(5, SS5)
            utime.sleep_ms(15)
        for index22 in range(26):
            SS3 += 1
            servos.goToPosition(3, SS3)
            SS4 += 1
            servos.goToPosition(4, SS4)
            SS6 += 1
            servos.goToPosition(6, SS6)
            SS5 += 0.5
            servos.goToPosition(5, SS5)
            utime.sleep_ms(10)
        for index23 in range(10):
            SS6 += 1
            servos.goToPosition(6, SS6)
            SS5 += 0.5
            servos.goToPosition(5, SS5)
            utime.sleep_ms(10)
        for index24 in range(3):
            EasyWalk()
        # From here the left foot moves forward
        for index25 in range(36):
            SS5 += 1
            servos.goToPosition(5, SS5)
            SS6 += 0.5
            servos.goToPosition(6, SS6)
            utime.sleep_ms(10)
        for index26 in range(26):
            SS4 -= 1
            servos.goToPosition(4, SS4)
            SS3 -= 1
            servos.goToPosition(3, SS3)
            SS5 -= 1
            servos.goToPosition(5, SS5)
            SS6 -= 0.5
            servos.goToPosition(6, SS6)
            utime.sleep_ms(10)
        for index27 in range(10):
            SS5 -= 1
            servos.goToPosition(5, SS5)
            SS6 -= 0.5
            servos.goToPosition(6, SS6)
            utime.sleep_ms(10)
        for index28 in range(25):
            SS7 -= 1
            servos.goToPosition(7, SS7)
            SS8 += 1
            servos.goToPosition(8, SS8)
            utime.sleep_ms(15)
        InitPosition()

def EasyWalk():
    global SS1, SS2, SS3, SS4, SS5, SS6, SS7, SS8
    # From here the left foot moves forward
    for index29 in range(36):
        SS5 += 1
        servos.goToPosition(5, SS5)
        SS6 += 0.5
        servos.goToPosition(6, SS6)
        utime.sleep_ms(10)
    for index30 in range(26):
        SS4 -= 1
        servos.goToPosition(4, SS4)
        SS3 -= 1
        servos.goToPosition(3, SS3)
        utime.sleep_ms(10)
    for index31 in range(26):
        SS4 -= 1
        servos.goToPosition(4, SS4)
        SS3 -= 1
        servos.goToPosition(3, SS3)
        SS5 -= 1
        servos.goToPosition(5, SS5)
        SS6 -= 0.5
        servos.goToPosition(6, SS6)
        utime.sleep_ms(10)
    for index32 in range(10):
        SS5 -= 1
        servos.goToPosition(5, SS5)
        SS6 -= 0.5
        servos.goToPosition(6, SS6)
        utime.sleep_ms(10)
    # From here the right foot moves forward
    for index33 in range(36):
        SS6 -= 1
        servos.goToPosition(6, SS6)
        SS5 -= 0.5
        servos.goToPosition(5, SS5)
        utime.sleep_ms(10)
    for index34 in range(26):
        SS3 += 1
        servos.goToPosition(3, SS3)
        SS4 += 1
        servos.goToPosition(4, SS4)
        utime.sleep_ms(10)
    for index35 in range(26):
        SS4 += 1
        servos.goToPosition(4, SS4)
        SS3 += 1
        servos.goToPosition(3, SS3)
        SS6 += 1
        servos.goToPosition(6, SS6)
        SS5 += 0.5
        servos.goToPosition(5, SS5)
        utime.sleep_ms(10)
    for index36 in range(10):
        SS6 += 1
        servos.goToPosition(6, SS6)
        SS5 += 0.5
        servos.goToPosition(5, SS5)
        utime.sleep_ms(10)