
from machine import ADC, Pin

version = 0.5

adc1=ADC(Pin(7,Pin.IN))
adc1.atten(ADC.ATTN_11DB)

def _map(val, min_in, max_in, min_out, max_out):
    if val >= max_in:
        return max_out
    if val <= min_in:
        return min_out
    delta_in = max_in - min_in
    delta_out = max_out - min_out
    return int( ((val - min_in)*delta_out) / delta_in + min_out)

def get_version():
    return version

def get_value():
    global adc1
    val = adc1.read()
    return _map(int(val), 0, 4095, 0, 100)