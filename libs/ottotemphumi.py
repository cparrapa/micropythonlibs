# ottotemphumi v01 11.03.2024
import machine, time
from machine import Pin
import dht

class DHT:

    def __init__(self, pin, type_sensor):
        
       if(type_sensor == "DHT11"):
         self.d = dht.DHT11(Pin(pin))
       else :
         self.d = dht.DHT22(Pin(pin))
         
    def temperature(self):
        try:
            self.d.measure()
            temp=self.d.temperature()
            return (temp)
        except OSError as e:
            print('Failed to read temp sensor.')
            return "0"
        
    def humidity(self):
        try:
            self.d.measure()
            hum=self.d.humidity()
            return (hum)
        except OSError as e:
            print('Failed to read temp sensor.')
            return "0"