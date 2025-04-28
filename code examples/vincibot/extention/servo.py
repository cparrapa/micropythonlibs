
import machine
import time
import system_state

version = 1.2

servo1 = machine.Pin(7, machine.Pin.OUT)
servo2 = machine.Pin(11, machine.Pin.OUT)
pwm1 = machine.PWM(servo1)
pwm2 = machine.PWM(servo2)
angle1 = 90
angle2 = 90

servo_init_flag_1 = False
servo_init_flag_2 = False

def get_version():
    return version

def _map_pwm(value, fromlow, fromhigh, tolow, tohigh):
    pwm_value = int((value - fromlow) * (tohigh - tolow) / (fromhigh - fromlow) + tolow)
    if pwm_value < tolow:
        pwm_value = tolow
    if pwm_value > tohigh:
        pwm_value = tohigh
    return pwm_value

# def init():
#     pass

def init(servo_num):
    global pwm1, pwm2, angle1, angle2, servo_init_flag_1, servo_init_flag_2
    if servo_num == 1 or servo_num == "1":
        pwm1.deinit()
        pwm1 = machine.PWM(servo1)
        pwm1.freq(50)
        pwm1.duty(_map_pwm(angle1,0,180,25,128))
        servo_init_flag_1 = True
    elif servo_num == 2 or servo_num == "2":
        pwm2.deinit()
        pwm2 = machine.PWM(servo2)
        pwm2.freq(50)
        pwm2.duty(_map_pwm(angle2,0,180,25,128))
        servo_init_flag_2 = True

def run(servo_num, angle):
    global servo_init_flag_1, servo_init_flag_2
    if(system_state.get_extention_flag(1) == False):
        servo_init_flag_1 = False
        servo_init_flag_2 = False
        init(servo_num)
        system_state.set_extention_flag(1,True)
    elif(servo_num == 1 and servo_init_flag_1 == False):
        init(1)
    elif(servo_num == 2 and servo_init_flag_2 == False):
        init(2)

    global pwm1, pwm2, angle1, angle2
    if servo_num == 1 or servo_num == "1":
        angle1 = angle
        pwm1.duty(_map_pwm(angle1,0,180,25,128))
    elif servo_num == 2 or servo_num == "2":
        angle2 = angle
        pwm2.duty(_map_pwm(angle2,0,180,25,128))