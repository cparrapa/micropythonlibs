import network, espnow, machine
from time import sleep
from machine import Pin, ADC, PWM, SoftI2C #importing classes
from neopixel import NeoPixel
from ottoneopixel import OttoNeoPixel
from ottoneopixel import OttoUltrasonic
from ottobuzzer import OttoBuzzer
from ottomotor import OttoMotor
from otto4wd import OttoMecanum

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  

# Initialize ESP-NOW
esp = espnow.ESPNow()
esp.active(True)

led = Pin(2, Pin.OUT)
ring = OttoNeoPixel(4, 13)  
ultrasonic = OttoUltrasonic(18, 19)

# Initialize the robot (adjust connector numbers if needed)
robot = OttoMecanum()

# Define a speed value (within -50 to +50)
speed = 30
duration = 2  # seconds

ring.fillAllRing(0, 255, 255)
ultrasonic.ultrasonicRGB2(0, 255, 255)

while True:
    _, msg = esp.recv()
    if msg:             # msg == None if timeout in recv()
        if msg == b'AOn':
            led.on()
            # Move forward
            print("Moving forward")
            ring.fillAllRing(0, 0, 255)
            ultrasonic.ultrasonicRGB2(0, 0, 255)
            robot.forward(speed)
            #sleep(duration)
        elif msg == b'AOff':
            led.off()
            # Stop
            print("Stopping")
            ring.fillAllRing(0, 0, 0)
            ultrasonic.ultrasonicRGB2(0, 0, 0)
            robot.stop()
        elif msg == b'Bon':
            # Move backward
            print("Moving backward")
            ring.fillAllRing(255, 0, 255)
            ultrasonic.ultrasonicRGB2(255, 0, 255)
            robot.backward(speed)
        elif msg == b'Boff':
            # Stop
            print("Stopping")
            ring.fillAllRing(0, 0, 0)
            ultrasonic.ultrasonicRGB2(0, 0, 0)
            robot.stop()
        elif msg == b'Con':
            # Crab left
            print("Crabbing left")
            ring.fillAllRing(0, 255, 0)
            ultrasonic.ultrasonicRGB2(0, 255, 0)
            robot.crab_left(speed)
        elif msg == b'Coff':
            # Stop
            print("Stopping")
            ring.fillAllRing(0, 0, 0)
            ultrasonic.ultrasonicRGB2(0, 0, 0)
            robot.stop()
        elif msg == b'Don':
            # Crab right
            print("Crabbing right")
            ring.fillAllRing(0, 255, 255)
            ultrasonic.ultrasonicRGB2(0, 255, 255)
            robot.crab_right(speed)
        elif msg == b'Doff':
            # Stop
            print("Stopping")
            ring.fillAllRing(0, 0, 0)
            ultrasonic.ultrasonicRGB2(0, 0, 0)
            robot.stop()
        elif msg == b'Eon':
            # Turn left
            print("Turning left")
            ring.fillAllRing(255, 0, 0)
            ultrasonic.ultrasonicRGB2(255, 0, 0)
            robot.turn_left(speed)
        elif msg == b'Eoff':
            # Stop
            print("Stopping")
            ring.fillAllRing(0, 0, 0)
            ultrasonic.ultrasonicRGB2(0, 0, 0)
            robot.stop()
        elif msg == b'Fon':
            # Turn right
            print("Turning right")
            ring.fillAllRing(255, 255, 0)
            ultrasonic.ultrasonicRGB2(255, 255, 0)
            robot.turn_right(speed)
        elif msg == b'Foff':
            # Stop
            print("Stopping")
            ring.fillAllRing(0, 0, 0)
            ultrasonic.ultrasonicRGB2(0, 0, 0)
            robot.stop()
        elif msg == b'Gon':
            print("Diagonal left")
            ring.fillAllRing(255, 255, 255)
            ultrasonic.ultrasonicRGB2(255, 255, 255)
            robot.diag_left(speed)
        elif msg == b'Hon':
            print("Diagonal right")
            ring.fillAllRing(50, 50, 50)
            ultrasonic.ultrasonicRGB2(50, 50, 50)
            robot.diag_right(speed)
        else:
            print("Unknown message!")

