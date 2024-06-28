import Pin, machine

channelA = Pin(16, Pin.IN, Pin.OUT)
channelB = Pin(17, Pin.IN, Pin.OUT)

while True:
    print("A", channelA.value(), "B", channelB.value())
    sleep.time(.01)