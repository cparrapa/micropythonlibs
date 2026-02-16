#***************************************
#      Self Hosted Web Control For HP Otto 
#       Alex Just-Alex Mar 2025
#***************************************

from micropyserver import MicroPyServer
import network
from secrets import WIFI_NAME, WIFI_PASS
from machine import Timer
import ottoWebInterface


import machine, time                       #importing machine and time libraries
from time import sleep                     #importing sleep class
from machine import Pin, ADC, PWM          #importing Pin, ADC and PWM classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
import utime

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
offsetL = 5                          # Calibration for left servo motor
offsetR = 0                           # Calibration for right servo motor

for i in range(6):
    ultrasonic[i] = 0, 0, 0
ultrasonic.write()



#meausre ultrasonic distance
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

def display_number(num,r,g,b):
    ring.fillAllRGBRing("000000")
    if num == 0:
        buzzer.playNote(359,.4)
        ring.setRGBLed(r,g,b,0)
        sleep(1)  
        ring.fillAllRGBRing("000000")  
        sleep(0.2)
        ring.setRGBLed(r,g,b,0)
        sleep(1)  
    for i in range(num):
        buzzer.playNote(659,.2)
        ring.setRGBLed(r,g,b,i+1)
        sleep(0.5)
    sleep(1)  
    ring.fillAllRGBRing("000000")  
    sleep(0.2)
    for i in range(num):
        ring.setRGBLed(r,g,b,i+1)    
    sleep(1)


def webpage():
    dist = str(int(measure_distance()))
    #Template HTML
    html = ottoWebInterface.webpage(dist)
    return str(html)


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_NAME, WIFI_PASS)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    buzzer.playEmoji("S_connection")
    ring.fillAllRGBRing("000000")
    
    #display ip using ring - comment out once you know the ip address
    """
    sleep(0.4)
    col = 1
    r = 0
    g = 0
    b = 0
    display_number(0,r,g,254)
    for c in ip:
        print(c)
        if c != ".":
            r = 0
            g = 0
            b = 0
            if col == 1:
                r = 254
                col = 2
            elif col == 2:
                g =254
                col = 3
            elif col == 3:
                b = 254
                col = 1
            display_number(int(c),r,g,b)
        else:
            buzzer.playNote(359,.4)
            col = 1
            sleep(0.5)
    
    ring.fillAllRGBRing("000000")
    buzzer.playEmoji("S_connection")
    """
    return ip


def show_index(request):
    ''' main request handler '''
    html = webpage()
    server.send(html)
    
def control_action(request):
    global walkStatus
    parts = request.split('/')
    walkStatus = parts[1].split('?')[0]
    html = webpage()
    server.send(html)

def move_action(request):
    html = ottoWebInterface.BLANKpage()
    server.send(html)
    global walkStatus
    global timer    
    timer.deinit()
    walkStatus = "STP"
    parts = request.split('/')
    cmd = parts[1].split('?')[0]    
    otto.home()
    if cmd =='M-F':
        otto.walk(2,1000,1)
    elif cmd =='M-B':
        otto.walk(2,1000,-1)
    elif cmd =='M-TL':
        otto.turn(2,1000,1)
    elif cmd =='M-TR':
        otto.turn(2,1000,-1)
    elif cmd =='M-BL':
        otto.bend(2,1000,1)
    elif cmd =='M-BR':
        otto.bend(2,1000,-1)
    elif cmd =='M-SL':
        otto.shakeLeg(1, 1500, 1)
    elif cmd =='M-SR"':
        otto.shakeLeg(1, 1500, -1)
    elif cmd =='M-ML':
        otto.moonwalker(3, 1000, 25, 1)
    elif cmd =='M-MR':
        otto.moonwalker(3, 1000, 25, -1)
    elif cmd =='M-CL':
        otto.crusaito(2, 1000, 20, 1)
    elif cmd =='M-CR':
        otto.crusaito(2, 1000, 20, -1)
    elif cmd =='M-FL':
        otto.flapping(2, 1000, 20, 1)
    elif cmd =='M-FR':
        otto.flapping(2, 1000, 20, -1)
    elif cmd =='M-SW':
        otto.swing(2, 1000, 20)
    elif cmd =='M-TS':
        otto.tiptoeSwing(2, 1000, 20)
    elif cmd =='M-JI':
        otto.jitter(2, 1000, 20)  
    elif cmd =='M-UD':
        otto.updown(2, 1500, 20)     
    elif cmd =='M-AT':
        otto.ascendingTurn(2, 1000, 50)
    elif cmd =='M-JU':
        otto.jump(1, 2000)
    hostip = otto.getip()    
    script =  f"""<script> window.location.href ="/UPD"</script>"""
    server.send(str(script))
    timer.init(period=200, mode=Timer.PERIODIC, callback=tick) 

