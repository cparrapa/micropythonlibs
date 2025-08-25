
import machine
import time
import system_state

version = 1.1

dc_ina = machine.Pin(7, machine.Pin.OUT)
dc_inb = machine.Pin(11, machine.Pin.OUT)
pwm1 = machine.PWM(dc_ina)
pwm2 = machine.PWM(dc_inb)

def _map(value, fromlow, fromhigh, tolow, tohigh):
    return int((value - fromlow) * (tohigh - tolow) / (fromhigh - fromlow) + tolow)

def get_version():
    return version

# def init():
#     pass

def init():
    global pwm1, pwm2
    pwm1.deinit()
    pwm2.deinit()
    pwm1 = machine.PWM(dc_ina)
    pwm2 = machine.PWM(dc_inb)
    pwm1.freq(20000)
    pwm2.freq(20000)
    pwm1.duty(_map(100,0,100,0,1023))
    pwm2.duty(_map(100,0,100,0,1023))

def run(speed):
    global pwm1, pwm2
    if(system_state.get_extention_flag(3) == False):
        init()
        system_state.set_extention_flag(3,True)
        
    if speed < -100:
        speed = -100
    elif speed > 100:
        speed = 100
    if speed > 0:
        pwm1.duty(_map(speed,0,100,0,1023))
        pwm2.duty(_map(0,0,100,0,1023))
    elif speed < 0:
        pwm1.duty(_map(0,0,100,0,1023))
        pwm2.duty(_map(-speed,0,100,0,1023))
    else:
        pwm1.duty(0)
        pwm2.duty(0)
        # pwm1.duty(_map(100,0,100,0,1023))
        # pwm2.duty(_map(100,0,100,0,1023))
    