import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottomotor import Servo

adc_32 = ADC(32)
adc_32.width(ADC.WIDTH_10BIT)

servo_26 = Servo()
servo_26.attach(15)

servo_26.write(90)
time.sleep(1)
servo_26.write(120)
time.sleep(1)
servo_26.write(160)
time.sleep(1)
servo_26.write(180)
time.sleep(1)
servo_26.write(90)
time.sleep(1)
servo_26.write(60)
time.sleep(1)
servo_26.write(30)
time.sleep(1)
servo_26.write(0)
time.sleep(1)
def map(value, in_min, in_max, out_min, out_max):
   map = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   return map

while True:
    print(adc_32.read())
    time.sleep(0.05)
    servo_26.write(map(adc_32.read(), 0, 1023, 0, 180))