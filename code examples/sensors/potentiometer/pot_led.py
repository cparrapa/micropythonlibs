from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from time import sleep                                 #importing sleep class

led=PWM(Pin(2), 5000)             #GPIO14 set as pin and 5000Hz as frequency

potentiometer=ADC(Pin(32))             #creating potentiometer object
potentiometer.width(ADC.WIDTH_12BIT)   #setting ADC resolution to 10 bit
potentiometer.atten(ADC.ATTN_11DB)         #3.3V full range of voltage

while True:
  potentiometer_value=potentiometer.read()           #reading analog pin
  print(potentiometer_value)
  led.duty(potentiometer_value)             #setting duty cycle value as that of the potentiometer value
  sleep(0.1)
