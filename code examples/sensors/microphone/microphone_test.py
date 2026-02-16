from machine import Pin, ADC, I2C
import ssd1306
import time

# Initialize I2C communication
i2c = I2C(scl=Pin(18), sda=Pin(19))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize ADC for sound sensor
adc = ADC(Pin(32)) #Connector 6

# Define pins for LED indicators
PIN_QUIET = Pin(14, Pin.OUT)
PIN_MODERATE = Pin(27, Pin.OUT)
PIN_LOUD = Pin(2, Pin.OUT)

# Set initial LED states
PIN_QUIET.off()
PIN_MODERATE.off()
PIN_LOUD.off()

def read_sound_level():
    sampleWindow = 50  # Set the sample window (milliseconds)
    signalMax = 0
    signalMin = 1024
    startMillis = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), startMillis) < sampleWindow:
        sample = adc.read()
        if sample < 1024:
            signalMax = max(signalMax, sample)
            signalMin = min(signalMin, sample)
    
    peakToPeak = signalMax - signalMin
    db = int(map_range(peakToPeak, 0, 900, 49, 90))
    return db

def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

while True:
    db = read_sound_level()
    display.fill(0)
    print("Loudness:", db, "dB")
    display.text("Loudness:", 0, 0)
    display.text(str(db) + " dB", 0, 16)
    display.show()
    
    if db <= 55:
        display.text("Level: Quiet", 0, 32)
        display.show()
        PIN_QUIET.on()
        PIN_MODERATE.off()
        PIN_LOUD.off()
        
    elif 60 < db < 85:
        display.text("Level: Moderate", 0, 32)
        display.show()
        PIN_QUIET.off()
        PIN_MODERATE.on()
        PIN_LOUD.off()
        
    elif 85 <= db <= 90:
        display.text("Level: High", 0, 32)
        display.show()
        PIN_QUIET.off()
        PIN_MODERATE.off()
        PIN_LOUD.on()
        
    else:
        PIN_QUIET.off()
        PIN_MODERATE.off()
        PIN_LOUD.off()
    
    time.sleep(0.2)