def song_action(request):
    songs = ("S_connection","S_disconnection","S_surprise",
             "S_OhOoh","S_OhOoh2","S_cuddly",
             "S_sleeping", "S_happy","S_superHappy",
             "S_happy_short","S_sad","S_confused",
             "S_fart1","S_fart2","S_fart3",   
             "S_mode1","S_mode2","S_mode3",
             "S_buttonPushed")
    
    html = ottoWebInterface.BLANKpage()
    server.send(html)
    global timer    
    timer.deinit()
    parts = request.split('/')
    #print(parts)
    song = parts[1].split('?')[0]
    number = int(song.split('-')[1])
    #print("sing " + str(number))
    
    buzzer.playEmoji(songs[number])
    #otto.sing(number) 
    #hostip = otto.getip()    
    script =  f"""<script> window.location.href ="/UPD"</script>"""
    server.send(str(script))
    timer.init(period=200, mode=Timer.PERIODIC, callback=tick) 

def gesture_action(request):
    html = ottoWebInterface.BLANKpage()
    server.send(html)
    global walkStatus
    global timer    
    timer.deinit()
    walkStatus = "STP"
    parts = request.split('/')
    cmd = parts[1].split('?')[0]   
    number = int(cmd.split('-')[1]) 
    #otto.home()
    #otto.playGesture(number)
    #hostip = otto.getip()    
    script =  f"""<script> window.location.href ="/UPD"</script>"""
    server.send(str(script))
    timer.init(period=200, mode=Timer.PERIODIC, callback=tick) 

def tick(timer):
    #print("tick")
    timer.deinit()
    global walkStatus
    #print("walk status " + walkStatus)
    if walkStatus == "STP":
        motor.Stop(1)
    elif walkStatus == "FW":
        motor.leftServo.duty(100) 
        motor.rightServo.duty(50) 
    elif walkStatus == "L":
        motor.leftServo.duty(50) 
        motor.rightServo.duty(50) 
    elif walkStatus == "R":
        motor.leftServo.duty(100) 
        motor.rightServo.duty(100) 
    elif walkStatus == "BK":
        motor.leftServo.duty(50) 
        motor.rightServo.duty(100) 
    else:
        motor.Stop(1)
    timer.init(period=200, mode=Timer.PERIODIC, callback=tick)
    
def setPhone(request):
    ottoWebInterface.interface = "phone"
    html = webpage()
    server.send(html)
    
def setPC(request):
    ottoWebInterface.interface = "PC"
    html = webpage()
    server.send(html)
#------------------CODE--------------------


#otto = Otto()          
#otto.init(6, 5, 7, 9, False, 2, 0, 1)
#otto.setTrims(0,0,0,0) #edit to suit your bot
walkStatus = "STP"

timer = Timer(0)  # create a timer object using timer 0
timer.init(period=200, mode=Timer.PERIODIC, callback=tick)    

ip = connect()
server = MicroPyServer()
''' add routes '''
server.add_route("/", show_index)
server.add_route("/UPD", show_index)
server.add_route("/STP", control_action)
server.add_route("/FW", control_action)
server.add_route("/BK", control_action)
server.add_route("/L", control_action)
server.add_route("/R", control_action)
server.add_route("/M-F", move_action)
server.add_route("/M-B", move_action)
server.add_route("/M-TL", move_action)
server.add_route("/M-TR", move_action)
server.add_route("/M-BL", move_action)
server.add_route("/M-BR", move_action)
server.add_route("/M-SL", move_action)
server.add_route("/M-SR", move_action)
server.add_route("/M-ML", move_action)
server.add_route("/M-MR", move_action)
server.add_route("/M-CL", move_action)
server.add_route("/M-CR", move_action)
server.add_route("/M-FL", move_action)
server.add_route("/M-FR", move_action)
server.add_route("/M-SW", move_action)
server.add_route("/M-TS", move_action)
server.add_route("/M-JI", move_action)
server.add_route("/M-UD", move_action)
server.add_route("/M-AT", move_action)
server.add_route("/M-JU", move_action)
server.add_route("/S-0", song_action)
server.add_route("/S-1", song_action)
server.add_route("/S-2", song_action)
server.add_route("/S-3", song_action)
server.add_route("/S-4", song_action)
server.add_route("/S-5", song_action)
server.add_route("/S-6", song_action)
server.add_route("/S-7", song_action)
server.add_route("/S-8", song_action)
server.add_route("/S-9", song_action)
server.add_route("/S-10", song_action)
server.add_route("/S-11", song_action)
server.add_route("/S-12", song_action)
server.add_route("/S-13", song_action)
server.add_route("/S-14", song_action)
server.add_route("/S-15", song_action)
server.add_route("/S-16", song_action)
server.add_route("/S-17", song_action)
server.add_route("/S-18", song_action)
server.add_route("/G-0", gesture_action)
server.add_route("/G-1", gesture_action)
server.add_route("/G-2", gesture_action)
server.add_route("/G-3", gesture_action)
server.add_route("/G-4", gesture_action)
server.add_route("/G-5", gesture_action)
server.add_route("/G-6", gesture_action)
server.add_route("/G-7", gesture_action)
server.add_route("/G-8", gesture_action)
server.add_route("/G-9", gesture_action)
server.add_route("/G-10", gesture_action)
server.add_route("/G-11", gesture_action)
server.add_route("/G-12", gesture_action)
server.add_route("/PH", setPhone)
server.add_route("/PC", setPC)

''' start server '''
server.start()
