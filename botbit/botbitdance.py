from microbit import *
import music
import math
servo_pos = bytearray([0, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC, 0x05, 0xDC])
def setServo(servo, angle):
    "set the servo angel"
    a = (1.5 + angle/90) * 1000
    servo_pos[servo*2 + 1] = int(a / 256)
    servo_pos[servo*2 + 2] = int(a % 256)
def updatePosition():
    servo_pos[0] = 0
    i2c.write(0x2A, servo_pos)     
def getDistance():
    i2c.write(0x0b, bytearray([1]))
    temp=i2c.read(0x0B,2)
    dis =(temp[0]+temp[1]*256)/10
    return dis
inc = 0
phase_start=[0, 0, 0, 0]
phase=[0, 0, 0, 0]
offset=[0, 0, 0, 0]
amplitude=[0, 0, 0, 0]
t = 0
def refresh():
    global t, phase, inc, amplitude, phase_start
    if (running_time() - t) > 50:
        t = running_time()
        for i in range(0, 4):
            pos = round(amplitude[i]*math.sin(phase[i] + phase_start[i]) + offset[i])
            setServo(i, pos)
            phase[i] = phase[i] + inc
        updatePosition()
def action(A, O, DIFF, T, steps):
    global inc, amplitude, phase_start, offset
    t2 = 0
    inc = 2*math.pi/(T/50)
    for i in range(0, 4):
        amplitude[i] = A[i]
        phase_start[i] = DIFF[i]
        offset[i] = O[i]
    cycle = int(steps)
    t2 = running_time() + T*cycle
    while (running_time() < t2):
        refresh()
    for i in range(0, 4):
        amplitude[i] = A[i]
        phase_start[i] = DIFF[i]
        offset[i] = O[i]
    # move the servo
    t2 = running_time() + T*(steps - cycle)
    while (running_time() < t2):
        refresh()
def walking(steps, T=1000, dir=1):
    AMP = (30, 30, 20, 20)
    OFFSET = (0, 0, 4, -4)   
    DIFF = (0, 0, -math.pi/2 * dir, -math.pi/2 * dir)
    action(AMP, OFFSET, DIFF, T, steps)
    return 
def turn(steps, T=2000, dir=1):
    OFFSET = [0, 0, 4, -4]   
    DIFF = (0, 0, -math.pi/2 * dir, -math.pi/2 * dir)
    if dir == 1:
        AMP = (30, 10, 20, 20)
    else:
        AMP = (10, 30, 20, 20)
    action(AMP, OFFSET, DIFF, T, steps)
    return 
def moonwalker(steps, T=900, h=20, dir=1):
    'Moonwalker. Otto moves like Michael Jackson'
    AMP = [0, 0, h, h]
    OFFSET = [0, 0, h/2 + 2, -h/2 -2]   
    DIFF = [0, 0, math.pi/180*dir*-90, math.pi/180*dir*-150]
    action(AMP, OFFSET, DIFF, T, steps)
    return 
def crusaito(steps, T, h, dir):
    AMP = [25, 25, h, h]
    OFFSET = [0, 0, h/2+ 4, -h/2 - 4]   
    DIFF = [90, 90, 0, math.pi/180*dir*-60]
    action(AMP, OFFSET, DIFF, T, steps)
def flapping(steps, T, h, dir):
    AMP = [12, 12, h, h]
    OFFSET = [0, 0, h-10, -h+10]   
    DIFF = [0, math.pi/180*180, math.pi/180*dir*-90, math.pi/180*dir*90]
    action(AMP, OFFSET, DIFF, T, steps)
    return    
servo_position = [0, 0, 0, 0]
servo_increment = [0, 0, 0, 0]
def moveServos(time, servo_target):
    if time > 20:
        for i in range(0, 4):
            servo_increment[i] = (servo_target[i] - servo_position[i])/(time/20)       
        final_time = running_time() + time;
        iteration = 1
        while running_time() < final_time:
            partial_time = running_time()+20
            for i in range(0, 4):
                setServo(i, servo_position[i]+iteration*servo_increment[i])
            updatePosition()
            while running_time() < partial_time:
                pass
            iteration = iteration+1
    else:
        for i in range(0, 4):
            setServo(i, servo_target[i])
        updatePosition()
    for i in range(0, 4):
        servo_position[i] = servo_target[i]
    return 
def jump(T):
    up = [0, 0, 45, -45]
    moveServos(T, up)
    down = [0, 0, 0, 0]
    moveServos(T, down)
    return
def home():
    for i in range(0, 4):
        setServo(i, 0)
        servo_position[i] = 0
    updatePosition()
    
display.off()
home()
while True:
    walking(5, 1500, 1)
    walking(5, 1500, -1)
    music.play(music.BA_DING)
    moonwalker(5, 1000, 25, 1)
    moonwalker(5, 1000, 25, -1)    
    music.play(music.BADDY)
    crusaito(8, 1000, 15, 1)
    crusaito(8, 1000, 15, -1)
    crusaito(4, 2000, 15, 1)
    crusaito(4, 2000, 15, -1)  
    music.play(music.NYAN)
    flapping(5, 1500, 15, 1)
    flapping(5, 1500, 15, -1)
    music.play(music.BIRTHDAY)