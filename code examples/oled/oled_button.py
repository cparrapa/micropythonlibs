from ottooled import OttoOled
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

oled = OttoOled(19, 18)  # Connector 1
button = Pin(26, Pin.IN) # Connector 4

i = 1
while True:
    print(i)
    if i == (1):
        oled.Eyes1Draw()
        oled.Mouth1Draw()
        oled.showDisplay()
    elif i == (2):
        oled.Eyes2Draw()
        oled.Mouth2Draw()
        oled.showDisplay()
    elif i == (3):
        oled.Eyes3Draw()
        oled.Mouth3Draw()
        oled.showDisplay()
    elif i == (4):
        oled.Eyes4Draw()
        oled.Mouth4Draw()
        oled.showDisplay()
    elif i == (5):
        oled.Eyes5Draw()
        oled.Mouth5Draw()
        oled.showDisplay()
    else:
        oled.Eyes6Draw()
        oled.Mouth6Draw()
        oled.showDisplay()
    if i > (6):
        i = 1
        oled.clearDisplay()
    if (button.value()) == (1):
        i += 1
        oled.clearDisplay()
