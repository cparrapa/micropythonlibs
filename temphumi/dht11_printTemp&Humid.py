from machine import Pin
from time import sleep
import dht

sensor1 = dht.DHT11(Pin(16))
sensor2 = dht.DHT11(Pin(26))
sensor3 = dht.DHT11(Pin(15))
sensor4 = dht.DHT11(Pin(27))

while True:
    sleep(1)
    sensor1.measure()
    print("temperature1:", sensor1.temperature(), "humidity1:", sensor1.humidity())
    sensor2.measure()
    print("temperature2:", sensor2.temperature(), end = " ")
    print("humidity2:",sensor2.humidity())
    sensor3.measure()
    print("temperature3:", sensor3.temperature(), "humidity3:", sensor3.humidity())
    sensor4.measure()
    print("temperature4:", sensor4.temperature(), "humidity4:", sensor4.humidity())
