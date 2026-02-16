# otto starter webcontrol v2.1 23.07.2024 works with libraries 2.0
import random, ubluetooth, ottosensors
from machine import Pin, Timer, PWM, ADC
from time import sleep_ms
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoNeoPixel
from ottoneopixel import OttoUltrasonic
from ottomotor import Motors
led = Pin(2, Pin.OUT)                   # Built in LED
buzzer = OttoBuzzer(25)                 # Built in Buzzer
ultrasonic = OttoUltrasonic(18, 19)     # Connector 1
analog = Pin(26, Pin.IN)                # Connector 4
n = 13                                  # Number of LEDs in ring
ring = OttoNeoPixel(4, n)               # Connector 5
ring.setBrightness(5)                   # brightness  for lights
line = ottosensors.FollowLine(32, 33, 27, 15) # Connectors 6 to 9
sensorL=ADC(Pin(32))                    # Connector 6 analog
sensorR=ADC(Pin(33))                    # Connector 7 analog
motors = Motors(right_motor_pin=13, left_motor_pin=14) # Connectors 10 & 11
toggleStatus = False
mode = 0
sliderR = 50
sliderL = 50

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
wipe(int(255), int(255), int(255), 50)
ultrasonic.ultrasonicRGB1("ffffff", "ffffff")
wipe(int(255), int(0), int(0), 50)
ultrasonic.ultrasonicRGB1("ff0000", "ff0000")
wipe(int(0), int(255), int(0), 50)
ultrasonic.ultrasonicRGB1("00ff00", "00ff00")
wipe(int(0), int(0), int(255), 50)
ultrasonic.ultrasonicRGB1("0000ff", "0000ff")

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
        motors.stop()
    elif v == 1:
        motors.move(sliderR, sliderL, "forward")
    elif v == 3:
        motors.move(sliderR, sliderL, "right")
    elif v == 7:
        motors.move(sliderR, sliderL, "left")
    elif v == 5:
        motors.move(sliderR, sliderL, "backward")        
        
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
    def handle_mode_1(self):
        # Function to execute during "mode-1"
        while True:
            buffer = self.ble.gatts_read(self.tx)
            message = buffer.decode('UTF-8').strip()
            if 'exit-mode' in message:
                print("Exiting Mode 1")
                break  # Exit the loop on "exit-mode"
            else:
                # Theremin
                distance = int(ultrasonic.readultrasonicRGB("cm"))
                if distance <= (10) and distance < (20):
                    ultrasonic.ultrasonicRGB1("ff6666", "ff6666")
                    buzzer.tone(buzzer.NOTE_C4, 100, 100)
                elif distance >= (20) and distance < (30):
                    ultrasonic.ultrasonicRGB1("ff9966", "ff9966")
                    buzzer.tone(buzzer.NOTE_D4, 100, 100)
                elif distance >= (30) and distance < (40):
                    ultrasonic.ultrasonicRGB1("ffff66", "ffff66")
                    buzzer.tone(buzzer.NOTE_E4, 100, 100)
                elif distance >= (40) and distance < (50):
                    ultrasonic.ultrasonicRGB1("ffff33", "ffff33")
                    buzzer.tone(buzzer.NOTE_F4, 100, 100)
                elif distance >= (50) and distance < (60):
                    ultrasonic.ultrasonicRGB1("66ff99", "66ff99")
                    buzzer.tone(buzzer.NOTE_G4, 100, 100)
                elif distance >= (60) and distance < (70):
                    ultrasonic.ultrasonicRGB1("33ffff", "33ffff")
                    buzzer.tone(buzzer.NOTE_A4, 100, 100)
                elif distance >= (70) and distance < (80):
                    ultrasonic.ultrasonicRGB1("66ffff", "66ffff")
                    buzzer.tone(buzzer.NOTE_B4, 100, 100)
                elif distance >= (80) and distance < (90):
                    ultrasonic.ultrasonicRGB1("9999ff", "9999ff")
                    buzzer.tone(buzzer.NOTE_C5, 100, 100)
                else:
                    ultrasonic.ultrasonicRGB1("000000", "000000")
            sleep_ms(200)
    def handle_mode_2(self):
        # Function to execute during "mode-2"
        while True:
            buffer = self.ble.gatts_read(self.tx)
            message = buffer.decode('UTF-8').strip()
            if message == "exit-mode":
                motors.stop()
                print("Exiting Mode 2")
                break  # Exit the loop on "exit-mode"
            else:
                # Avoidance
                if (ultrasonic.readultrasonicRGB(1)) <= (15):
                    ultrasonic.ultrasonicRGB1("cc0000", "cc0000")
                    motors.stop()
                    sleep_ms(200)
                    if (random.randint(1, 2)) == (1):
                        motors.move(sliderR, sliderL, "right")
                    else:
                        motors.move(sliderR, sliderL, "left")
                else:
                    ultrasonic.ultrasonicRGB1("ffffff", "ffffff")
                    motors.move(sliderR, sliderL, "forward")
    def handle_mode_3(self):
        # Function to execute during "mode-3"
        while True:
            buffer = self.ble.gatts_read(self.tx)
            message = buffer.decode('UTF-8').strip()
            if "exit-mode" in message:
                motors.stop()
                print("Exiting Mode 3")
                break  # Exit the loop on "exit-mode"
            else:
                # Line Follow
                sensorL_value=sensorL.read()
                sensorR_value=sensorR.read()
                if (sensorL_value) >= (700):
                    motors.move(sliderR, sliderL, "left")
                elif (sensorR_value) >= (700):
                    motors.move(sliderR, sliderL, "right")
                else:
                    motors.move(sliderR, sliderL, "forward")
    def connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()
    def disconnected(self):        
        self.timer1.init(
            period=1000,
            mode=Timer.PERIODIC,
            callback=lambda t: (
                ring.fillAllRGBRing("000077")
            )
        )
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: ring.fillAllRGBRing("000000"))   
    def ble_irq(self, event, data):
        global mode
        global toggleStatus
        global sliderR
        global sliderL
        digitalPinStatus = 0
        distance_cm = int(ultrasonic.readultrasonicRGB("cm"))
        lineRStatus = line.readLineRight()
        lineLStatus = line.readLineLeft()
        analogValue = analog.value()
        txtString = ''
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
            if 'mode-1' in message:
                self.handle_mode_1()
            elif 'mode-2' in message:
                self.handle_mode_2()
            elif 'mode-3' in message:
                self.handle_mode_3()
            elif 'exit-mode' in message:
                print("Exiting Mode")
                motors.stop()
                ultrasonic.ultrasonicRGB1("000000", "000000")
            elif 'update' in message:
                print('Update robot sensor values')
            elif 'forward' in message:
                motors.move(sliderR, sliderL, "forward")
            elif 'right ' in message:
                motors.move(sliderR, sliderL, "right")
            elif 'backward' in message:
                motors.move(sliderR, sliderL, "backward")
            elif 'left ' in message:
                motors.move(sliderR, sliderL, "left")
            elif 'stop' in message:
                motors.stop()
            elif 'J' in message:
                value = message[1:]
                value = int(value)
                JS(value)
            elif 's-' in message:
                buzzer.playEmoji(message[2:])
            elif 'S' in message:
                numbers = message.split('-')
                sliderR = int(numbers[0][1:])
                sliderL = int(numbers[1])
            elif message == 'simple':
                led.value(not led.value())
                digitalPinStatus = led.value()
            elif 'dance' in message:
                motors.move(sliderR, 0, "forward", 0.2)
                motors.move(0, sliderL, "forward", 0.2)
                motors.move(sliderR, 0, "backward", 0.2)
                motors.move(0, sliderL, "backward", 0.2)
            elif 'moonwalk-' in message:
                if 'left' in message:
                    for _ in range(2):
                        motors.move(sliderR, 0, "backward", 0.4)
                        motors.move(0, sliderL, "backward", 0.4)
                else:
                    for _ in range(2):
                        motors.move(sliderR, 0, "forward", 0.4)
                        motors.move(0, sliderL, "forward", 0.4)
            elif 'crossing-' in message:
                if 'left' in message:
                    motors.move(sliderR, sliderL, "left", 0.3)
                    motors.move(0, sliderL, "forward", 0.6)
                elif 'right' in message:
                    motors.move(sliderR, sliderL, "right", 0.3)
                    motors.move(sliderR, 0, "forward", 0.6)
            elif message == 'switchtoggle':
                toggleStatus = not toggleStatus
                if toggleStatus == True:
                    ring.fillAllRGBRing("FFFFFF")
                else:
                    ring.fillAllRGBRing("000000")
                    # check out the fun clear for this
            elif 'T' in message:
                print('Text sended: ')
                print(message[1:])
                txtString = message[1:]
            elif 'U' in message:
                ultrasonic.ultrasonicRGB1(message[7:],message[1:7])
            elif 'N' in message:
                color1 = decodeColor(message[13:14])
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
                color13 = decodeColor(message[1:2])
                ring.fillRGBRing(color1, color2, color3, color4, color5, color6, color7, color8, color9, color10, color11, color12, color13)
            elif 'led-' in message:
                print('LED Screen: ')
                print(message[4:])                
            elif 'n-' in message:
                note = message[2:]
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

ble = BLE("Ottoremote v2.1")
