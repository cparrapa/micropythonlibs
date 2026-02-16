from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
import dht

sensor = dht.DHT11(Pin(4)) # Connector 5

while True:
    #Debugging
    print("Measuring...")
    sensor.measure()
    print("Done.")
    temp = sensor.temperature()
    hum = sensor.humidity()
    print(temp, hum)
    sleep(1)