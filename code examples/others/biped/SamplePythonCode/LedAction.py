import utime
from machine import Pin

# LED definitions

led_Up=Pin(28,Pin.OUT)
led_Under=Pin(27,Pin.OUT)


# LED Action

def control_led(cmd):
    if cmd == 'on':
        led_Up.value(1)  
        led_Under.value(1)
        
    if cmd == 'blink':
        led_Up.value(1)
        utime.sleep(0.5)
        led_Up.value(0)
        utime.sleep(0.5)
        led_Up.value(1)
        utime.sleep(0.5)
        led_Up.value(0)
        utime.sleep(0.5)
        led_Under.value(1)
        utime.sleep(0.5)
        led_Under.value(0)
        utime.sleep(0.5)
        led_Under.value(1)
        utime.sleep(0.5)
        led_Under.value(0)

    if cmd == 'off':
        led_Up.value(0)  
        led_Under.value(0)
