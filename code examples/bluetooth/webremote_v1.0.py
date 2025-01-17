# otto starter webcontrol v01 21.3.2024
from machine import Pin 
from machine import Timer
from time import sleep_ms
import ubluetooth
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoNeoPixel
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor
import ottosensors

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ultrasonic = OttoUltrasonic(18,19)    # Connector 1
analog = Pin(26, Pin.IN)              # Connector 4
n = 13                                 # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
ring.setBrightness(5)                 # brightness for lights
line = ottosensors.FollowLine(32, 33, 27, 15) # Connectors 6 to 9 
toggleStatus = False

def wipe(r, g, b, wait):
    global i, n, delaytime
    for i in range(n):
        ring.pixels[i] = (r, g, b)
        ring.pixels.write()
        sleep_ms(wait)

buzzer.playNote(261,125)
buzzer.playNote(293,125)
buzzer.playNote(329,125)
buzzer.playNote(349,125)
buzzer.playNote(392,125)
buzzer.playNote(440,125)
buzzer.playNote(493,125)
buzzer.playNote(523,125)

wipe(int(255), int(0), int(0), 50)
ultrasonic.ultrasonicRGB("ff0000", "ff0000")
wipe(int(0), int(255), int(0), 50)
ultrasonic.ultrasonicRGB("00ff00", "00ff00")
wipe(int(0), int(0), int(255), 50)
ultrasonic.ultrasonicRGB("0000ff", "0000ff")
wipe(int(255), int(255), int(255), 50)
ultrasonic.ultrasonicRGB("ffffff", "ffffff")

