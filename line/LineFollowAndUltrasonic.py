import utime
import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor


def measure_distance():
   io_pin = Pin(io, Pin.OUT)
   io_pin.off()
   utime.sleep_us(2)
   io_pin.on()
   utime.sleep_us(20)
   io_pin.off()
   io_pin = Pin(io, Pin.IN)
   pulse_duration = machine.time_pulse_us(io_pin, 1)
   distance = 0
   if ((pulse_duration < 60000) and (pulse_duration > 1)):
      distance = pulse_duration / 58.00;

   return distance

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ultrasonic = NeoPixel(Pin(18), 6)     # Connector 1
io = 19                               # echo input and trigger out signal
bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
analogL=ADC(Pin(32))                  # Connector 6
analogR=ADC(Pin(33))                  # Connector 7
digitalL = Pin(27, Pin.IN)            # Connector 8
digitalR = Pin(15, Pin.IN)            # Connector 9
motor = OttoMotor(13, 14)             # Connectors 10 & 11
offsetL = 0                           # Calibration for left servo motor
offsetR = 0                           # Calibration for right servo motor

def detect():
    while (measure_distance()) < (10):
        print("Detect!")
        motor.Stop(1)


while True:
    detect()
    print("Left sensor value:")
    print(analogL.read())
    print("Right sensor value:")
    print(analogR.read())
    if (analogL.read()) > (800):
        ultrasonic[0] = int(254 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[1] = int(254 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[2] = int(254 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[3] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[4] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[5] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic.write()
        motor.leftServo.duty(60+ offsetL)
        motor.rightServo.duty(60- offsetR)
    elif (analogR.read()) > (800):
        ultrasonic[0] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[1] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[2] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[3] = int(254 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[4] = int(254 * bright), int(0 * bright), int(0 * bright)
        ultrasonic[5] = int(254 * bright), int(0 * bright), int(0 * bright)
        ultrasonic.write()
        motor.leftServo.duty(95+ offsetL)
        motor.rightServo.duty(95- offsetR)
    else:
        ultrasonic[0] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[1] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[2] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[3] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[4] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic[5] = int(0 * bright), int(255 * bright), int(0 * bright)
        ultrasonic.write()
        motor.leftServo.duty(95+ offsetL)
        motor.rightServo.duty(60- offsetR)

