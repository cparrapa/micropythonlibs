import machine, time
from machine import Pin, ADC, PWM

encoder = Pin(16, Pin.IN, Pin.PULL_UP)

channelA = Pin(16, Pin.IN)
channelB = Pin(17, Pin.IN)

stateA = 0
stateB = 0
laststateA = stateA

currenttime = 0
lasttime = 0

response = 10

def encoder_callback(pin):
    
    global laststateA
    global lasttime
    global currenttime
    
    stateA = channelA.value()
    stateB = channelB.value()
    
    currenttime = time.ticks_ms()
    
    if time.ticks_diff(currenttime, lasttime) > response:
        #Logic for recognizing clock and counter clock wise rotation
            #Sometimes channels A and B change at the same time/ESP doesn't capture this their phase difference
            #For this reason we'll watch both stateA and stateB
        if laststateA == stateA:
            print(1)
        else:
            print(0)
        
    lasttime = currenttime
    laststateA = stateA
    laststateB = stateB
    
while True:
    channelB.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_callback)
    channelA.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=encoder_callback)