def map_value(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def decodeColor(color):
    if color == "0":
        return "000000"
    elif color == "1":
        return "FFFFFF"
    elif color == "2":
        return "FF0000"
    elif color == "3":
        return "FF8000"
    elif color == "4":
        return "FFFF00"
    elif color == "5":
        return "7DFF00"
    elif color == "6":
        return "00FF00"
    elif color == "7":
        return "00FF7D"
    elif color == "8":
        return "00FFFF"
    elif color == "9":
        return "007DFF"
    elif color == "a":
        return "0000FF"
    elif color == "b":
        return "7D00FF"
    elif color == "c":
        return "FF00FF"
    elif color == "d":
        return "FF007D"

def JS(v):
    if v == 0:
        motor = OttoMotor(14, 13)
        motor.Stop(1)
    elif v == 1:
        motor = OttoMotor(14, 13)
        motor.Moveloop(-1, 2)
    elif v == 2:
        motor = OttoMotor(14, 13)
        motor.Rotate(1)
    elif v == 3:
        motor = OttoMotor(14, 13)
        motor.Rotate(0)
    elif v == 4:
        motor = OttoMotor(14, 13)
        motor.Moveloop(1, 2)
        
class BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()

    def disconnected(self):        
        self.timer1.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: ring.fillAllRGBRing("000077"))
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: ring.fillAllRGBRing("000000"))   

    def ble_irq(self, event, data):
        global toggleStatus
        sliderValue = 0
        digitalPinStatus = 0
        distance_cm = int(ultrasonic.readultrasonicRGB("cm"))
        lineRStatus = line.readLineRight()
        lineLStatus = line.readLineLeft()
        analogValue = analog.value()
        txtString = ''
        
        last_js = -1
        
        if event == 1:
            '''Connected'''
            self.connected()
            ring.fillAllRGBRing("00AA00")
            self.led(0)
            print('Otto connected')
            buzzer.playEmoji("S_connection")
            ring.fillAllRGBRing("000000")
            
        elif event == 2:
            '''Disconnected'''
            self.advertiser()
            self.disconnected()
            buzzer.playEmoji("S_disconnection")
        
        elif event == 3:
            '''New message received'''            
            buffer = self.ble.gatts_read(self.tx)
            message = buffer.decode('UTF-8').strip()
            #print(message)            
            if 'Connect-' in message:
                print('Type of Otto connected: ')
                print(message[8:])
            
            elif 'update' in message:
                print('Update robot sensor values')
                
            elif 'forward' in message:
                motor = OttoMotor(14, 13)
                motor.Moveloop(-1, 2)
                print('Go forward')
                
            elif 'right ' in message:
                print('Turn right')
                motor = OttoMotor(14, 13)
                motor.Rotate(1)
                
            elif 'backward' in message:
                print('Go backward')
                motor = OttoMotor(14, 13)
                motor.Moveloop(1, 2)
                
            elif 'left ' in message:
                print('Turn left')
                motor = OttoMotor(14, 13)
                motor.Rotate(0)
                
            elif 'stop' in message:
                print('Stop motors')
                motor = OttoMotor(14, 13)
                motor.Stop(1)
                
            elif 'J' in message:
                values = message[1:].split(',')
                x, y = map(int, values)
                #print(x, ', ', y)
                if y < -10:
                    if x > 10:
                        # front right
                        js = 5
                    elif x < -10:
                        # front left
                        js = 6
                    else:
                        # front
                        js = 1
                elif y > 10:
                    if x > 10:
                        # back right
                        js = 7
                    elif x < -10:
                        # back left
                        js = 8
                    else:
                        # back
                        js = 4
                elif x > 10:
                    # right
                    js = 2
                elif x < -10:
                    # left
                    js = 3
                else:
                    # stop
                    js = 0
                
                if js != last_js:
                    last_js = js
                    #print(js)
                    JS(js)         
                
            elif 'S' in message:
                print('Slider: ')
                print(message[1:])
            
            elif message == 'simple':
                #print('Digital Pin Status changed')
                led.value(not led.value())
                digitalPinStatus = led.value()
                
            elif 'dance' in message:
                print('Dance move ')
            
            elif 'moonwalk-' in message:
                print('Dance move: ')
                print(message)
                
            elif 'crossing-' in message:
                print('Dance move: ')
                print(message)
            
            elif message == 'switchtoggle':
                #print('Toggle switch changed')
                toggleStatus = not toggleStatus
                #print(toggleStatus)
                if toggleStatus == True:
                    ring.fillAllRGBRing("FFFFFF")
                else:
                    ring.fillAllRGBRing("000000")
                    # check out the fun clear for this
                
            elif 'mode' in message:
                print('Mode activated: ')
                print(message)
            
            elif 'T' in message:
                print('Text sended: ')
                print(message[1:])
                txtString = message[1:]
            
            elif 'U' in message:
                #print('Ultrasound LEDs activated')
                #print(message[1:7])
                ultrasonic.ultrasonicRGB(message[7:],message[1:7])
            
            elif 'N' in message:
                #print('Activate Neopixel ring')
                color1 = decodeColor(message[1:2])
                color2 = decodeColor(message[2:3])
                color3 = decodeColor(message[3:4])
                color4 = decodeColor(message[4:5])
                color5 = decodeColor(message[5:6])
                color6 = decodeColor(message[6:7])
                color7 = decodeColor(message[7:8])
                color8 = decodeColor(message[8:9])
                color9 = decodeColor(message[9:10])
                color10 = decodeColor(message[10:11])
                color11 = decodeColor(message[11:12])
                color12 = decodeColor(message[12:13])
                color13 = decodeColor(message[13:14])
                ring.fillRGBRing(color1, color2, color3, color4, color5, color6, color7, color8, color9, color10, color11, color12, color13)
            
            
            elif 'led-' in message:
                print('LED Screen: ')
                print(message[4:])
                
            elif 'n-' in message:
                print('Music note: ')
                note = message[2:]
                print(message[2:])
                if note == "do":
                    buzzer.tone(buzzer.NOTE_C4, 100, 100)
                elif note == "re":
                    buzzer.tone(buzzer.NOTE_D4, 100, 100)
                elif note == "mi":
                    buzzer.tone(buzzer.NOTE_E4, 100, 100)
                elif note == "fa":
                    buzzer.tone(buzzer.NOTE_F4, 100, 100)
                elif note == "sol":
                    buzzer.tone(buzzer.NOTE_G4, 100, 100)
                elif note == "la":
                    buzzer.tone(buzzer.NOTE_A4, 100, 100)
                elif note == "si":
                    buzzer.tone(buzzer.NOTE_B4, 100, 100)
                elif note == "edo":
                    buzzer.tone(buzzer.NOTE_C5, 100, 100)
                
            elif 'happy' in message:
                print('Sound: happy')
                buzzer.playEmoji("S_happy")
            
            elif 'sad' in message:
                print('Sound: sad')
                buzzer.playEmoji("S_sad")
            
            elif 'confused' in message:
                print('Sound: confused')
                buzzer.playEmoji("S_confused")
            
            elif 'cuddle' in message:
                print('Sound: cuddle')
                buzzer.playEmoji("S_cuddly")
            
            elif 'oh!' in message:
                print('Sound: oh!')
                buzzer.playEmoji("S_OhOoh")
            
            elif 'surprised' in message:
                print('Sound: surprised')
                buzzer.playEmoji("S_surprise")
            
            elif 'disconnect' in message:
                print('Sound: disconnect')
                buzzer.playEmoji("S_disconnection")
                
            elif 'connect' in message:
                print('Sound: connect')
                buzzer.playEmoji("S_connection")
            
            elif 'push' in message:
                print('Sound: push')
                buzzer.playEmoji("S_buttonPushed")
            
            elif '!1' in message:
                print('Sound: !1')
                buzzer.playEmoji("S_mode1")
            
            elif '!!2' in message:
                print('Sound: !!2')
                buzzer.playEmoji("S_mode2")
            
            elif '!!!3' in message:
                print('Sound: !!!3')
                buzzer.playEmoji("S_mode3")
            
            elif 'sleep' in message:
                print('Sound: sleep')
                buzzer.playEmoji("S_sleeping")
            
            elif 'fart' in message:
                print('Sound: fart')
                buzzer.playEmoji("S_fart1")
            
            self.send('{"D":'+str(digitalPinStatus)+',"U":'+str(distance_cm)+',"R":'+str(lineRStatus)+',"L":'+str(lineLStatus)+',"A":'+str(analogValue)+',"T":"'+str(txtString)+'"}')
    def register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
            
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY | ubluetooth.FLAG_WRITE | ubluetooth.FLAG_READ)
            
        BLE_UART = (BLE_NUS, (BLE_TX,))
        SERVICES = (BLE_UART, )
        ((self.tx,), ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytes([0x02, 0x01, 0x02]) + bytes([len(name) + 1, 0x09]) + name)

ble = BLE("Ottoremote v1")



