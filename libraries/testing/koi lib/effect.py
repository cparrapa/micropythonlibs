from time import sleep

__version__ = "1.0.4"

def breath(neopix):
    # 缓慢变亮
    x=0
    while not (x > 255):
        neopix.setColorAll((x,x,0))
        neopix.update()
        x += 3
        sleep(0.05)
    x = 255
    # 变暗
    while not (x < 0):
        neopix.setColorAll((x,x,0))
        neopix.update()
        x += -3
        sleep(0.05)
    


def brighter(neopix):
    x=0
    while not (x > 255):
        neopix.setColorAll((x,x,0))
        neopix.update()
        x += 5
        sleep(0.03)

def dimmer(neopix):
    x = 255
    while not (x < 0):
        neopix.setColorAll((x,x,0))
        neopix.update()
        x += -5
        sleep(0.03)


def flow(neopix):
    x=0
    while not (x >= len(neopix.np)):
        neopix.setColor(x, (255, 255, 255))
        x += 1
        neopix.update()
        sleep(0.05)
    neopix.setColorAll((0,0,0))
    neopix.update()


def rainbow(neopix):

    rainbow_color = [[255, 0, 0], [255, 165, 0], [255, 255, 0], [0, 255, 0], [0, 127, 255], [0, 0, 255], [139, 0, 255]]
    for i in range(len(neopix.np)):
        current_color = rainbow_color[i % 7]
        neopix.setColor(i, (current_color[0], current_color[1], current_color[2]))
    neopix.update()
    sleep(0.3)


def firefly(neopix):
    x=0
    while not (x > 255):
        neopix.setColorAll((x,x,0))
        neopix.update()
        x += 5
        sleep(0.03)
    sleep(2)
    x = 255
    while not (x < 0):
        neopix.setColorAll((x,x,0))
        neopix.update()
        x += -5
        sleep(0.03)


def blink(neopix):
    for count in range(3):
        neopix.setColorAll(255, 0, 0)
        neopix.update()
        sleep(0.2)
        neopix.setColorAll(0, 0, 0)
        neopix.update()
        sleep(0.2)


def heartbeat(neopix):
    x = 0
    for count in range(5):
        neopix.setColorAll(255, 0, 0)
        neopix.update()
        sleep(0.5)
        neopix.setColorAll(20, 0, 0)
        neopix.update()
        sleep(0.5)
    neopix.setColorAll(0, 0, 0)
    neopix.update()
