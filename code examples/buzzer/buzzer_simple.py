from time import sleep
from machine import Pin, PWM

buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512) #built in buzzer
duration= 0.125  #quarter:0.25 half:0.5 whole:1

buzzer.duty(512)
buzzer.freq(261) #c - Do
sleep(duration)
buzzer.freq(293) #d - Re
sleep(duration)
buzzer.freq(329) #e - Mi
sleep(duration)
buzzer.freq(349) #f - Fa
sleep(duration)
buzzer.freq(392) #g - Sol
sleep(duration)
buzzer.freq(440) #a - La
sleep(duration)
buzzer.freq(493) #b - Si
sleep(duration)
buzzer.freq(523) #C - Do
sleep(duration)
buzzer.duty(0)
