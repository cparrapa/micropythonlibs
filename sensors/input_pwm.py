from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from time import sleep                   #importing sleep class
import time

def map(x, in_min, in_max, out_min, out_max):
    """ return linear interpolation like map() fonction in Arduino"""
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

if __name__ == "__main__":

    # Create a PWM object linked to pin 23
    pwm_led = PWM(Pin(2,mode=Pin.OUT))
    pwm_led.freq(1_000)
    #led=PWM(Pin(2), 5000)

    # Create an ADC object linked to pin 36
    adc = ADC(Pin(26, mode=Pin.IN)) #Connector 4
    #pot = ADC(Pin(26))             #creating potentiometer object
    adc.atten(ADC.ATTN_11DB)    
    #ADC.ATTN_0DB — the full range voltage: 1.2V
    #ADC.ATTN_2_5DB — the full range voltage: 1.5V
    #ADC.ATTN_6DB — the full range voltage: 2.0V
    #ADC.ATTN_11DB — defalult full range voltage: 3.3V
    
    #ADC.width(ADC.WIDTH_12BIT)
    #ADC.WIDTH_9BIT: range 0 to 511
    #ADC.WIDTH_10BIT: range 0 to 1023
    #ADC.WIDTH_11BIT: range 0 to 2047
    #ADC.WIDTH_12BIT: range 0 to 4095

    while True:
        val = adc.read()
        pwm_value = map(x=val, in_min=0, in_max=4095, out_min=0,out_max=1023)
        pwm_led.duty(pwm_value)
        sleep_ms(10)
        sleep(0.01)
        print(val)
        #potentiometer_value=int(adc.read()/4)           #reading analog pin
        #pwm_led.duty(potentiometer_value)             #setting duty cycle’s value as that of the potentiometer value
