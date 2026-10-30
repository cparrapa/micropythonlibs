# otto 3wd class v0.0 11 November 2025
# Alex Etchells
# A class to control HP Otto with 3 Omni Wheels
#
# The constructor takes the connector number (rather than Pin)
#
# Speed values should be in the range -50 to + 50
#
from machine import Pin, PWM
import math

"""
Constructor takes connector numbers for the three 
Left, Right, Back
"""
class Otto3WD:
    def __init__(self, connectorL = 10, connectorR = 11, connectorB = 8, ):
        connectorPin = [None,None,None,None,26,4,32,33,27,15,14,13] #GPIO pin for the 3pin connectors (4 to 11)
              
        self.rightServo = PWM(Pin(connectorPin[connectorR]))
        self.rightServo.freq(50)
        self.leftServo = PWM(Pin(connectorPin[connectorL]))
        self.leftServo.freq(50)
        self.backServo = PWM(Pin(connectorPin[connectorB]))
        self.backServo.freq(50)

        #servo duty values
        self.loDutyL = 20
        self.hiDutyL = 130
        self.loDutyR = 20
        self.hiDutyR = 130
        self.loDutyB = 20
        self.hiDutyB = 130
        
        self.dutyRangeL = int((self.hiDutyL - self.loDutyL)/2)  #halved because plus and minus around mid value
        self.dutyRangeR = int((self.hiDutyR - self.loDutyR)/2)
        self.dutyRangeB = int((self.hiDutyB - self.loDutyB)/2)
        
        self.midDutyL = self.loDutyL + self.dutyRangeL
        self.midDutyR = self.loDutyR + self.dutyRangeR
        self.midDutyB = self.loDutyB + self.dutyRangeB
        
        #if we need further fine tuning
        self.ftForwardL = 0
        self.ftReverseL = 0
        self.ftForwardR = 0
        self.ftReverseR = 0
        self.ftForwardB = 0
        self.ftReverseB = 0

    """
    Slight adjustments are recommended to achieve straight line movement
    """
    def setFineTune(self,forwardL,backwardL,forwardR,backwardR,forwardB,backwardB):
        self.ftForwardL = forwardL
        self.ftReverseL = backwardL
        self.ftForwardR = forwardR
        self.ftReverseR = backwardR
        self.ftForwardB = forwardB
        self.ftReverseB = backwardB

    """ speed -50 to +50 """
    def motorL(self,speed):
        if speed < 0:
            speed = speed - self.ftReverseL
        if speed > 0:
            speed = speed + self.ftForwardL
        #speed 0 to duty range
        if speed < 0 - self.dutyRangeL:
            speed = 0 - self.dutyRangeL
        if speed > self.dutyRangeL:
            speed = self.dutyRangeL
        #left motors high duty is forward
        self.leftServo.duty(self.midDutyL + speed)
            
    def motorR(self,speed):
        if speed < 0:
            speed = speed - self.ftReverseR
        if speed > 0:
            speed = speed + self.ftForwardR
        #speed 0 to duty range
        if speed < 0 - self.dutyRangeR:
            speed = 0 - self.dutyRangeR
        if speed > self.dutyRangeR:
            speed = self.dutyRangeR
        #right motors high duty is forward
        self.rightServo.duty(self.midDutyR + speed)

    def motorB(self,speed):
        if speed < 0:
            speed = speed - self.ftReverseB
        if speed > 0:
            speed = speed + self.ftForwardB
        #speed 0 to duty range
        if speed < 0 - self.dutyRangeB:
            speed = 0 - self.dutyRangeB
        if speed > self.dutyRangeB:
            speed = self.dutyRangeB
        #back motor high duty is forward
        self.backServo.duty(self.midDutyB + speed)

    def setThrottles(self,left,right,back):
        print("L R B",left,right,back)
        self.motorL(int(left))
        self.motorR(int(right))
        self.motorB(int(back))      
    
    def stop(self):
        #hard code duty to 0 to avoid any confusion caused by user defined range
        self.leftServo.duty(0)
        self.rightServo.duty(0)
        self.backServo.duty(0)

    def Motor_Control(self,speed, dir_angle, angular_v):
        
        print(speed, dir_angle, angular_v)
        
        vx = -speed * math.sin(dir_angle * (math.pi / 180))
        vy = speed * math.cos(dir_angle * (math.pi / 180))
        vb = -vx + angular_v
        vr = 0.5 * vx - math.sqrt(3) / 2 * vy + angular_v
        vl = 0.5 * vx + math.sqrt(3) / 2 * vy + angular_v
        self.setThrottles(vl,vr,vb)

    def forward(self,speed):
        self.Motor_Control(speed, 0, 0)

    def backward(self,speed):
        self.Motor_Control(-speed, 0, 0)

    def turn_left(self,speed):
        self.setThrottles(-speed, -speed, -speed)

    def turn_right(self,speed):
        self.setThrottles(speed, speed, speed)

    """  def curve_left(self,speed, biasPcent=20):
        self.setThrottles(speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100)

    def curve_right(self,speed, biasPcent=20):
        self.setThrottles(speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100)
    """

    def crab_left(self,speed):
        self.Motor_Control(speed, 90, 0)

    def crab_right(self,speed):
        self.Motor_Control(speed, -90, 0)

    def diag_left(self,speed):
        self.Motor_Control(speed, 45, 0)

    def diag_right(self,speed):
        self.Motor_Control(speed, -45, 0)

        
