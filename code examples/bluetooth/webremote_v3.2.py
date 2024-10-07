# otto starter webcontrol v3.2 07.09.2024
# v01, v02 Iván R. Artiles Bretón
# v03 Iván R. Artiles Bretón, Alex Etchells
# reference to ottomotor.Motors replaced with ottomptor.OttoMotor
# led control code updated for new ring configuration
# Mode code moved to timer to be compatible with micropythom v1.20 on
# additon of battery voltage to status string
# in v3.2 modifed the battery status to display percentage every minute
# changes in formatting to conform with new preferred  practice
# v04 updated to changes in ultrasonic lib v2.0

import random, ubluetooth, ottosensors
from machine import Pin, Timer, PWM, ADC
from time import sleep_ms,sleep, ticks_ms, ticks_diff
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoNeoPixel
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor
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
motor = OttoMotor(13, 14)               # Connectors 10 & 11
toggleStatus = False
mode = 0
sliderR = 50
sliderL = 50
battery = ADC(Pin(39))      
battery.atten(ADC.ATTN_11DB)  #0 - 3.3v range
battery_percentage = 0

#servo duty values
loDutyL = 25
hiDutyL = 125
midDutyL = 75 #int(loDutyL + (hiDutyL - loDutyL)/2)

loDutyR = 25
hiDutyR = 125
midDutyR = 75 #int(loDutyR + (hiDutyR - loDutyR)/2)

'''
temporary function to translate commands for Motors class to OttoMotor class
ultimately to be moved to the OttoMotor class or replaced with a new method 
in OttoMotor 
'''
def MotorsMove(right_speed, left_speed, direction, t=None):
    right_speed = int(right_speed/2)
    left_speed = int(left_speed/2)

    if direction == "forward":
        motor.leftServo.duty(midDutyL + left_speed) 
        motor.rightServo.duty(midDutyR - right_speed) 
    elif direction == "backward":
        motor.leftServo.duty(midDutyL - left_speed) 
        motor.rightServo.duty(midDutyR + right_speed) 
    elif direction == "right":
        motor.leftServo.duty(midDutyL + left_speed) 
        motor.rightServo.duty(midDutyR + right_speed) 
    elif direction == "left":
        motor.leftServo.duty(midDutyL - left_speed) 
        motor.rightServo.duty(midDutyR - right_speed) 
    else:
        raise ValueError("Invalid direction")

    if t is not None:
        sleep(t)
        motor.Stop(1)        

def wipe(r, g, b, wait):
    global i, n, delaytime
    for i in range(n):
        ring.pixels[i] = (r, g, b)
        ring.pixels.write()
        sleep_ms(wait)

def get_battery_percentage(battery_reading, min_voltage=3.2, max_voltage=4.2):
    """
    Convert the raw battery reading from ADC to an integer battery percentage.
    :param battery_reading: The raw ADC value from battery.read()
    :param min_voltage: The minimum voltage corresponding to 0% battery (default 3.2V)
    :param max_voltage: The maximum voltage corresponding to 100% battery (default 4.2V)
    :return: Battery percentage as an integer
    """
    # Convert ADC value to voltage
    measV = battery_reading * 3.3 / 4095
    voltage = measV * 90 / 51  # Apply calibration factor
    # Calculate the battery percentage
    percentage = (voltage - min_voltage) / (max_voltage - min_voltage) * 100
    # Limit the percentage to 0-100%
    percentage = max(0, min(percentage, 100))
    # Return percentage as an integer
    return int(percentage)
        
buzzer.playNote(261,125)
buzzer.playNote(293,125)
buzzer.playNote(329,125)
buzzer.playNote(349,125)
buzzer.playNote(392,125)
buzzer.playNote(440,125)
buzzer.playNote(493,125)
buzzer.playNote(523,125)
wipe(int(255), int(0), int(0), 50)
ultrasonic.ultrasonicRGB1("ff0000", "ff0000")
wipe(int(0), int(255), int(0), 50)
ultrasonic.ultrasonicRGB1("00ff00", "00ff00")
wipe(int(0), int(0), int(255), 50)
ultrasonic.ultrasonicRGB1("0000ff", "0000ff")
wipe(int(255), int(255), int(255), 50)
ultrasonic.ultrasonicRGB1("ffffff", "ffffff")
 
