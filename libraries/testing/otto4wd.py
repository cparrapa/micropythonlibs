# otto 4wd class v0.0 27 Aug 2024 Alex Etchells
# A class to control HP Otto with 4 wheel drive and a subclass for mecanum wheels
# The constructor takes the connector number (rather than Pin)
# Speed values should be in the range -50 to + 50
from ottomotor import OttoMotor

"""
Constructor takes connector numbers for the four servos
"""
class Otto4WD:
    def __init__(self, connectorRL = 10, connectorRR = 11, connectorFL = 8, connectorFR = 9):
        connectorPin = [None,None,None,None,26,4,32,33,27,15,14,13] #GPIO pin for the 3pin connectors (4 to 11)
        self.rearMotors = OttoMotor(connectorPin[connectorRR], connectorPin[connectorRL])
        self.frontMotors = OttoMotor(connectorPin[connectorFR], connectorPin[connectorFL])
        #servo duty values
        self.loDutyRL = 20
        self.hiDutyRL = 130
        self.loDutyRR = 20
        self.hiDutyRR = 130
        self.loDutyFL = 20
        self.hiDutyFL = 130
        self.loDutyFR = 20
        self.hiDutyFR = 130
        self.dutyRangeRL = int((self.hiDutyRL - self.loDutyRL)/2)  #halved because plus and minus around mid value
        self.dutyRangeRR = int((self.hiDutyRR - self.loDutyRR)/2)
        self.dutyRangeFL = int((self.hiDutyFL - self.loDutyFL)/2)
        self.dutyRangeFR = int((self.hiDutyFR - self.loDutyFR)/2)
        self.midDutyRL = self.loDutyRL + self.dutyRangeRL
        self.midDutyRR = self.loDutyRR + self.dutyRangeRR
        self.midDutyFL = self.loDutyFL + self.dutyRangeFL
        self.midDutyFR = self.loDutyFR + self.dutyRangeFR
        #if we need further fine tuning
        self.ftForwardRL = 0
        self.ftReverseRL = 0
        self.ftForwardRR = 0
        self.ftReverseRR = 0
        self.ftForwardFL = 0
        self.ftReverseFL = 0
        self.ftForwardFR = 0
        self.ftReverseFR = 0
        
    """
    Probably don't need to change these, the servos I've looked at seem pretty consistent
    """
    def setDutyRanges(self,loRL,hiRL,loRR,hiRR,loFL,hiFL,loFR,hiFR):
        #servo duty values
        self.loDutyRL = loRL
        self.hiDutyRL = hiRL
        self.loDutyRR = loRR
        self.hiDutyRR = hiRR
        self.loDutyFL = loFL
        self.hiDutyFL = hiFL
        self.loDutyFR = loFR
        self.hiDutyFR = hiFR          
        self.dutyRangeRL = int((self.hiDutyRL - self.loDutyRL)/2)  
        self.dutyRangeRR = int((self.hiDutyRR - self.loDutyRR)/2)
        self.dutyRangeFL = int((self.hiDutyFL - self.loDutyFL)/2)
        self.dutyRangeFR = int((self.hiDutyFR - self.loDutyFR)/2)
        self.midDutyRL = self.loDutyRL + self.dutyRangeRL
        self.midDutyRR = self.loDutyRR + self.dutyRangeRR
        self.midDutyFL = self.loDutyFL + self.dutyRangeFL
        self.midDutyFR = self.loDutyFR + self.dutyRangeFR

    """
    Slight adjustments are recommended to achieve straight line movement
    """
    def setFineTune(self,forwardRL,backwardRL,forwardRR,backwardRR,forwardFL,backwardFL,forwardFR,backwardFR):
        self.ftForwardRL = forwardRL
        self.ftReverseRL = backwardRL
        self.ftForwardRR = forwardRR
        self.ftReverseRR = backwardRR
        self.ftForwardFL = forwardFL
        self.ftReverseFL = backwardFL
        self.ftForwardFR = forwardFR
        self.ftReverseFR = backwardFR  

    """ speed -50 to +50 """
    def motorRL(self,speed):
        if speed < 0:
            speed = speed - self.ftReverseRL
        if speed > 0:
            speed = speed + self.ftForwardRL
        #speed 0 to duty range
        if speed < 0 - self.dutyRangeRL:
            speed = 0 - self.dutyRangeRL
        if speed > self.dutyRangeRL:
            speed = self.dutyRangeRL
        #left motors high duty is forward
        self.rearMotors.leftServo.duty(self.midDutyRL + speed)
            
    def motorRR(self,speed):
        if speed < 0:
            speed = speed - self.ftReverseRR
        if speed > 0:
            speed = speed + self.ftForwardRR
        #speed 0 to duty range
        if speed < 0 - self.dutyRangeRR:
            speed = 0 - self.dutyRangeRR
        if speed > self.dutyRangeRR:
            speed = self.dutyRangeRR
        #right motors low duty is forward
        self.rearMotors.rightServo.duty(self.midDutyRR - speed)

    def motorFL(self,speed):
        if speed < 0:
            speed = speed - self.ftReverseFL
        if speed > 0:
            speed = speed + self.ftForwardFL
        #speed 0 to duty range
        if speed < 0 - self.dutyRangeFL:
            speed = 0 - self.dutyRangeFL
        if speed > self.dutyRangeFL:
            speed = self.dutyRangeFL
        #left motors high duty is forward
        self.frontMotors.leftServo.duty(self.midDutyFL + speed)
            
    def motorFR(self,speed):
        if speed < 0:
            speed = speed - self.ftReverseFR
        if speed > 0:
            speed = speed + self.ftForwardFR
        #speed 0 to duty range
        if speed < 0 - self.dutyRangeFR:
            speed = 0 - self.dutyRangeFR
        if speed > self.dutyRangeFR:
            speed = self.dutyRangeFR
        #right motors low duty is forward
        self.frontMotors.rightServo.duty(self.midDutyFR - speed)          

    def setThrottles(self,rl,rr,fl,fr):    
        self.motorRL(int(rl))
        self.motorRR(int(rr))
        self.motorFL(int(fl))
        self.motorFR(int(fr))      
    
    def stop(self):
        #self.setThrottles(0,0,0,0)
        #hard code duty to 0 to avoid any confusion caused by user defined range
        self.rearMotors.leftServo.duty(0)
        self.rearMotors.rightServo.duty(0)
        self.frontMotors.leftServo.duty(0)
        self.frontMotors.rightServo.duty(0)

    def forward(self,speed):
        self.setThrottles(speed, speed, speed, speed)

    def backward(self,speed):
        self.setThrottles(-speed, -speed, -speed, -speed)

    def turn_left(self,speed):
        self.setThrottles(-speed, speed, -speed, speed)

    def turn_right(self,speed):
        self.setThrottles(speed, -speed, speed, -speed)

    def curve_left(self,speed, biasPcent=20):
        self.setThrottles(speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100)

    def curve_right(self,speed, biasPcent=20):
        self.setThrottles(speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100, speed * (100 + biasPcent) / 100, speed * (100 - biasPcent) / 100)


class OttoMecanum(Otto4WD):
    def __init__(self, connectorRL = 10, connectorRR = 11, connectorFL = 8, connectorFR = 9):
        super().__init__(connectorRL, connectorRR, connectorFL, connectorFR)
        
    def crab_left(self,speed):
        self.setThrottles(speed, -speed, -speed, speed)

    def crab_right(self,speed):
        self.setThrottles(-speed, speed, speed, -speed)

    def diag_left(self,speed):
        self.setThrottles(speed, 0, 0, speed)

    def diag_right(self,speed):
        self.setThrottles(0, speed, speed, 0)
