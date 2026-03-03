# ottowalkroll v2.1 27.02.2025
from time import sleep               #importing sleep class
from machine import Pin, PWM
from ottomotor import Servo

class Ninja:
    def __init__(self, LL, RL, LF, RF): #(Left leg), (Right leg), (Left foot), (Right foot)
        self.leftlegServo=Servo()
        self.leftlegServo.attach(LL) # angle servo
        self.rightlegServo=Servo()
        self.rightlegServo.attach(RL) # angle servo
        self.leftfootServo=Servo()
        self.leftfootServo.attach(LF) # wheel servo
        self.rightfootServo=Servo()
        self.rightfootServo.attach(RF) # wheel servo
        
    def rollset(self):
        self.leftlegServo.write(180)
        self.rightlegServo.write(0)
        sleep(0.2)
        
    def roll(self, direction, speed):
        if(direction == -1): #backward
            if(speed == 1): #slow
                leftSpeed = 60
                rightSpeed = 110
            elif(speed == 2): #normal
                leftSpeed = 40
                rightSpeed = 140
            elif(speed == 3): #fast
                leftSpeed = 0
                rightSpeed = 180
                
        else: #(direction == 1) forward
            if(speed == 1):
                leftSpeed = 115
                rightSpeed = 70
            elif(speed == 2):
                leftSpeed = 140
                rightSpeed = 40
            elif(speed == 3):
                leftSpeed = 180
                rightSpeed = 0
                
        self.leftfootServo.write(leftSpeed)
        self.rightfootServo.write(rightSpeed)
        
    def rollrotate(self, turn):
        if(turn == -1): #left
            leftSpeed = 0
            rightSpeed = 0

        elif(turn == 1): #right
            leftSpeed = 180
            rightSpeed = 180
            
        self.leftfootServo.write(leftSpeed)
        self.rightfootServo.write(rightSpeed)
        sleep(1)
        self.leftfootServo.write(90)
        self.rightfootServo.write(90)
        
    def rollstop(self):
        self.leftfootServo.write(90)
        self.rightfootServo.write(90)
        sleep(0.2)
        
    def walkset(self):
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        sleep(0.2)
        
    def walk(self, direction, speed):
        if(direction == -1): #backward
            if(speed == 1):
                leftSpeed = 70
                rightSpeed = 120
                delay = 1
            elif(speed == 2):
                leftSpeed = 50
                rightSpeed = 140
                delay = 0.5
            elif(speed == 3):
                leftSpeed = 30
                rightSpeed = 160
                delay = 0.3
                
        else: #(direction == 1) forward
            if(speed == 1):
                leftSpeed = 120
                rightSpeed = 70
                delay = 1
            elif(speed == 2):
                leftSpeed = 140
                rightSpeed = 50
                delay = 0.5
            elif(speed == 3):
                leftSpeed = 160
                rightSpeed = 30
                delay = 0.3
                
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        sleep(delay)
        self.rightlegServo.write(150)
        self.leftlegServo.write(120)
        sleep(delay)
        self.leftfootServo.write(leftSpeed)
        sleep(0.6)
        self.leftfootServo.write(90)
        sleep(delay)
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        sleep(delay)
        self.rightlegServo.write(60)
        self.leftlegServo.write(30)
        sleep(delay)
        self.rightfootServo.write(rightSpeed)
        sleep(0.6)
        self.rightfootServo.write(90)
        sleep(delay)
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        sleep(0.2)
        
    def walkstop(self):
        self.leftfootServo.write(90)
        self.rightfootServo.write(90)
        self.leftlegServo.write(60)
        self.rightlegServo.write(120)
        sleep(0.2)
        
class Arms:
    def __init__(self, LA, RA): #(Left arm), (Right arm)
        self.leftarm=Servo()
        self.leftarm.attach(LA)
        self.rightarm=Servo()
        self.rightarm.attach(RA)
        
    def move(self, turn, direction):
        if(turn == "left"):
            if(direction == "up"):
                leftAngle = 0
            elif(direction == "center"):
                leftAngle = 60
            elif(direction == "down"):
                leftAngle = 120

        elif(turn == "right"):
            if(direction == "up"):
                rightAngle = 120
            elif(direction == "center"):
                rightAngle = 60
            elif(direction == "down"):
                rightAngle = 0
            
        elif(turn == "both"):
            if(direction == "up"):
                leftAngle = 0
                rightAngle = 120
            elif(direction == "center"):
                leftAngle = 60
                rightAngle = 60
            elif(direction == "down"):
                leftAngle = 120
                rightAngle = 0
            
        sleep(0.3)
        self.leftarm.write(leftAngle)
        sleep(0.1)
        self.rightarm.write(rightAngle)
        sleep(0.3)