import time
import matatalab
import math
import audio
import drv_motion as motion

curX = 0
curY = 0
tarX = 0
tarY = 0
curVecX = 0
curVecY = 0
tarVecX = 0 
tarVecY = 0
tmpVecX = 0.0
tmpVecY = 0.0
curD = 0
tarD = 0
PI = 3.141592654
useHermit = 0
preCommand = "G1"

def initPosition():
    global curX
    global curY
    global curA
    global curB
    global curVecX
    global curVecY
    global curD
    curX = 0;
    curY = 0;
    curA = 0;
    curB = 0;
    curVecX = 1
    curVecY = 0
    curD = 0
    useHermit = 0

def prepareMove():
    global tarX
    global tarY
    global curX
    global curY
    global tarVecX
    global tarVecY
    global tmpVecX
    global tmpVecY
    global useHermit
    global curD
    global tarD
    dx = tarX - curX;
    dy = tarY - curY;
    distance = int(round(math.sqrt(dx*dx+dy*dy)));
    tarD = math.atan2(dy,dx);
    if(tarD > PI):
        tarD -= (2 * PI);
    elif(tarD < -PI):
        tarD += (2 * PI);
    if (distance < 1):
        return
    if(useHermit == 0):
        dAng = curD - tarD
        if(dAng > PI):
          dAng -= (2*PI);
        elif(dAng < -PI):
          dAng += (2*PI);
        angle = (dAng / (2 * PI)) * 360
        print("move_command- angle:%f, distance:%f" %(angle, distance))
        motion.move_raw_angle(angle, 60, 1)
        motion.move_raw_position(distance, 60, 1)
    else:
        print("useHermit move");
    curD = tarD;
    curX = tarX;
    curY = tarY;

def prepareTurn():
    global tarX
    global tarY
    global curX
    global curY
    global tarVecX
    global tarVecY
    global tmpVecX
    global tmpVecY
    global useHermit
    global curD
    global tarD

    if(tarD > PI):
        tarD -= (2 * PI);
    elif(tarD < -PI):
        tarD += (2 * PI);
    if(useHermit == 0):
        dAng = curD - tarD
        if(dAng > PI):
          dAng -= (2*PI);
        elif(dAng < -PI):
          dAng += (2*PI);
        angle = (dAng / (2 * PI)) * 360
        print("move_command- angle:%f" %(angle))
        motion.move_raw_angle(angle, 60, 1)
    else:
        print("useHermit move");
    curD = tarD;
    curX = tarX;
    curY = tarY;

def processGcode(line):
    global tarX
    global tarY
    global curX
    global curY
    global preCommand
    global tarD
    if("G100" in line):
        line_data = line.split(' ')
        for data in line_data:
            if("X" in data) or ("x" in data):
                curX = float(data[1:])
            elif("Y" in data) or ("y" in data):
                curY = float(data[1:])
    elif("G1 " in line):
        if(preCommand != "G1"):
            for i in range(5):
                audio.play_alto(i+1, 0.5);
        preCommand = "G1"
        line_data = line.split(' ')
        for data in line_data:
            if("X" in data) or ("x" in data):
                tarX = float(data[1:])
            elif("Y" in data) or ("y" in data):
                tarY = float(data[1:])
        prepareMove()
    elif("G0 " in line):
        if(preCommand != "G0"):
            for i in range(5):
                audio.play_alto(6-i, 0.5);
        preCommand = "G0"
        line_data = line.split(' ')
        for data in line_data:
            if("X" in data) or ("x" in data):
                tarX = float(data[1:])
            elif("Y" in data) or ("y" in data):
                tarY = float(data[1:])
        prepareMove()
    elif("G28" in line):
        tarX = 0
        tarY = 0
        initPosition()
        prepareMove()
        #initPosition()
    elif("G200" in line):
        tarD = 0
        prepareTurn()
