import machine
import time                       # importing machine and time libraries
from time import sleep            # importing sleep class
from machine import Pin, ADC, PWM, I2C, SoftI2C # importing Pin, ADC, PWM and I2C classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
import network
import ubinascii
import utime
import ntptime
from machine import RTC
from ssd1306 import SSD1306_I2C  # Make sure you have this library
from rotary import Rotary

led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
ultrasonic = NeoPixel(Pin(18), 6)     # Connector 1
io = 19                               # echo input and trigger out signal
bright = 0.8                          # brightness variable for lights
n = 13                                # Number of LEDs in ring
ring = OttoNeoPixel(4, n)             # Connector 5
analogL = ADC(Pin(32))                # Connector 6
analogR = ADC(Pin(33))                # Connector 7
digitalL = Pin(27, Pin.IN)            # Connector 8
digitalR = Pin(15, Pin.IN)            # Connector 9
motor = OttoMotor(13, 14)             # Connectors 10 & 11
offsetL = 0                           # Calibration for left servo motor
offsetR = 0                           # Calibration for right servo motor

#OLED setup
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000) 
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

rotary = Rotary(18, 19, 26) # GPIO Pins for the encoder pins Connector 2. third is the button press switch Connector 4.

alarmtime = [0, 0, 0, 12, 0, 0, 0, 0]

lastbuttonpress = 0
delay = 60000
diff = 0
now = 0

#Global flag for the alarm
alarm = False

def do_sta_connect():
    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect("MRV_WiFi_Guest", "")
        print("Connecting to network ...")
        oled.fill(0)
        oled.text("Connecting to network...", 0, 0)
        oled.show()
        time.sleep(1)
        while not sta_if.isconnected():
            pass
    print("Connected. The MAC address is:", ubinascii.hexlify(sta_if.config('mac'), ':').decode().upper())
    print("The network values are:", sta_if.ifconfig())
    oled.fill(0)
    oled.text("Connected!", 0, 0)
    oled.show()
    time.sleep(1)

def rotary_changed(change):
    global alarmtime, lastbuttonpress
    if change == Rotary.ROT_CW:
        print("+5")
        alarmtime[5] += 5
        if alarmtime[5] >= 60:
            alarmtime[5] = 0
            alarmtime[4] = (alarmtime[4] + 1) % 24
    elif change == Rotary.ROT_CCW:
        print("-5")
        alarmtime[5] -= 5
        if alarmtime[5] < 0:
            alarmtime[5] = 55
            alarmtime[4] = (alarmtime[4] - 1) % 24
    elif change == Rotary.SW_PRESS:
        print('PRESS')
        lastbuttonpress = utime.ticks_ms()
    elif change == Rotary.SW_RELEASE:
        print('RELEASE')

rtc = RTC()

do_sta_connect()

# Attempt to set NTP time
try:
    ntptime.settime()
    utc_shift = 2
    tm_internal = utime.localtime(utime.mktime(utime.localtime()) + utc_shift * 3600)
    tm_internal = tm_internal[0:3] + (0,) + tm_internal[3:6] + (0,)
    rtc.datetime(tm_internal)
    print("NTP time set successfully")
except OSError as e:
    print("Failed to set NTP time:", e)

rotary.add_handler(rotary_changed)

while True:
    # Format the current datetime from RTC
    current_time = rtc.datetime()
    formatted_time = "{:2d}:{:02d}".format(
        current_time[4],  # Hour
        current_time[5]   # Minute
    )
    
    # Format time for alarm
    selectedtime = "{:2d}:{:02d}".format(
        alarmtime[4],  # Hour
        alarmtime[5]   # Minute
    )
    
    # Display the time on the OLED
    oled.fill(0)  # Clear the display
    oled.text("Wakey, wakey!", 0, 0)
    oled.text(selectedtime, 80, 20)
    oled.text(formatted_time, 0, 40)
    oled.show()
    
    print("Last: ", lastbuttonpress, "Now :", now,"Diff: ", diff)
    
    now = utime.ticks_ms()
    diff = utime.ticks_diff(now, lastbuttonpress)
    if current_time[4] == alarmtime[4] and current_time[5] == alarmtime[5] and diff > delay:
        oled.fill(0)
        oled.text("ALARM!", 0, 0)
        oled.show()
        buzzer.playEmoji("S_happy")
        time.sleep(1)
    
    time.sleep(.1)