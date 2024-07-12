# Testing multiple components at once, becareful many connections have changed from default pins
import machine, time, math, utime, dht
from ssd1306 import SSD1306_I2C
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor

led = Pin(2, Pin.OUT)             # Built in LED
buzzer = OttoBuzzer(25)           # Built in Buzzer

# Connector 1 pending add mp3
matrix = NeoPixel(Pin(16), 64)    # Connector 2
i2c=machine.I2C(0,sda=Pin(21), scl=Pin(22), freq=400000) # Connector 3
oled = SSD1306_I2C(128, 64, i2c)

button = Pin(26, Pin.IN)          # Connector 4
# Connector 5 tilt?

pot=ADC(Pin(32))                  # Connector 6
light=ADC(Pin(33))                # Connector 7

pot.atten(ADC.ATTN_11DB)    
light.atten(ADC.ATTN_0DB)

output = Pin(27, Pin.OUT)         # Connector 8

dht = dht.DHT11(Pin(15))          # Connector 9

motor = OttoMotor(13, 14)         # Connectors 10 & 11

def draw(bits,r=0, g=0, b=0):
   for i, bit in enumerate(bits):
       if bit == '1':
           matrix[i] = (r, g, b)
   matrix.write()
   sleep(0.01)

def pixel(row, col, r=0, g=0, b=0, color=''):
   if color == '':
       matrix[col + (row*8)] = (r, g, b)
       matrix.write()
   else:
       matrix[col + (row*8)] = self.color
       matrix.write();

pixel(1, 0, 255,0,0)

def map(value, in_min, in_max, out_min, out_max):
   map = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
   return map

buzzer.playEmoji("S_JUMP")
draw("1111111111111111111111111111111111111111111111111111111111111111",50,0,0)

while True:
    print("Potentiometer:", pot.read())
    matrix[(int(map(pot.read(), 0, 4095, 0, 63)))] = (0, 0, 30)
    matrix[(int(map(light.read(), 0, 4095, 0, 63)))] = (30, 30, 0)

    matrix.write()
    """
    #for faster meassurements of analog inputs dht must be deleted
    dht.measure()
    temp = dht.temperature()
    hum = dht.humidity()
    print('Temperature: %3.1f C' %temp)
    print('Humidity: %3.1f %%' %hum)
    sleep(0.1)
    """
    
    oled.fill(0)
    oled.text("Pot:{}".format(pot.read()), 0, 0)
    oled.text("* {}%".format(int(map(light.read(), 4095, 0, 0, 100))), 0, 12)
    oled.fill_rect(48,12,int(map(light.read(), 4095, 0, 0, 80)),8,1) 
    #oled.text('Temp: %3.1f C' %temp, 0, 24)
    #oled.text('Humidity: %3.1f %%' %hum, 0, 36)
    oled.show()
    
    matrix.fill((0,0,0))
    
    if (button.value()) == (1):
        draw("1111111111111111111111111111111111111111111111111111111111111111",0,30,0)
        led.on()
        oled.text('Button pushed', 0, 48)
        oled.show()
        output.value(1)
        buzzer.playNote(261, 125)
        buzzer.playNote(293, 125)
        buzzer.playNote(329, 125)
        buzzer.playNote(349, 125)
    else:
        output.value(0)
        led.off()