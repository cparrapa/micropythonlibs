import time
from ottolight import LightSensor


lightsensor = LightSensor(5) # connector 5


while True:
    lightPercent = lightsensor.Read()
    
    print(lightPercent, "%")
    time.sleep_ms(100)
