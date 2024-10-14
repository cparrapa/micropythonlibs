import ssd1306, time, machine
from machine import Pin, SPI, ADC

# Takes an input number value and a range between high-and-low and returns it scaled to the new range
# This is similar to the Arduino map() function
def scaled(value, istart, istop, ostart, ostop):
  return int(ostart + (ostop - ostart) * ((int(value) - istart) / (istop - istart)))

from ssd1306 import SSD1306_I2C

scl=machine.Pin(18) # Connector 1
sda=machine.Pin(19)
i2c=machine.I2C(0,sda=sda, scl=scl)
# Screen size
width=128
height=64
oled = SSD1306_I2C(width, height, i2c)

# Turn all pixels off
oled.fill(0)
oled.show()

# Provide info to user
oled.text('Etch-A-Sketch', 0, 0, 1)
oled.text('Hit the reset', 0, 20, 1)
oled.text('button to clear', 0, 30, 1)
oled.text('the screen', 0, 40, 1)
oled.show()

# Define the pin for the reset button
resetButton = Pin(26, Pin.IN, Pin.PULL_DOWN)

# Wait unti the user hits the button to clear the screen and start drawing
while resetButton.value() != 1:
    time.sleep(.25)

oled.fill(0)
oled.show()

# Define the Horizontal and Vertical inputs from the Rheostats
vert = ADC(32)
horiz = ADC(33)

# Calculate where to start the line
x = newX = scaled(vert.read_u16(), 0, 65536, 0, 128)
y = newY = scaled(horiz.read_u16(), 0, 65536, 0, 64)

# Loop forever
# Draw the line, look for a reset to clear the screen, and get the new end points for the line
while True:
    oled.line(x, y, newX, newY, 1)
    x = newX
    y = newY
    if resetButton.value():
        oled.fill(0)
    oled.show()
    time.sleep(.2)
    newX = scaled(vert.read_u16(), 0, 65536, 0, 128)
    newY = scaled(horiz.read_u16(), 0, 65536, 0, 64)
