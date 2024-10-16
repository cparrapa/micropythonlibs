import machine, time, network, ubinascii, utime, ntptime
from time import sleep            # importing sleep class
from machine import Pin, ADC, PWM, I2C, SoftI2C # importing Pin, ADC, PWM and I2C classes
from ottobuzzer import OttoBuzzer
from machine import RTC
from ssd1306 import SSD1306_I2C  # Make sure you have this library
 
led = Pin(2, Pin.OUT)                 # Built in LED
buzzer = OttoBuzzer(25)               # Built in Buzzer
#OLED setup
i2c = I2C(scl=Pin(18), sda=Pin(19), freq=400000)  # Connector 1
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

alarmtime = [0, 0, 0, 12, 0, 0, 0, 0]
lastbuttonpress = 0
delay = 60000
diff = 0
now = 0
scroll = 5
 
def do_sta_connect():
    global sta_if
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        sta_if.active(True)
        sta_if.connect("insert wifi name here", "inser wifi password here")
        print("Connecting to network ...")
        oled.fill(0)
        oled.text("Connecting to", 0, 0)
        oled.text("network...", 0, 10)
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
    #print("Last: ", lastbuttonpress, "Now :", now,"Diff: ", diff)
    now = utime.ticks_ms()
    diff = utime.ticks_diff(now, lastbuttonpress)
    if current_time[4] == alarmtime[4] and current_time[5] == alarmtime[5] and diff > delay:
        oled.fill(0)
        oled.text("ALARM!", 0, 0)
        oled.show()
        buzzer.playEmoji("S_happy")
        time.sleep(1)
    if current_time[4] < 6 or current_time[4] > 21:
        if diff > delay/100:
            oled.contrast(1)
        else:
            oled.contrast(255)
    time.sleep(.1)
 