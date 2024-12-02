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

matrix = NeoPixel(Pin(22), 64) # connector 3
brightm = 0.3 # brightness variable for matrix lights

def draw(bits,r=0, g=0, b=0):
   for i, bit in enumerate(bits):
       if bit == '1':
           matrix[i] = (r, g, b)
   matrix.write()
   sleep(0.01)


pin_led.off()
delaytime = 0.1
ultrasonicRGB[0] = (255, 255, 255)
ultrasonicRGB[1] = (255, 255, 255)
ultrasonicRGB[2] = (255, 255, 255)
ultrasonicRGB[3] = (255, 255, 255)
ultrasonicRGB[4] = (255, 255, 255)
ultrasonicRGB[5] = (255, 255, 255)
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
    if (sensorL_value) >= (900):
        pin_led.on()
        leftServo.duty(65)
        rightServo.duty(65)
        ultrasonicRGB[0] = (255, 255, 0)
        ultrasonicRGB[1] = (255, 255, 0)
        ultrasonicRGB[2] = (255, 255, 0)
        ultrasonicRGB[3] = (0, 0, 255)
        ultrasonicRGB[4] = (0, 0, 255)
        ultrasonicRGB[5] = (0, 0, 255)
        ultrasonicRGB.write()
        matrix.fill((0,0,0))
        matrix.write()
        draw("0000000000000000000000000001100000111100011001101100001100000000",0,0,50)
    elif (sensorR_value) >= (900):
        pin_led.on()
        leftServo.duty(95)
        rightServo.duty(95)
        ultrasonicRGB[0] = (0, 0, 255)
        ultrasonicRGB[1] = (0, 0, 255)
        ultrasonicRGB[2] = (0, 0, 255)
        ultrasonicRGB[3] = (255, 0, 255)
        ultrasonicRGB[4] = (255, 0, 255)
        ultrasonicRGB[5] = (255, 0, 255)
        ultrasonicRGB.write()
        matrix.fill((0,0,0))
        matrix.write()
        draw("0000000000000000000000000100001001100110001111000001100000000000",0,0,50)
    else:
        pin_led.off()
        leftServo.duty(108) # 100 slower
        rightServo.duty(45) # 60 slower
        ultrasonicRGB[0] = (0, 0, 255)
        ultrasonicRGB[1] = (0, 0, 255)
        ultrasonicRGB[2] = (0, 0, 255)
        ultrasonicRGB[3] = (0, 0, 255)
        ultrasonicRGB[4] = (0, 0, 255)
        ultrasonicRGB[5] = (0, 0, 255)
        ultrasonicRGB.write()
        matrix.fill((0,0,0))
        matrix.write()
        draw("0000000001100110111111111111111101111110001111000001100000000000",0,50,0)





    