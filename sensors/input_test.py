import machine, time
from time import sleep
from machine import Pin, ADC ,PWM

pin_led = Pin(2, Pin.OUT)
analog_pinL = ADC(Pin(32))
analog_pinR = ADC(Pin(33))
adc_0 = ADC(Pin(26))
digital_pin_27 = Pin(27, Pin.IN)

for count in range((10)):
    print(analog_pinL.read_u16())
    print(analog_pinR.read_u16())
    print(adc_0.read_u16())
    print(digital_pin_27.value())
    time.sleep((1))