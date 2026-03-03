from microbit import *
from MuVisionSensor import *

mu=MuVisionSensor(0x60)
mu.begin()
mu.VisionBegin(VISION_SHAPE_CARD_DETECT)
while True:
    if mu.GetValue(VISION_SHAPE_CARD_DETECT,Status):
        print("x: %d" % mu.GetValue(VISION_SHAPE_CARD_DETECT,XValue))
        print("y: %d" % mu.GetValue(VISION_SHAPE_CARD_DETECT,YValue))
        print("width: %d" % mu.GetValue(VISION_SHAPE_CARD_DETECT,WidthValue))
        print("height: %d" % mu.GetValue(VISION_SHAPE_CARD_DETECT,HeightValue))
        print("Label: %d" % mu.GetValue(VISION_SHAPE_CARD_DETECT,Label))
    else:
        print("undetected")
    sleep(0.1)
