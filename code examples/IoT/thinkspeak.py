import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
import network
import ubinascii
import urequests
from ottoneopixel import OttoUltrasonic
import utime

led = Pin(2, Pin.OUT)                 # Built in LED
def do_sta_connect():
 global sta_if
 sta_if = network.WLAN(network.STA_IF)
 if not sta_if.isconnected():
  sta_if.active(True)
  sta_if.connect("wifi","pass*")
 print("Connecting to network ...")
 while not sta_if.isconnected():
  pass
 print("Connected.The MAC address is: ", ubinascii.hexlify(sta_if.config('mac'), ':').decode().upper())
 print("The network values are: ", sta_if.ifconfig())

THINGSPEAK_API = 'api here'
def make_thingspeak_request(field="field1",value=""):
 print("Connecting")
 response = urequests.post('http://api.thingspeak.com/update?api_key=' + THINGSPEAK_API + "&"+field+"="+str(value))
 print(response.text)
 print (response.status_code)
 response.close()
 print("Closing Connection")

ultrasonic = OttoUltrasonic(18, 19)
io = 19     # echo input and trigger out signal

def distance():
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

do_sta_connect()
while True:
    dist = distance()
    make_thingspeak_request('field1',dist)
    print(dist)
    sleep((20))

