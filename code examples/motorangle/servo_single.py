from machine import Pin
from machine import PWM
from time import sleep_ms

def map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)
    
class SERVO:
    def __init__(self, signal_pin):
        self.pwm = PWM(Pin(signal_pin), freq=50, duty=0)

    def rotate(self, angle):
        self.pwm.duty(map(angle, 0, 180, 23, 124))
        

servo = SERVO(signal_pin=13)

# The following lines of codes can be tested using the REPL:
# # To rotate the servo motor to 0 degrees
# servo.rotate(0)
# 
# # To rotate the servo motor to 90 degrees
# servo.rotate(90)
# 
# # To rotate the servo motor to 180 degrees
# servo.rotate(180)
# 
# # To rotate the servo from 0 to 180 degrees
# # by 10 degrees increment
for angle in range(0, 181, 10):
    servo.rotate(angle)
    print(angle)
    sleep_ms(500)
# # To rotate the servo from 180 to 0 degrees
# # by 10 degrees decrement
# for angle in range(180, -1, -10):
#     servo.rotate(angle)
#     print(angle)
#     sleep_ms(500)
