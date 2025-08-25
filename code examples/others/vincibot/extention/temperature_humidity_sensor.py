import sensor, time
from machine import Pin
import system_state
import math
# DHT11_CRC_ERROR = -2,
# DHT11_TIMEOUT_ERROR = -1

version = 0.8
# dht_sensor = dht.DHT11(Pin(7, Pin.OPEN_DRAIN))

last_temperature = 25
last_humidity = 55

def get_version():
    return version

def get_temperature(type = 'Celsius'):
    global last_temperature
    val = sensor.get_dht11_temperature(7)
    status = sensor.get_dht11_status(7)

    if val > 50:
        status = -4

    if status < 0:
        val = last_temperature
    else:
        last_temperature = val
    
    if type == 'Fahrenheit':
        val = round(32 + val*1.8)
    time.sleep(0.2)
    return val

def get_humidity():
    global last_humidity
    val = sensor.get_dht11_humidity(7)
    status = sensor.get_dht11_status(7)

    if val > 96:
        status = -3

    if status < 0:
        val = last_humidity
    else:
        last_humidity = val
    time.sleep(0.2)
    return val

def get_status():
    status = sensor.get_dht11_status(7)
    return status
