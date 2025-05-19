import random, ubluetooth
from machine import Pin, Timer, PWM, ADC
import time
from ottobuzzer import OttoBuzzer
from ottoneopixel import OttoUltrasonic
from ottomotor import OttoMotor

led = Pin(2, Pin.OUT)                   # Built in LED
buzzer = OttoBuzzer(25)                 # Built in Buzzer
ultrasonic = OttoUltrasonic(18, 19)      # Connector 1
motor = OttoMotor(13, 14) # Connectors 10 & 11
sliderR = 40
sliderL = 50

#servo duty values
loDutyL = 25
hiDutyL = 125
midDutyL = 75 #int(loDutyL + (hiDutyL - loDutyL)/2)

loDutyR = 25
hiDutyR = 125
midDutyR = 75 #int(loDutyR + (hiDutyR - loDutyR)/2)

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
        time.sleep(t)
        motor.Stop(1)        

        
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
        self.timer1.init(
            period=1000,
            mode=Timer.PERIODIC,
            callback=lambda t: (
                ultrasonic.ultrasonicRGB1('000077', '000077'),
                buzzer.playNote(261,125)
            )
        )
        time.sleep_ms(200)
        self.timer2.init(period=1000, mode=Timer.PERIODIC, callback=lambda t: ultrasonic.ultrasonicRGB1('000000', '000000'))
        
    def ble_irq(self, event, data):
        global sliderR
        global sliderL
        distance_cm = int(ultrasonic.readultrasonicRGB("cm"))
        
        if event == 1:
            '''Connected'''
            self.connected()
            ultrasonic.ultrasonicRGB1('007700', '007700')
            self.led(0)
            print('Otto connected')
            ultrasonic.ultrasonicRGB1('000000', '000000')
            
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
                buzzer.playEmoji('S_connection')
            
            elif 'Wait' in message:
                print(float(message[5:-1]))
                time.sleep(float(message[5:-1]))
            
            elif 'SetSpeed' in message:
                left_index = message.find('(')
                comma_index = message.find(',')
                right_index = message.find(')')
                if left_index != -1 and comma_index != -1 and right_index != -1:
                    sliderR = int(message[left_index + 1: comma_index].strip())
                    sliderL = int(message[comma_index + 1: right_index].strip())
                    print(sliderR, sliderL)

                else:
                    # Handle case where required characters are not found
                    print("Required characters not found in the message.")
                    return None, None

            # Lights
            elif 'RightEye' in message:
                print(message[11:-2])
                ultrasonic.ultrasonicRGB1('000000', message[11:-2])
                
            elif 'LeftEye' in message:
                ultrasonic.ultrasonicRGB1(message[11:-2], '000000')
            
            elif 'BothEyes' in message:
                ultrasonic.ultrasonicRGB1(message[11:-2], message[11:-2])
            
            # Movement
            elif 'Forward' in message:
                #print('Go forward')
                MotorsMove(sliderR, sliderL, "forward", float(message[8:-1]))
                time.sleep(0.3)
                
            elif 'Right' in message:
                #print('Turn right')
                MotorsMove(sliderR, sliderL, "right", float(message[6:-1]))
                time.sleep(0.3)
                
            elif 'Backward' in message:
                #print('Go backward')
                MotorsMove(sliderR, sliderL, "backward", float(message[9:-1]))
                time.sleep(0.3)
                
            elif 'Left' in message:
                #print('Turn left')
                MotorsMove(sliderR, sliderL, "left", float(message[5:-1]))
                time.sleep(0.3)
                
            elif 'Stop' in message:
                #print('Stop motors')
                motor.Stop(1)
            
            elif 'MoveLoop' in message:
                print(message[10:-2])
                val = message[10:-2]
                if val == "forward":
                    MotorsMove(sliderR, sliderL, "forward")
                elif val == "backward":
                    MotorsMove(sliderR, sliderL, "backward")
                elif val == "right":
                    MotorsMove(sliderR, sliderL, "right")
                elif val == "left":
                    MotorsMove(sliderR, sliderL, "left")
                
            # Sounds
            elif 'PlayS' in message:
                buzzer.playEmoji(message[7:-2])
                
            elif 'PlayTone' in message:
                print(message[9:-1])
            
            elif 'noTone' in message:
                print('No tone')
                
                
            self.send('Done!')
            
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

ble = BLE("GPTTO")