def DecodeColor(color):
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
        motor.Stop(1)
    elif v == 1:
        MotorsMove(sliderR, sliderL, "forward")
    elif v == 3:
        MotorsMove(sliderR, sliderL, "right")
    elif v == 7:
        MotorsMove(sliderR, sliderL, "left")
    elif v == 5:
        MotorsMove(sliderR, sliderL, "backward")        
        
class BLE():
    def __init__(self, name):
        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)
        self.led = Pin(2, Pin.OUT)
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)
        self.Disconnected()
        self.ble.irq(self.BLE_irq)
        self.Register()
        self.Advertiser()
        self.curMode = 0
        self.last_voltage_update = ticks_ms()
            
        def tick(timer):   # we will receive the timer object when being called
                if self.curMode == 1:
                    self.Mode_1()
                elif self.curMode == 2:
                    self.Mode_2()
                elif self.curMode == 3:
                    self.Mode_3()
        
        timer3 = Timer(3)  # create a timer object using timer 3
        timer3.init(period=100, mode=Timer.PERIODIC, callback=tick)    
    
    def Mode_1(self):
        # Function to execute during "mode-1"
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
                    
    def Mode_2(self):
        # Function to execute during "mode-2"
        # Avoidance
        if (ultrasonic.readultrasonicRGB(1)) <= (15):
            ultrasonic.ultrasonicRGB1("cc0000", "cc0000")
            motor.Stop(1)
            sleep_ms(200)
            if (random.randint(1, 2)) == (1):
                MotorsMove(sliderR, sliderL, "right")
            else:
                MotorsMove(sliderR, sliderL, "left")
        else:
            ultrasonic.ultrasonicRGB1("ffffff", "ffffff")
            MotorsMove(sliderR, sliderL, "forward")
            
    def Mode_3(self):
        # Function to execute during "mode-3"
        # Line Follow
        sensorL_value=sensorL.read()
        sensorR_value=sensorR.read()
        if (sensorL_value) >= (700):
            MotorsMove(sliderR, sliderL, "left")
        elif (sensorR_value) >= (700):
            MotorsMove(sliderR, sliderL, "right")
        else:
            MotorsMove(sliderR, sliderL, "forward")
            
    def Connected(self):        
        self.timer1.deinit()
        self.timer2.deinit()
    def Disconnected(self):
        self.curMode = 0
        motor.Stop(1)
        self.timer1.init(
            period=1000,
            mode=Timer.PERIODIC,
            callback=lambda t: (
                ring.fillAllRGBRing("000077")
            )
        )
        sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, 
            callback=lambda t: ring.fillAllRGBRing("000000"))   
    def BLE_irq(self, event, data):
        global mode
        global toggleStatus
        global sliderR
        global sliderL
        global battery_percentage
        digitalPinStatus = 0
        distance_cm = int(ultrasonic.readultrasonicRGB("cm"))
        lineRStatus = line.readLineRight()
        lineLStatus = line.readLineLeft()
        analogValue = analog.value()
        txtString = ''
        # Check if 60 seconds (60000 ms) have passed
        current_time = ticks_ms()
        if ticks_diff(current_time, self.last_voltage_update) > 60000:
            # Update voltage value
            battery_reading = battery.read()  # Get the raw ADC value
            battery_percentage = get_battery_percentage(battery_reading)
            self.last_voltage_update = current_time  # Reset the timer

        if event == 1:
            '''Connected'''
            self.Connected()
            ring.fillAllRGBRing("00AA00")
            self.led(0)
            print('Otto Connected')
            buzzer.playEmoji("S_connection")
            ring.fillAllRGBRing("000000")
            battery_reading = battery.read()  # Get the raw ADC value
            battery_percentage = get_battery_percentage(battery_reading)
        elif event == 2:
            '''Disconnected'''
            self.Advertiser()
            self.Disconnected()
            buzzer.playEmoji("S_disconnection")
        elif event == 3:
            '''New message received'''
            try:
                buffer = self.ble.gatts_read(self.tx)
                message = buffer.decode('UTF-8').strip()
                if 'mode-1' in message:
                    self.curMode = 1
                elif 'mode-2' in message:
                    self.curMode = 2
                elif 'mode-3' in message:
                    self.curMode = 3
                elif 'exit-mode' in message:
                    print("Exiting Mode")
                    self.curMode = 0
                    motor.Stop(1)
                    ultrasonic.ultrasonicRGB1("000000", "000000")          
                elif 'Connect-' in message:
                    print('Type of Otto Connected: ')
                    print(message[8:])       
                elif 'update' in message:
                    print('Update robot sensor values')
                elif 'forward' in message:
                    MotorsMove(sliderR, sliderL, "forward")
                elif 'right ' in message:
                    MotorsMove(sliderR, sliderL, "right")
                elif 'backward' in message:
                    MotorsMove(sliderR, sliderL, "backward")
                elif 'left ' in message:
                    MotorsMove(sliderR, sliderL, "left")
                elif 'stop' in message:
                    motor.Stop(1)
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
                    MotorsMove(sliderR, 0, "forward", 0.2)
                    MotorsMove(0, sliderL, "forward", 0.2)
                    MotorsMove(sliderR, 0, "backward", 0.2)
                    MotorsMove(0, sliderL, "backward", 0.2)
                elif 'moonwalk-' in message:
                    if 'left' in message:
                        for _ in range(2):
                            MotorsMove(sliderR, 0, "backward", 0.4)
                            MotorsMove(0, sliderL, "backward", 0.4)
                    else:
                        for _ in range(2):
                            MotorsMove(sliderR, 0, "forward", 0.4)
                            MotorsMove(0, sliderL, "forward", 0.4)
                elif 'crossing-' in message:
                    if 'left' in message:
                        MotorsMove(90, 90, "left", 0.3)
                        MotorsMove(0, 90, "forward", 0.6)
                    elif 'right' in message:
                        MotorsMove(90, 90, "right", 0.3)
                        MotorsMove(90, 0, "forward", 0.6)
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
                    color13 = DecodeColor(message[1:2])
                    color2 = DecodeColor(message[2:3])
                    color3 = DecodeColor(message[3:4])
                    color4 = DecodeColor(message[4:5])
                    color5 = DecodeColor(message[5:6])
                    color6 = DecodeColor(message[6:7])
                    color7 = DecodeColor(message[7:8])
                    color8 = DecodeColor(message[8:9])
                    color9 = DecodeColor(message[9:10])
                    color10 = DecodeColor(message[10:11])
                    color11 = DecodeColor(message[11:12])
                    color12 = DecodeColor(message[12:13])
                    color1 = DecodeColor(message[13:14])
                    ring.fillRGBRing(color1, color2, color3, color4, color5, 
                        color6, color7, color8, color9, color10, color11, 
                        color12, color13)
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
            except Exception as err:
                print("except ", err)
            self.Send('{"D":' + str(digitalPinStatus) + 
                    ',"U":' + str(distance_cm) + ',"R":' + str(lineRStatus) + 
                    ',"L":' + str(lineLStatus) + ',"A":' + str(analogValue) + 
                    ',"T":"' + str(txtString) + '","B":' + str(battery_percentage) + '}')            
    def Register(self):        
        # Nordic UART Service (NUS)
        NUS_UUID = '6e400001-b5a3-f393-e0a9-e50e24dcca9e'
        TX_UUID = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'
        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY | 
            ubluetooth.FLAG_WRITE | ubluetooth.FLAG_READ)
        BLE_UART = (BLE_NUS, (BLE_TX,))
        SERVICES = (BLE_UART, )
        ((self.tx,), ) = self.ble.gatts_register_services(SERVICES)
    def Send(self, data):
        self.ble.gatts_notify(0, self.tx, data + '')
    def Advertiser(self):
        name = bytes(self.name, 'UTF-8')
        self.ble.gap_advertise(100, bytes([0x02, 0x01, 0x02]) + 
            bytes([len(name) + 1, 0x09]) + name)
ble = BLE("OttoReact")
