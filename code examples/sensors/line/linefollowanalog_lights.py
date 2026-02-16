import machine, utime
from time import sleep                    #importing sleep class
from neopixel import NeoPixel
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes

brg = 0.75
pixels = NeoPixel(Pin(4), 13)
leftServo = PWM(Pin(14))
leftServo.freq(50)
rightServo = PWM(Pin(13))
rightServo.freq(50)
pin_led = machine.Pin(2, machine.Pin.OUT)
digital_pin_L = machine.Pin(27, machine.Pin.IN)
digital_pin_R = machine.Pin(15, machine.Pin.IN)
sensorL=ADC(Pin(32))           #creating potentiometer object
sensorR=ADC(Pin(33))           #creating potentiometer object
buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512)
ultrasonicRGB = NeoPixel(Pin(18), 6)

pin_led.off()

delaytime = 0.1

def colorWipe():
    global delaytime, i
    for i in range(13):
        pixels[i] = (int(51 * brg), int(255 * brg), int(51 * brg))
        pixels.write()
        sleep(delaytime)

ultrasonicRGB[0] = (0, 0, 255)
ultrasonicRGB[1] = (0, 0, 255)
ultrasonicRGB[2] = (0, 0, 255)
ultrasonicRGB[3] = (0, 0, 255)
ultrasonicRGB[4] = (0, 0, 255)
ultrasonicRGB[5] = (0, 0, 255)
ultrasonicRGB.write()
print("Otto is alive!")
pin_led.on()
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
leftServo.freq(50)
rightServo.freq(50)
colorWipe()
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

while True:
    print("Left sensor:",digital_pin_L.value(),"Right sensor:",digital_pin_R.value())
    sensorL_value=sensorL.read()           #reading analog pin
    sensorR_value=sensorR.read()           #reading analog pin
    print("Left analog sensor:",sensorL_value,"Right analog sensor:",sensorR_value)
    if (sensorL_value) >= (700): #up to 1000
        pin_led.on()
        leftServo.duty(60) #70
        rightServo.duty(60) #70
        ultrasonicRGB[0] = (255, 255, 0)
        ultrasonicRGB[1] = (255, 255, 0)
        ultrasonicRGB[2] = (255, 255, 0)
        ultrasonicRGB[3] = (0, 0, 0)
        ultrasonicRGB[4] = (0, 0, 0)
        ultrasonicRGB[5] = (0, 0, 0)
        ultrasonicRGB.write()
    elif (sensorR_value) >= (700): #1000
        pin_led.on()
        leftServo.duty(100) #90
        rightServo.duty(100) #90
        ultrasonicRGB[0] = (0, 0, 0)
        ultrasonicRGB[1] = (0, 0, 0)
        ultrasonicRGB[2] = (0, 0, 0)
        ultrasonicRGB[3] = (255, 0, 255)
        ultrasonicRGB[4] = (255, 0, 255)
        ultrasonicRGB[5] = (255, 0, 255)
        ultrasonicRGB.write()
    else:
        pin_led.off()
        leftServo.duty(100) #faster 120
        rightServo.duty(60) #faster40
        ultrasonicRGB[0] = (255, 0, 0)
        ultrasonicRGB[1] = (255, 0, 0)
        ultrasonicRGB[2] = (255, 0, 0)
        ultrasonicRGB[3] = (255, 0, 0)
        ultrasonicRGB[4] = (255, 0, 0)
        ultrasonicRGB[5] = (255, 0, 0)
        ultrasonicRGB.write()


