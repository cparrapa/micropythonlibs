import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor
offset = 0

led = Pin(2, Pin.OUT)                 # Built in LED
digital_pin_27 = Pin(27, Pin.IN) # Tilt
microphone = Pin(15, Pin.IN, Pin.OUT)
adc_33 = ADC(33) # Light 
adc_33.width(ADC.WIDTH_10BIT)
buzzer = OttoBuzzer(25) 
ultrasonic = OttoUltrasonic(18, 19)
motor = OttoMotor(13, 14)

coef = 500

tilt = digital_pin_27.value()
mic = microphone.value()
micx = float(mic**5)
light = 1023 - adc_33.read()

def buzz(pin):
    buzzer.playEmoji("S_JUMP")

def jump(pin):
    motor.leftServo.freq(50)
    motor.rightServo.freq(50)
    motor.leftServo.duty(109- offset)
    motor.rightServo.duty(43+ offset)
    sleep(0.01)
    motor.rightServo.duty(0)
    motor.leftServo.duty(0)

digital_pin_27.irq(trigger=Pin.IRQ_RISING, handler=buzz)
microphone.irq(trigger=Pin.IRQ_RISING, handler=jump)


while True:
    # Updating pins
    tilt = digital_pin_27.value() * 100
    light = 1023 - adc_33.read()
    
    # Mic detection
    mic = microphone.value()
    
    # Debug
    print("Light: ", light, "Mic: ", mic, "Tilt: ", tilt)
    
    # Ultrasonic light reaction
    if light > 500:
        ultrasonic.ultrasonicRGB1("000000", "000000")
    else:
        ultrasonic.ultrasonicRGB1("33ccff", "33ccff")
    
    time.sleep(.5)

