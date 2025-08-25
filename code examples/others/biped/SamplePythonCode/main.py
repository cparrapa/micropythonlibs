import network
import utime
import uasyncio as asyncio
from machine import Pin
import Config
import LedAction
import ServoAction
import ServoAction2


""" For save local log when you trouble. """

# import os
# logfile = open('log.txt', 'a')
# os.dupterm(logfile)


""" For Servo No.1 Test example https://github.com/KitronikLtd/Kitronik-Pico-Simply-Servos-MicroPython/tree/main/Examples """

# from SimplyServos import KitronikSimplyServos
# servos = KitronikSimplyServos()
# for count in range(2):
#     servos.goToPosition(1,0)
#     utime.sleep(1)
#     servos.goToPosition(1,180)
#     utime.sleep(1)


# First lighting and Servo Init Position

LedAction.led_Up.value(1)
LedAction.led_Under.value(1)

ServoAction.InitPosition()



# HTML for Controller webpage

html = """<!DOCTYPE html><html>
<head> <title>Remote Controller for EasyPico</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="icon" href="data:,">
<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}
.buttonGreen { background-color: #a0c238; border: 2px solid #000000;; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-weight:bold; }
.buttonBlue { background-color: #65ace4; border: 2px solid #000000;; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 18px; margin: 4px 2px; cursor: pointer; font-weight:bold; }
.buttonBlack { background-color: #000000; border: 2px solid #000000;; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer; font-weight:bold; }
.buttonWhite { background-color: #FFFFFF; border: 2px solid #000000;; color: black; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer; font-weight:bold; }
.buttonGlay { background-color: #808080; border: 2px solid #000000;; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer; font-weight:bold; }
.buttonSilver { background-color: #c0c0c0; border: 2px dotted #000000;; color: black; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer; }
.buttonRed { background-color: #d11d53; border: 2px solid #000000;; color: white; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; font-weight:bold; }
.buttonYellow { background-color: #ffff00; border: 2px solid #000000;; color: black; padding: 15px 25px; text-align: center; text-decoration: none; display: inline-block; font-size: 12px; margin: 4px 2px; cursor: pointer; font-weight:bold; }
text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
</style></head>

<body><h2>EasyPico</h2>
<form>
<button class="buttonBlue" name="Servo" value="Forward" type="submit">Forward</button>
</form>
<form>
<button class="buttonSilver" name="Servo" value="Left" type="submit">Left_</button>
<button class="buttonSilver" name="Servo" value="Stop" type="submit">Stop</button> 
<button class="buttonSilver" name="Servo" value="Right" type="submit">Right</button>
</form>
<button class="buttonSilver" name="Servo" value="Back" type="submit">Back</button>
<p>"Left, Stop, Right, Back" is dummy</p>
<form>
<button class="buttonGreen" name="Servo" value="Exercise" type="submit">Exercise</button>
</form>

<h3>Head LED</h3>
<form>
<button class="buttonWhite" name="LED" value="ON" type="submit">ON</button>
<button class="buttonGlay" name="LED" value="BLINK" type="submit">BLINK</button>
<button class="buttonBlack" name="LED" value="OFF" type="submit">OFF</button>
</form>

<p>Last command issued was %s</p></body></html>
"""



# WIFI 

check_interval_sec = 0.25
wlan = network.WLAN(network.STA_IF)


async def connect_to_wifi():
    wlan.active(True)
    wlan.config(pm = 0xa11140)  # Disable powersave mode
    wlan.connect(Config.SSID,Config.Password)

    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        utime.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('WiFi connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])


# Remote Control

async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass
    
    # find() valid commands within the request
    request = str(request_line)
    cmd_on = request.find('LED=ON')
    cmd_blink = request.find('LED=BLINK')
    cmd_off = request.find('LED=OFF')
    Servo_Exercise = request.find('Servo=Exercise')
    Servo_Forward = request.find('Servo=Forward')
    print ('LED=ON => ' + str(cmd_on)) # show where the commands were found (-1 means not found)
    print ('LED=BLINK => ' + str(cmd_blink))
    print ('LED=OFF => ' + str(cmd_off))
    print ('Servo=Exercise => ' + str(Servo_Exercise))
    print ('Servo=Forward => ' + str(Servo_Forward))

    stateis = "" # Keeps track of the last command issued

    # Carry out a command if it is found (found at index: 8)
    if cmd_on == 8:
        stateis = "LED: ON"
        print(stateis)
        LedAction.control_led('on')
        
    elif cmd_blink == 8:
        stateis = "LED: BLINK"
        print(stateis)
        LedAction.control_led('blink')
        
    elif cmd_off == 8:
        stateis = "LED: OFF"
        print(stateis)
        LedAction.control_led('off')
        
    elif Servo_Exercise == 8:
        stateis = "Servo: Exercise"
        print(stateis)
        ServoAction.control_servo('Exercise')
        
    elif Servo_Forward == 8:
        stateis = "Servo: Forward"
        print(stateis)
        ServoAction2.control_servo2('Forward')

    response = html % stateis
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()

async def main():
    print('Connecting to WiFi...')
    asyncio.create_task(connect_to_wifi())

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))

    while True:
        await asyncio.sleep(check_interval_sec)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
