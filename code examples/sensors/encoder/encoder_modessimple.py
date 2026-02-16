import machine
import time
from machine import I2C, Pin
from ssd1306 import SSD1306_I2C

# Define the pin for the button
button_pin = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)  # Adjust the pin number as needed

# OLED setup
i2c = I2C(scl=Pin(18), sda=Pin(19), freq=400000)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)

def run_program():
    print("Running program1.py...")
    with open('program1.py') as f:
        exec(f.read())

def main():
    print("Do you want to run program1.py? Press the button to confirm.")

    while True:
        oled.fill(0)
        oled.text("Do you want to", 0, 0)
        oled.text("run program1.py?", 0, 10)
        oled.text("Press button.", 0, 20)
        oled.show()
        if not button_pin.value() == 1:  # Check if the button is pressed
            run_program()
            break
        time.sleep(0.1)  # Small delay to avoid CPU hogging

if __name__ == "__main__":
    main()