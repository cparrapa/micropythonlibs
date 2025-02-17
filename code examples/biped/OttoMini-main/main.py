#***************************************
#      Web Control For Otto Mini
#       Alex Just-Alex Nov 2024
#***************************************

from micropyserver import MicroPyServer
import network
from secrets import WIFI_NAME, WIFI_PASS
from MiniOtto import Otto
from time import sleep
from machine import Timer
import MO_WebInterface

def webpage():
    dist = str(int(otto.getDistanceCm()))
    #Template HTML
    html = MO_WebInterface.webpage(dist)
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
    otto.sing(0)
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
    html = MO_WebInterface.BLANKpage()
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
    html = MO_WebInterface.BLANKpage()
    server.send(html)
    global timer    
    timer.deinit()
    parts = request.split('/')
    #print(parts)
    song = parts[1].split('?')[0]
    number = int(song.split('-')[1])
    #print("sing " + str(number))             
    otto.sing(number) 
    hostip = otto.getip()    
    script =  f"""<script> window.location.href ="/UPD"</script>"""
    server.send(str(script))
    timer.init(period=200, mode=Timer.PERIODIC, callback=tick) 

def gesture_action(request):
    html = MO_WebInterface.BLANKpage()
    server.send(html)
    global walkStatus
    global timer    
    timer.deinit()
    walkStatus = "STP"
    parts = request.split('/')
    cmd = parts[1].split('?')[0]   
    number = int(cmd.split('-')[1]) 
    otto.home()
    otto.playGesture(number)
    hostip = otto.getip()    
    script =  f"""<script> window.location.href ="/UPD"</script>"""
    server.send(str(script))
    timer.init(period=200, mode=Timer.PERIODIC, callback=tick) 

def tick(timer):
    #print("tick")
    timer.deinit()
    global walkStatus
    #print("walk status " + walkStatus)
    if walkStatus == "STP":
        otto.home()
    elif walkStatus == "FW":
        otto.walk(2,1000,1)
    elif walkStatus == "L":
        otto.turn(2,1000,1)
    elif walkStatus == "R":
        otto.turn(2,1000,-1)
    elif walkStatus == "BK":
        otto.walk(2,1000,-1)
    else:
        otto.home()
    timer.init(period=200, mode=Timer.PERIODIC, callback=tick)
    
def setPhone(request):
    MO_WebInterface.interface = "phone"
    html = webpage()
    server.send(html)
    
def setPC(request):
    MO_WebInterface.interface = "PC"
    html = webpage()
    server.send(html)
#------------------CODE--------------------


otto = Otto()          
otto.init(6, 5, 7, 9, False, 2, 0, 1)
otto.setTrims(0,0,0,0) #edit to suit your bot
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
