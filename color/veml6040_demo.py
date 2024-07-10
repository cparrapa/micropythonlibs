from veml6040 import VEML6040
from time import sleep_ms
from machine import  SoftI2C, Pin 

i2c = SoftI2C(scl=Pin(22), sda=Pin(21)) 
colourSensor = VEML6040(i2c) # initialise the sensor

while True:
    ### Example 1: Print Raw RGB Data
    data = colourSensor.readRGB() # Read the sensor (Colour space: Red Green Blue)
    red = data['red'] # extract the RGB information from data
    grn = data['green']
    blu = data['blue']
    
    print(str(blu) + " Blue  " + str(grn) + " Green  " + str(red) + " Red") # Print the data. Printing as BGR 

    ### Example 2: Classify the colour being shown 
    data = colourSensor.readHSV() # Read the sensor (Colour space: Hue Saturation Value)
    hue = data['hue'] # extract the Hue information from data

    label = colourSensor.classifyHue() # Read the sensor again, this time classify the colour
    print(str(label) + " Hue: " + str(hue)) # Show the label and the corresponding hue

    sleep_ms(1000)
