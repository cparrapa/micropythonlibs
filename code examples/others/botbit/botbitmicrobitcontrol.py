from microbit import *
import radio
radio.on()
radio.config(length=8, queue=3, channel=79, power=7, 
             address=0x44773311, group=0x1B, data_rate=radio.RATE_250KBIT)
    
msg = bytearray(8)
x = 0
y = 0
z = 0
a = 0
while True:
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    if button_a.is_pressed():
        a = a | 0x01
    else:
        a = a & 0xFE
    if button_b.is_pressed():
        a = a | 0x02
    else:
        a = a & 0xFD
    x = x + 10000;
    msg[0] = int(x / 256)
    msg[1] = x % 256
    y = y + 10000;
    msg[2] = int(y / 256)
    msg[3] = y % 256
    z = z + 10000;
    msg[4] = int(z / 256)
    msg[5] = z % 256
    msg[6] = int(a / 256)
    msg[7] = a % 256
    radio.send_bytes(msg)
    sleep(100)