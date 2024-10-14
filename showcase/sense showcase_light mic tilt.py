import machine, time
from time import sleep
from machine import Pin, ADC, PWM
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor

# ---------------------------
# This code is meant to display Sense expansion with Microphone (9) and Light sensor (5), both on analog pins inside a Double universal top.
# There is also Tilt sensor (4) that triggers buzzing sound when rotated.
# ---------------------------

# Initialize components
offset = 0
led = Pin(2, Pin.OUT)  # Built-in LED
digital_pin_27 = Pin(27, Pin.IN)  # Tilt sensor
microphone = Pin(15, Pin.IN)
adc_33 = ADC(33)  # Light sensor
adc_33.width(ADC.WIDTH_10BIT)
buzzer = OttoBuzzer(25)
ultrasonic = OttoUltrasonic(18, 19)
motor = OttoMotor(13, 14)

# Variables
debounce = 500
debouncetilt = 200
lasttilt = 0
lastjump = 0
tilt_detected = False
jump_detected = False

# IRQ Handlers
def buzz_handler(pin):
    global tilt_detected, lasttilt
    nowtilt = time.ticks_ms()
    if time.ticks_diff(nowtilt, lasttilt) > debouncetilt:
        tilt_detected = True  # Set a flag
        lasttilt = nowtilt  # Update the last tilt timestamp

def jump_handler(pin):
    global jump_detected, lastjump
    now = time.ticks_ms()
    if time.ticks_diff(now, lastjump) > debounce:
        jump_detected = True  # Set a flag
        lastjump = now  # Update the last jump timestamp

# Attach IRQs
digital_pin_27.irq(trigger=Pin.IRQ_RISING, handler=buzz_handler)
microphone.irq(trigger=Pin.IRQ_RISING, handler=jump_handler)

# Main loop
while True:
    # Check for tilt and execute the action outside IRQ
    if tilt_detected:
        buzzer.playEmoji("S_JUMP")
        tilt_detected = False  # Reset flag

    # Check for jump and execute the action outside IRQ
    if jump_detected:
        motor.leftServo.freq(50)
        motor.rightServo.freq(50)
        motor.leftServo.duty(109 - offset)
        motor.rightServo.duty(43 + offset)
        sleep(0.01)
        motor.rightServo.duty(0)
        motor.leftServo.duty(0)
        jump_detected = False  # Reset flag

    # Other sensor readings
    light = 1023 - adc_33.read()
    mic = microphone.value()

    # Debugging output
    print("Light:", light, "Mic:", mic, "Tilt:", digital_pin_27.value())

    # Ultrasonic light reaction
    if light > 500:
        ultrasonic.ultrasonicRGB1("000000", "000000")
    else:
        ultrasonic.ultrasonicRGB1("33ccff", "33ccff")
    
    time.sleep(0.5)
