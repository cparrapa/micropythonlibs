from machine import Pin
from time import sleep
import dht 

sensor = dht.DHT11(Pin(26)) #blue one
#sensor = dht.DHT22(Pin(26)) #white one
from ottooled import OttoOled
oled = OttoOled(21, 22)


while True:
  try:
    sleep(2)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    temp_f = temp * (9/5) + 32.0
    print('Temperature: %3.1f C' %temp)
    print('Temperature: %3.1f F' %temp_f)
    print('Humidity: %3.1f %%' %hum)
    oled.clearDisplay()
    oled.writeTextDisplay('Temp: %3.1f C' %temp, 0, 0)
    oled.showDisplay()
  except OSError as e:
    print('Failed to read sensor.')
    