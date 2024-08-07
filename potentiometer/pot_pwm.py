from machine import ADC, Pin, PWM
from utime import sleep

# Pins Used
BUILT_IN_LED_PIN = 2
POT_PIN = 32

pot = ADC(POT_PIN)

builtin_pwm = PWM(Pin(BUILT_IN_LED_PIN))
builtin_pwm.freq(1000) # 1K Hz

POLL_DELAY = .1 # poll the pot after this delay in seconds

# repeat forever
while True:
    pot_value = pot.read_u16() # read the value from the pot
    print("pot value:", pot_value)
    builtin_pwm.duty_u16(pot_value)
    sleep(POLL_DELAY)