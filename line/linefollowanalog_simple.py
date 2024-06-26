import machine, time
from time import sleep
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

digitalL = Pin(27, Pin.IN)
digitalR = Pin(15, Pin.IN)
analogL=ADC(Pin(32))           #creating potentiometer object
analogR=ADC(Pin(33))           #creating potentiometer object
leftServo = PWM(Pin(14))
leftServo.freq(50)
rightServo = PWM(Pin(13))
rightServo.freq(50)

while True:
    print("Left sensor:",digital_L.value(),"Right sensor:",digital_R.value())
    print("Left analog sensor:",analog_L.read() ,"Right analog sensor:",analog_R.read())
    if (analog_L.read() ) >= (900):
        leftServo.duty(60)
        rightServo.duty(60)
    elif (analog_R.read() ) >= (900):
        leftServo.duty(100)
        rightServo.duty(100)
    else:
        leftServo.duty(100)
        rightServo.duty(60)




