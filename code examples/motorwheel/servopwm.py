import machine, time, math                 #importing machine, time and math libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from ottomotor import Servo, OttoMotor

potA = ADC(Pin(32, mode=Pin.IN)) # Create an ADC object linked to Connector 6
potA.width(ADC.WIDTH_12BIT)
potA.atten(ADC.ATTN_11DB)

potB = ADC(33)
potB.width(ADC.WIDTH_12BIT)
potB.atten(ADC.ATTN_11DB)
  
#ADC.ATTN_0DB — the full range voltage: 1.2V
#ADC.ATTN_2_5DB — the full range voltage: 1.5V
#ADC.ATTN_6DB — the full range voltage: 2.0V
#ADC.ATTN_11DB — defalult full range voltage: 3.3V
#ADC.width(ADC.WIDTH_12BIT)
#ADC.WIDTH_9BIT: range 0 to 511
#ADC.WIDTH_10BIT: range 0 to 1023
#ADC.WIDTH_11BIT: range 0 to 2047
#ADC.WIDTH_12BIT: range 0 to 4095

servoA = PWM(Pin(14), freq=50, duty=77)
servoA.duty(90)
servoB=Servo()
servoB.attach(13)

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

if __name__ == "__main__":
    led = PWM(Pin(2,mode=Pin.OUT))  #led=PWM(Pin(2), 5000)
    led.freq(1_000)

    while True:
        val = potA.read()
        sleep(0.01)
        pwm_value = map(val, 0, 4095, 0,1023)
        led.duty(pwm_value)
        motorA = map(val, 0, 4095, 15,139)
        motorB = map(potB.read(), 0, 4095, 0,180)
        print("potA:",val,"potB:",potB.read(),"motA:",motorA,"motB:",motorB)
        time.sleep_ms(10)
        servoB.write(motorB)
        servoA.duty(motorA)