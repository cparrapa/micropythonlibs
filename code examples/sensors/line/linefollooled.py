import machine, utime
from time import sleep                    #importing sleep class
from neopixel import NeoPixel
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from ottodisplay import OttoOled
from ssd1306 import SSD1306_I2C
from machine import Pin, SoftI2C
i2c = SoftI2C(sda=Pin(19), scl=Pin(18)) # Connector 1
oled = SSD1306_I2C(128, 64, i2c) # width, height using default address 0x3C

brg = 0.75
pixels = NeoPixel(Pin(4), 13)
leftServo = PWM(Pin(14))
leftServo.freq(50)
rightServo = PWM(Pin(13))
rightServo.freq(50)
pin_led = machine.Pin(2, machine.Pin.OUT)
analogL=ADC(Pin(27))                  # Connector 6
analogR=ADC(Pin(15))                  # Connector 7
sensorL=ADC(Pin(32))           #creating potentiometer object
sensorR=ADC(Pin(33))           #creating potentiometer object
buzzer = PWM(Pin(25, Pin.OUT), freq=440, duty=512)

pin_led.off()
delaytime = 0.1


def oled_eyesclosed():
    oled.rect(16,0,96,33,0,True)
    oled.rect(16,16,32,6,1,True)
    oled.rect(80,16,32,6,1,True)
  
def oled_eyes():
    oled.rect(16,0,96,33,0,True)
    oled.ellipse(32,16,16,16,1,1)  #left eye
    oled.ellipse(32,16,10,10,0,1)  #left eye -
    oled.ellipse(96,16,16,16,1,1)  #right eye
    oled.ellipse(96,16,10,10,0,1)  #right eye -

def oled_eyesup():
    oled_eyes()
    oled.rect(0,16,128,17,0,True)
    
def oled_eyesup2():
    oled.rect(16,0,96,33,0,True)
    oled.ellipse(32,32,16,16,1,1)  
    oled.ellipse(32,32,10,10,0,1)  
    oled.ellipse(96,32,16,16,1,1) 
    oled.ellipse(96,32,10,10,0,1)  
    oled.rect(0,32,128,17,0,True)
    
def oled_eyesdown():
    oled_eyes()
    oled.rect(0,0,128,16,0,True)
    
def oled_eyesdown2():
    oled.rect(16,0,97,33,0,True)
    oled.ellipse(32,0,16,16,1,1) 
    oled.ellipse(32,0,10,10,0,1) 
    oled.ellipse(96,0,16,16,1,1)  
    oled.ellipse(96,0,10,10,0,1)  
    
def oled_eyeswinkleft():
    oled_eyes()
    oled.rect(64,0,128,16,0,True)
    
def oled_eyeswinkright():
    oled_eyes()
    oled.rect(0,0,64,16,0,True)
    
def oled_eyesangry():
    oled_eyes()
    triangle1 = array.array('I', [16,0,48,0,48,32])
    oled.poly(0,0, triangle1, 0, True)
    triangle2 = array.array('I', [80,0,112,0,80,32])
    oled.poly(0,0, triangle2, 0, True) 
    
def oled_eyesworry():
    oled_eyes()
    triangle1 = array.array('I', [16,0,48,0,16,32])
    oled.poly(0,0, triangle1, 0, True) 
    triangle2 = array.array('I', [80,0,112,0,112,32])
    oled.poly(0,0, triangle2, 0, True) 

def oled_mouthclosed():
    oled.rect(32,32,64,32,0,True)
    oled.rect(32,42,64,6,1,True)

def oled_mouth():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,48,16,16,1,1) 
    oled.ellipse(64,48,10,10,0,1)
    
def oled_mouthup():
    oled_mouth()
    oled.rect(48,32,33,16,0,True)
    
def oled_mouthup2():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,32,16,16,1,1) 
    oled.ellipse(64,32,10,10,0,1)
    oled.rect(48,16,33,16,0,True)
    
def oled_mouthdown():
    oled_mouth()
    oled.rect(48,48,33,16,0,True)

def oled_mouthdown2():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,64,16,16,1,1) 
    oled.ellipse(64,64,10,10,0,1)
    
def oled_mouthleft():
    oled_mouthclosed()
    oled.ellipse(80,53,15,11,1,1)
    oled.rect(64,48,32,5,1,True)
    
def oled_mouthright():
    oled_mouthclosed()
    oled.ellipse(48,53,15,11,1,1)
    oled.rect(32,48,32,5,1,True)
    
def oled_mouthhappy():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,48,15,15,1,1)
    oled.rect(48,32,32,16,1,True)
    
def oled_mouthworry():
    oled.rect(32,32,64,32,0,True)
    oled.ellipse(64,48,15,10,1,1)


def colorWipe():
    global delaytime, i
    for i in range(13):
        pixels[i] = (int(51 * brg), int(255 * brg), int(51 * brg))
        pixels.write()
        sleep(delaytime)
        
oled_eyes()
oled_mouth()
oled.show() 

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
    print(str("l") + str(analogL.read()))
    print(str("R") + str(analogR.read()))
    sensorL_value=sensorL.read()           #reading analog pin
    sensorR_value=sensorR.read()           #reading analog pin
    print("Left analog sensor:",sensorL_value,"Right analog sensor:",sensorR_value)
    if (sensorL_value) >= (700): #up to 1000
        pin_led.on()
        leftServo.duty(60) #70
        rightServo.duty(60) #70
        oled_eyeswinkleft()
        oled_mouthleft()
        oled.show() 
    elif (sensorR_value) >= (700): #1000
        pin_led.on()
        leftServo.duty(100) #90
        rightServo.duty(100) #90
        oled_eyeswinkright()
        oled_mouthright()
        oled.show() 
    else:
        pin_led.off()
        leftServo.duty(90) #faster 120
        rightServo.duty(60) #faster40
        oled_eyesup()
        oled_mouthup2()
        oled.show() 



