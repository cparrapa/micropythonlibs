import machine                       #importing machine libraries
from time import sleep               #importing sleep class
from machine import Pin, PWM         #importing Pin and PWM classes
from ottowalk&roll import Ninja

ninja = Ninja(27, 15, 14, 13)         # Connector 8 (Left leg), 9(Right leg), 10(Left foot), 11(Right foot)

while True:
    ninja.Walkset()
    sleep(0.5)
    ninja.Walk(1,3) #forward, fast
    ninja.Walk(1,3)
    sleep(0.5)
    ninja.Walk(-1,3) #backward, fast
    ninja.Walk(-1,3)
    sleep(0.5)
    ninja.Walkset()
    ninja.Rollset()
    sleep(0.5)
    ninja.Roll(-1, 3) #backward, fast
    ninja.Roll(-1, 3)
    sleep(1)
    ninja.Roll(1, 3) #forward, fast
    ninja.Roll(1, 3)
    sleep(1)
    ninja.Rollstop()
    sleep(0.5)
    ninja.Rollrotate(1) #right
    ninja.Rollrotate(1)
    ninja.Rollrotate(-1) #left
    ninja.Rollrotate(-1)
    sleep(1)
