from machine import Pin, ADC
from time import sleep_ms

LDR = ADC(Pin(33, Pin.IN)) # Connector 7
LDR.atten(ADC.ATTN_11DB)

led = Pin(2, Pin.OUT)
isAlert = False

while True:
    
    if LDR.read() < 1200:
        isAlert = True
        print(LDR.read())
    else:
        isAlert = False
        
    if isAlert:
        led.value(not led.value())
        sleep_ms(100)
    