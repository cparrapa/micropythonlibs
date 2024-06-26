from time import sleep
from machine import Pin
from neopixel import NeoPixel
import machine, utime

trigecho=19 # Conenctor 1
ultrasonic = NeoPixel(Pin(18), 6)

def measure_distance():
   io_pin = machine.Pin(trigecho, machine.Pin.OUT)
   io_pin.off()
   utime.sleep_us(2)
   io_pin.on()
   utime.sleep_us(20)
   io_pin.off()
   io_pin = machine.Pin(trigecho, machine.Pin.IN)
   pulse_duration = machine.time_pulse_us(io_pin, 1)
   distance = 0
   if ((pulse_duration < 60000) and (pulse_duration > 1)):
      distance = pulse_duration / 45.6;
   return distance

ultrasonic[0] = (0, 0, 255)
ultrasonic[1] = (0, 0, 255)
ultrasonic[2] = (0, 0, 255)
ultrasonic[3] = (255, 0, 0)
ultrasonic[4] = (255, 0, 0)
ultrasonic[5] = (255, 0, 0)
ultrasonic.write()
print(measure_distance())
