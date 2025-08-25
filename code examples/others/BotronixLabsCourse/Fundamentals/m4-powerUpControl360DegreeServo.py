from machine import Pin, PWM
import time

# Initialize PWM on GPIO 15
servo = PWM(Pin(1))
servo.freq(50)
led = Pin(25, Pin.OUT)

def clockwise():
    servo.duty_u16(8000)  # Forward (adjust value based on your servo)

def counterclockwise():
    servo.duty_u16(3000)  # Reverse (adjust as needed)

def stop():
    servo.duty_u16(5000)  # Neutral pulse to stop

# Loop to demonstrate motion
while True:
    led.value(1)
    
    print("Spinning Clockwise")
    clockwise()
    time.sleep(2)

    print("Stopping")
    stop()
    time.sleep(1)

    print("Spinning Counter-Clockwise")
    counterclockwise()
    time.sleep(2)

    print("Stopping")
    stop()
    time.sleep(1)


