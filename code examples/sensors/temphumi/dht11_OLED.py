import dht
from machine import Pin
from time import sleep
from ottodisplay import OttoOled

sensor = dht.DHT11(Pin(4)) # Connector 5
oled = OttoOled(19, 18) # Connector 1

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
    oled.writeTextDisplay('Humidity: %3.1f %%' %hum, 0, 20)
    oled.showDisplay()
  except OSError as e:
    print('Failed to read sensor.')
    