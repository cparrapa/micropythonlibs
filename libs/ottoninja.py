# ottoninja v1 12.09.2024
from time import sleep               #importing sleep class
from machine import Pin, PWM
from ottomotor import Servo

class Ninja:
    def __init__(self, LL, RL, LF, RF): #(Left leg), (Right leg), (Left foot), (Right foot)
        self.leftlegServo=Servo()
        self.leftlegServo.attach(LL)
        self.rightlegServo=Servo()
        self.rightlegServo.attach(RL)
        self.leftfootServo=Servo()
        self.leftfootServo.attach(LF)
        self.rightfootServo=Servo()
        self.rightfootServo.attach(RF)
        
    def Rollset(self):
        self.leftlegServo.write(180)
        self.rightlegServo.write(0)
        
    def Roll(self, direction, speed):
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
        
    def Rollrotate(self, turn):
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
        
    def Rollstop(self):
        self.leftfootServo.write(90)
        self.rightfootServo.write(90)
        
    def Walkset(self):
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        
    def Walk(self, direction, speed):
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
        
    def Walkstop(self):
        self.leftfootServo.write(90)
        self.rightfootServo.write(90)
        self.leftlegServo.write(60)
        self.rightlegServo.write(120)