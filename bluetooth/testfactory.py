from time import sleep             #importing sleep class
from machine import Pin, ADC, PWM  #importing Pin, ADC and PWM classes
from neopixel import NeoPixel      #importing NeoPixel (RGB lights) class
import machine
import utime

brg = 0.50
pixels = NeoPixel(Pin(4), 13) # Connector 5
leftServo = PWM(Pin(14))      # Connector 10
leftServo.freq(50)
rightServo = PWM(Pin(13))     # Connector 11
rightServo.freq(50)
builtinled = machine.Pin(2, machine.Pin.OUT) #built in LED
analogL=ADC(Pin(32))          #Connector 6
analogR=ADC(Pin(33))          #Connector 7
digitalL = machine.Pin(27, machine.Pin.IN) #Connector 8
digitalR = machine.Pin(15, machine.Pin.IN) #Connector 9
buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512) #built in buzzer
ultrasonicRGB = NeoPixel(Pin(18), 6)       # Connector 1
numberleds = 13
delaytime = 0.05
builtinled.off()

def red():
    global i, numberleds, delaytime
    for i in range(numberleds):
        pixels[i] = (int(255 * brg), int(0 * brg), int(0 * brg))
        pixels.write()
        sleep(delaytime)

def green():
    global i, numberleds, delaytime
    for i in range(numberleds):
        pixels[i] = (int(0 * brg), int(0 * brg), int(255 * brg))
        pixels.write()
        sleep(delaytime)

def blue():
    global i, numberleds, delaytime
    for i in range(numberleds):
        pixels[i] = (int(0 * brg), int(255 * brg), int(0 * brg))
        pixels.write()
        sleep(delaytime)

def white():
    global i, numberleds, delaytime
    for i in range(numberleds):
        pixels[i] = (int(255 * brg), int(255 * brg), int(255 * brg))
        pixels.write()
        sleep(delaytime)

def OttoNeo(index):
    global brg
    colors = [(255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0), (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255), (0, 0, 255), (127, 0, 255), (255, 0, 255), (255, 0, 127)]
    color = colors[index % len(colors)]
    for i in range(13):
        pixels[i] = (int(color[0] * brg), int(color[1] * brg), int(color[2] * brg))
    pixels.write()

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
builtinled.on()
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
pixels[0] = (int(255 * brg), int(1 * brg), int(1 * brg))
pixels[1] = (int(255 * brg), int(128 * brg), int(0 * brg))
pixels[2] = (int(255 * brg), int(255 * brg), int(0 * brg))
pixels[3] = (int(128 * brg), int(255 * brg), int(0 * brg))
pixels[4] = (int(0 * brg), int(255 * brg), int(0 * brg))
pixels[5] = (int(0 * brg), int(255 * brg), int(128 * brg))
pixels[6] = (int(0 * brg), int(255 * brg), int(255 * brg))
pixels[7] = (int(0 * brg), int(128 * brg), int(255 * brg))
pixels[8] = (int(0 * brg), int(0 * brg), int(255 * brg))
pixels[9] = (int(127 * brg), int(0 * brg), int(255 * brg))
pixels[10] = (int(255 * brg), int(0 * brg), int(255 * brg))
pixels[11] = (int(255 * brg), int(0 * brg), int(127 * brg))
pixels[12] = (int(255 * brg), int(255 * brg), int(255 * brg))
pixels.write()
color_index = 1

while True:
    analogL_value=analogL.read()           #reading analog pin
    analogR_value=analogR.read()           #reading analog pin
    distance = measure_distance()
    print("Left analog sensor:",analogL_value,"Right analog sensor:",analogR_value, "Distance:", measure_distance())
    print("Left digital sensor:",digitalL.value(),"Right digital sensor:",digitalR.value())
    print("Measured Distance:", distance)
    if (measure_distance()) < (10):
        print("Distance is less than 10, setting to red.")
        ultrasonicRGB[0] = (255, 0, 0)
        ultrasonicRGB[1] = (255, 0, 0)
        ultrasonicRGB[2] = (255, 0, 0)
        ultrasonicRGB[3] = (255, 0, 0)
        ultrasonicRGB[4] = (255, 0, 0)
        ultrasonicRGB[5] = (255, 0, 0)
        ultrasonicRGB.write()
        for count in range(13):
            pixels[count] = int(255 * brg), int(0 * brg), int(0 * brg)
        pixels.write()
        rightServo.duty(115)
        leftServo.duty(45)
        sleep(1)
        rightServo.duty(0)
        leftServo.duty(0)
        rightServo.duty(45)
        leftServo.duty(45)
        sleep(0.4)
        rightServo.duty(0)
        leftServo.duty(0)
    else:
        print("Distance is greater than or equal to 10, setting to OttoNeo.")
        OttoNeo(color_index)
        color_index += 1
        if color_index >= 12:
            color_index = 0
        ultrasonicRGB[0] = (51, 255, 51)
        ultrasonicRGB[1] = (51, 255, 51)
        ultrasonicRGB[2] = (51, 255, 51)
        ultrasonicRGB[3] = (51, 255, 51)
        ultrasonicRGB[4] = (51, 255, 51)
        ultrasonicRGB[5] = (51, 255, 51)
        ultrasonicRGB.write()
        for count in range(13):
            pixels[count] = int(0 * brg), int(255 * brg), int(0 * brg)
        pixels.write()
        rightServo.duty(45)
        leftServo.duty(115)
