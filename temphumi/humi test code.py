import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
import dht
import time

sensor = dht.DHT11(Pin(27))

while True:
    #Debugging
    print("Measuring...")
    sensor.measure()
    print("Done.")
    temp = sensor.temperature()
    hum = sensor.humidity()
    print(temp, hum)
    time.sleep(1)l