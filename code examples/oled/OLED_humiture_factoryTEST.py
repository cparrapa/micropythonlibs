from machine import Pin, SoftI2C
import ssd1306
import dht
import time

# Initialize I2C for OLED
i2c = SoftI2C(scl=Pin(18), sda=Pin(19)) # Connector 1

# Scan for I2C devices
devices = i2c.scan()
if not devices:
    raise Exception('No I2C devices found')
else:
    print('I2C devices found:', [hex(device) for device in devices])

# Assuming the address is 0x3C (check this from the scan result)
oled_address = 0x3C

# Initialize OLED display (128x64)
oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, addr=oled_address)

# Initialize DHT sensor (Assuming DHT11 or DHT22)
sensor = dht.DHT11(Pin(27))

def read_sensor():
    """Read temperature and humidity from the sensor."""
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    return temp, hum

def display_data(temp, hum):
    """Display temperature and humidity on the OLED."""
    oled.fill(0)
    oled.text("Temp: {} C".format(temp), 0, 0)
    oled.text("Hum: {} %".format(hum), 0, 10)
    oled.show()

while True:
    try:
        temperature, humidity = read_sensor()
        display_data(temperature, humidity)
    except OSError as e:
        print('Failed to read sensor.')
    
    time.sleep(2)
