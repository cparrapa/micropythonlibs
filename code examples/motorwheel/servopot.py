from machine import Pin, ADC, PWM
from time import sleep

# CONFIG -------------------------
SERVO_PIN = 14        # change to your pin
FREQ = 50             # 50 Hz = standard servo frequency
MIN_US = 500         # pulse for -100% (full reverse)
MID_US = 1500         # pulse for 0% (stop)
MAX_US = 2500         # pulse for +100% (full forward)
# --------------------------------

pwm = PWM(Pin(SERVO_PIN), freq=FREQ)
pot = ADC(Pin(32, mode=Pin.IN)) # Create an ADC object linked to Connector 6
pot.width(ADC.WIDTH_12BIT)
pot.atten(ADC.ATTN_11DB)

def set_servo_speed(percent):
    """
    percent: -100 (full anticlockwise) ... 0 (stop) ... +100 (full clockwise)
    """
    if percent < -100: percent = -100
    if percent > 100:  percent = 100

    # convert percent → pulse width in microseconds
    if percent == 0:
        pulse_us = MID_US
    elif percent > 0:
        pulse_us = MID_US + (MAX_US - MID_US) * (percent / 100)
    else:
        pulse_us = MID_US - (MID_US - MIN_US) * (abs(percent) / 100)

    # convert microseconds → duty for ESP32 PWM
    duty = int((pulse_us / 20000) * 1023)  # 20ms period, 10-bit duty
    pwm.duty(duty)
    return pulse_us

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    val = pot.read()
    sleep(0.01)
    speed=map(val, 0, 4095, -100,100)
    set_servo_speed(speed)
    print("Raw: %3d" % val )
    print("Speed: %3d%%" % speed)
    
