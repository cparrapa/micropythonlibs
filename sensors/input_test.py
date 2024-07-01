from machine import Pin, ADC ,PWM
from time import sleep

adc_0 = ADC(Pin(26))

analogL=ADC(Pin(32))        # Connector 6
analogR=ADC(Pin(33))        # Connector 7

digitalR = Pin(15, Pin.IN)  # Connector 9

while True:
    print(analogL.read_u16())
    print(analogR.read_u16())
    print(adc_0.read_u16())
    print(digitalR.value())
    sleep((1))