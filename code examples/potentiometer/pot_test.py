from machine import Pin, ADC, PWM        #importing Pin, ADC and PWM classes
from time import sleep                   #importing sleep class

led = Pin(2, Pin.OUT)
button = Pin(26, Pin.IN)    # Connector 4
analogL=ADC(Pin(32))        # Connector 6
analogR=ADC(Pin(33))        # Connector 7
digitalL = Pin(27, Pin.IN)  # Connector 8
digitalR = Pin(15, Pin.IN)  # Connector 9

while True:
    print("button:", button.value(), end = " ")
    print("Connector 6:",analogL.read_u16(), end = " ")
    print("Connector 7:",analogR.read_u16())
    analogL_value=analogL.read()           #reading analog pin
    analogR_value=analogR.read()           #reading analog pin
    print("Left analog sensor:",analogL_value,"Right analog sensor:",analogR_value)
    print("Left digital sensor:",digitalL.value(),"Right digital sensor:",digitalR.value())
    led.value(button.value())
    sleep(0.2)