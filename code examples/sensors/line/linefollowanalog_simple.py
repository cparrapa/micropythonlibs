from time import sleep
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

analogL=ADC(Pin(32))                  # Connector 6
analogR=ADC(Pin(33))                  # Connector 7
digitalL = Pin(27, Pin.IN)            # Connector 8
digitalR = Pin(15, Pin.IN)            # Connector 9

leftServo = PWM(Pin(14))
leftServo.freq(50)

rightServo = PWM(Pin(13))
rightServo.freq(50)

while True:
    print("Left sensor:",digitalL.value(),"Right sensor:",digitalR.value())
    print("Left analog sensor:",analogL.read() ,"Right analog sensor:",analogR.read())
    if (analogL.read() ) >= (900):
        leftServo.duty(60)
        rightServo.duty(60)
    elif (analogR.read() ) >= (900):
        leftServo.duty(100)
        rightServo.duty(100)
    else:
        leftServo.duty(100)
        rightServo.duty(60)




