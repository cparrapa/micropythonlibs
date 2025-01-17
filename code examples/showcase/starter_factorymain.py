#v02 DEMO all starter components without libraries 2025
import machine, utime
from time import sleep             #importing sleep class
from machine import Pin, ADC, PWM  #importing Pin, ADC and PWM classes
from neopixel import NeoPixel      #importing NeoPixel (RGB lights) class

ultrasonicRGB = NeoPixel(Pin(18), 6)       # Connector 1
brg = 0.8
numberleds = 13
ring = NeoPixel(Pin(4), numberleds) # Connector 5
leftServo = PWM(Pin(14))      # Connector 10
leftServo.freq(50)
rightServo = PWM(Pin(13))     # Connector 11
rightServo.freq(50)
led = Pin(2, Pin.OUT) #built in LED
buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512) #built in buzzer
analogL = ADC(Pin(32))          #Connector 6
analogR = ADC(Pin(33))          #Connector 7
digitalL = Pin(27, Pin.IN) #Connector 8
digitalR = Pin(15, Pin.IN) #Connector 9
delaytime = 0.05
led.off()

def red():
    global i, numberleds, delaytime
    for i in range(numberleds):
        ring[i] = (int(255 * brg), int(0 * brg), int(0 * brg))
        ring.write()
        sleep(delaytime)

def green():
    global i, numberleds, delaytime
    for i in range(numberleds):
        ring[i] = (int(0 * brg), int(0 * brg), int(255 * brg))
        ring.write()
        sleep(delaytime)

def blue():
    global i, numberleds, delaytime
    for i in range(numberleds):
        ring[i] = (int(0 * brg), int(255 * brg), int(0 * brg))
        ring.write()
        sleep(delaytime)

def white():
    global i, numberleds, delaytime
    for i in range(numberleds):
        ring[i] = (int(255 * brg), int(255 * brg), int(255 * brg))
        ring.write()
        sleep(delaytime)

def OttoNeo(index):
    global brg
    colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127)]
    color = colors[index % len(colors)]
    for i in range(13):
        ring[i] = (int(color[0] * brg), int(color[1] * brg), int(color[2] * brg))
    ring.write()

def measure_distance():
   io_pin = machine.Pin(19, machine.Pin.OUT)
   io_pin.off()
   utime.sleep_us(2)
   io_pin.on()
   utime.sleep_us(20)
   io_pin.off()
   io_pin = machine.Pin(19, machine.Pin.IN)
   pulse_duration = machine.time_pulse_us(io_pin, 1)
   distance = 0
   if ((pulse_duration < 60000) and (pulse_duration > 1)):
      distance = pulse_duration / 22.8;
   return distance

def redUS():
    global delaytime, i
    for i in range(6):
        ultrasonicRGB[i] = (int(255 * brg), int(0 * brg), int(0 * brg))
        ultrasonicRGB.write()
        sleep(delaytime)
        
def greenUS():
    global delaytime, i
    for i in range(6):
        ultrasonicRGB[i] = (int(0 * brg), int(255 * brg), int(0 * brg))
        ultrasonicRGB.write()
        sleep(delaytime)
        
def blueUS():
    global delaytime, i
    for i in range(6):
        ultrasonicRGB[i] = (int(0 * brg), int(0 * brg), int(255 * brg))
        ultrasonicRGB.write()
        sleep(delaytime)
        
ultrasonicRGB[0] = (0, 0, 255)
ultrasonicRGB[1] = (0, 0, 255)
ultrasonicRGB[2] = (0, 0, 255)
ultrasonicRGB[3] = (0, 0, 255)
ultrasonicRGB[4] = (0, 0, 255)
ultrasonicRGB[5] = (0, 0, 255)
ultrasonicRGB.write()
print("Otto is alive!")
led.on()
buzzer.duty(512)
buzzer.freq(261)
sleep(0.125)
buzzer.freq(293)
sleep(0.125)
buzzer.freq(329)
sleep(0.125)
buzzer.freq(349)
sleep(0.125)
buzzer.freq(392)
sleep(0.125)
buzzer.freq(440)
sleep(0.125)
buzzer.freq(493)
sleep(0.125)
buzzer.freq(523)
sleep(0.125)
buzzer.duty(0)
red()
redUS()
green()
greenUS()
blue()
blueUS()
white()
ring[0] = (int(255 * brg), int(1 * brg), int(1 * brg))
ring[1] = (int(255 * brg), int(128 * brg), int(0 * brg))
ring[2] = (int(255 * brg), int(255 * brg), int(0 * brg))
ring[3] = (int(128 * brg), int(255 * brg), int(0 * brg))
ring[4] = (int(0 * brg), int(255 * brg), int(0 * brg))
ring[5] = (int(0 * brg), int(255 * brg), int(128 * brg))
ring[6] = (int(0 * brg), int(255 * brg), int(255 * brg))
ring[7] = (int(0 * brg), int(128 * brg), int(255 * brg))
ring[8] = (int(0 * brg), int(0 * brg), int(255 * brg))
ring[9] = (int(127 * brg), int(0 * brg), int(255 * brg))
ring[10] = (int(255 * brg), int(0 * brg), int(255 * brg))
ring[11] = (int(255 * brg), int(0 * brg), int(127 * brg))
ring[12] = (int(255 * brg), int(255 * brg), int(255 * brg))
ring.write()
color_index = 1
rightServo.duty(115)
leftServo.duty(45)
sleep(1)
rightServo.duty(45)
leftServo.duty(115)
sleep(1)
rightServo.duty(0)
leftServo.duty(0)
rightServo.duty(45)
leftServo.duty(45)
sleep(0.4)
rightServo.duty(115)
leftServo.duty(115)
sleep(0.4)
rightServo.duty(0)
leftServo.duty(0)
color_index += 1
if color_index >= 12:
    color_index = 0
for color in range(11):
    OttoNeo(color)
    sleep(0.2)

while True:
    analogL_value=analogL.read()           #reading analog pin
    analogR_value=analogR.read()           #reading analog pin
    distance = measure_distance()
    print("Left analog:",analogL_value,"Right analog:",analogR_value)
    print("Left digital:",digitalL.value(),"Right digital:",digitalR.value())
    print("Ultrasonic distance:", distance, "cm")
    if (analogL_value) <= (800):
        led.on()
        ultrasonicRGB[0] = (0, 0, 255)
        ultrasonicRGB[1] = (0, 0, 255)
        ultrasonicRGB[2] = (0, 0, 255)
        ultrasonicRGB.write()
    elif (analogR_value) <= (800):
        led.on()
        ultrasonicRGB[3] = (0, 0, 255)
        ultrasonicRGB[4] = (0, 0, 255)
        ultrasonicRGB[5] = (0, 0, 255)
        ultrasonicRGB.write()
    else:
        led.off()
        for leds in range(6):
            ultrasonicRGB[leds] = (255, 255, 0)
        ultrasonicRGB.write()
    if (distance) < (3):
        OttoNeo(1)
    elif (distance) < (7):
        OttoNeo(2)
    elif (distance) < (10):
        OttoNeo(3)
    elif (distance) < (14):
        OttoNeo(4)
    else:
        OttoNeo(5)
    sleep(0.1)
