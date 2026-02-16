import time
from ottosensors import Percentage

lightsensor = Percentage(7) # connector 7

while True:
    lightPercent = lightsensor.Read()
    
    print(lightPercent, "%")
    time.sleep_ms(100)
