import math

"""
solvLinReg.py  v0.0  10 Nov 2025  Alex Etchells
use least squares regression to derive slope, intcpt
and rsq from a bunch of co-ords
"""
class SolvLinReg:
    
    def __init__(self):
        self.pointList = None
        self.numOfEntries = 0
        
    
    def AddPoints(self,x, y):
        if (x is None or y is None):
            return
        pointPair = (x,y)
        if self.numOfEntries == 0:
            self.pointList = [pointPair]
        else:
            self.pointList.append(pointPair)
        self.numOfEntries +=1
        
    def Slope(self): # get slope
        if (self.numOfEntries < 2): return 0
        return ((self.numOfEntries * self.getSxy()) - (self.getSx() * self.getSy())) / ((self.numOfEntries * self.getSxx()) - (self.getSx() * self.getSx()))
    
    
    def Intercept(self):  # get intercept    {
        if self.numOfEntries < 2: return 0
        return (self.getSy() - (self.Slope() * self.getSx())) / self.numOfEntries
 
    def RSquare(self):  # get rsquare,
        if self.numOfEntries < 2: return 0
        denom = (((self.numOfEntries * self.getSxx()) - (self.getSx() * self.getSx())) *
                        ((self.numOfEntries * self.getSyy()) - (self.getSy() * self.getSy())))
        denom = math.sqrt(denom)
        r = ((self.numOfEntries * self.getSxy()) - (self.getSx() * self.getSy())) / denom
        return r * r
    
    
    
    # helper methods
    def getSx(self):   # get sum of x        y
        Sx = 0
        for ppair in self.pointList:
            Sx += ppair[0]            
        return Sx

    def getSy(self):   # get sum of y
        Sy = 0
        for ppair in self.pointList:
            Sy += ppair[1]
        return Sy

    def getSxx(self):   # get sum of x*x
        Sxx = 0
        for ppair in self.pointList:
            Sxx += ppair[0] * ppair[0] # sum of x*x
        return Sxx
    
    def getSyy(self):   # get sum of y*y
        Syy = 0;
        for ppair in self.pointList:
            Syy += ppair[1] * ppair[1]    # sum of y*y
        return Syy

    def getSxy(self):   # get sum of x*y
        Sxy = 0;
        for ppair in self.pointList:
            Sxy += ppair[0] * ppair[1]    # sum of x*y
        return Sxy

