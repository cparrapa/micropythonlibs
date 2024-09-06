# micropythonlibs
Set of micro Python libraries and example codes to use with HP Robots Otto starter with all expansions and more.
[version of MicroPython (v1.22)](https://micropython.org/download/ESP32_GENERIC/)

## blocks folder 
Examples that work in webcode. This will help beginners to do transition. The idea is to have for every example both text and block versions.

## libraries
In order for the examples to work, FIRST save all the [**files in libs must be uploaded**](https://github.com/cparrapa/micropythonlibs/tree/main/libs) to the circuit board in advance. 

Then navigate by folder or component to try examples:

* accelerometer: examples with ADXL345 sensor. (TESTED)
* biped: it is supposed to be a replica of the classic Otto (WIP).
* bluetooth: everything related to the use of Bluetooth, including webcontrol and webcode BLE. (TESTED but can be improved)
* botbit: 3rd party files need to be adapted to HP Otto pins. (WIP)
* button: simple digital input (TESTED)
* buzzer: sounds for embedded PCB piezo (TESTED)
* color: sensor based on tcs34725 but chip is End Of Life (WIP)
* encoder: The use of encoder needs to be converted into the ottoencoder.py library. (WIP)
* light: simple LDR sensor (WIP)
* line: infrared sensors for line tracking but could be adapted for other applications (TESTED)
* matrix: multiple LED matrix, RGB 8x8 will be the main; missing mouths and emojis and ottomatrix.py library. (WIP)
* microphone:  needs a way to detect better in analog (WIP)
* motorangle:  use of fix angle servo motors 180 (TESTED)
* motorwheel:  use of continuos roation servo motors 360 (TESTED)
* mp3: music player needs check (WIP)
* ninja: Code for Walk and Transform as Ninja Remix (TESTED)
* oled: 128x64 monochrome display, missing more faces (TESTED)
* omni: From the Alex remix, it can be adapted to the current Otto. (WIP)
* potentiometer: simple analog input (WIP)
* ring: use of the LED RGB ring and also built-in LED. (TESTED)
* temphumi: DHT 11 & 22 temperature and humidity sensor (TESTED)
* tilt: simple digital input (TESTED)
* ultrasonic: Distance sonar sensor needs more examples (WIP)
* wifi: everything related to the use of WiFi web servers, IoT applications, etc. (WIP)

New components and examples are always welcome!

## wirings folder 
includes some of the default connections and circuit diagrams that are mostly used in the examples, as well as the GPIO pin numbers for the main circuit board, but always double check GPIO pins with their respective connector #:

* Built in LED:  GPIO 2
* Buzzer pin:    GPIO 25
* Battery pin:   GPIO 39 
* Connector #1:  GPIO 18 & 19
* Connector #2:  GPIO 16 & 17 
* Connector #3:  GPIO 22 & 21 (I2C SCL & SDA) 
* Connector #5:  GPIO 4 
* Connector #6:  GPIO 32 (ADC good for analog inputs) 
* Connector #7:  GPIO 33 (ADC good for analog inputs) 
* Connector #8:  GPIO 27
* Connector #9:  GPIO 15
* Connector #10: GPIO 13
* Connector #11: GPIO 33