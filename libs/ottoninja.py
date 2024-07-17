# ottoninja v0 28.05.2024
import time
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
        self.leftlegServo.write(0)
        self.rightlegServo.write(180)
        
    def Roll(self, direction, speed):
        if(direction == -1): #backward
            if(speed == 1):
                leftSpeed = 80
            elif(speed == 2):
                leftSpeed = 40
            elif(speed == 3):
                leftSpeed = 0

            if(speed == 1):
                rightSpeed = 100
            elif(speed == 2):
                rightSpeed = 140
            elif(speed == 3):
                rightSpeed = 180
                
        else: #(direction == 1) forward
            if(speed == 1):
                leftSpeed = 100
            elif(speed == 2):
                leftSpeed = 140
            elif(speed == 3):
                leftSpeed = 180
            
            if(speed == 1):
                rightSpeed = 80
            elif(speed == 2):
                rightSpeed = 40
            elif(speed == 3):
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
        time.sleep(1)
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
                leftSpeed = 80
            elif(speed == 2):
                leftSpeed = 40
            elif(speed == 3):
                leftSpeed = 0

            if(speed == 1):
                rightSpeed = 100
            elif(speed == 2):
                rightSpeed = 140
            elif(speed == 3):
                rightSpeed = 180
                
        else: #(direction == 1) forward
            if(speed == 1):
                leftSpeed = 100
            elif(speed == 2):
                leftSpeed = 140
            elif(speed == 3):
                leftSpeed = 180
            
            if(speed == 1):
                rightSpeed = 80
            elif(speed == 2):
                rightSpeed = 40
            elif(speed == 3):
                rightSpeed = 0
                
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        time.sleep(1)
        self.rightlegServo.write(107)
        self.leftlegServo.write(125)
        time.sleep(1)
        self.rightfootServo.write(125)
        time.sleep(1)
        self.rightfootServo.write(90)
        time.sleep(1)
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        time.sleep(1)
        self.rightlegServo.write(46)
        self.leftlegServo.write(54)
        time.sleep(1)
        self.leftfootServo.write(55)
        time.sleep(1)
        self.leftfootServo.write(90)
        time.sleep(1)
        self.leftlegServo.write(90)
        self.rightlegServo.write(90)
        
    def Walkstop(self):
        self.leftfootServo.write(90)
        self.rightfootServo.write(90)
        self.leftlegServo.write(60)
        self.rightlegServo.write(120)


