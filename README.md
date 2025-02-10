# micropythonlibs
Set of micro Python libraries and example codes to use with HP Robots Otto starter with all expansions and more.
[version of MicroPython (v1.22)](https://micropython.org/download/ESP32_GENERIC/)

## libraries v2.0 
In order for the examples to work, FIRST [**all files in libraries must be uploaded**](https://github.com/cparrapa/micropythonlibs/tree/main/libraries) to the circuit board in advance. Some are WIP (work in progress) not even functional.

- ottomotor.py v2.0- in charge of servo motors classes (pending separate)
- ottobuzzer.py v2.0- piezo notes and RTTTL melodies (pending separate mp3)
- ottoneopixel.py v2.3- every RGB LED related component (pending separate ring, matrix and ultrasonic)
- ottosensors.py v2.1- multiple sensors (pending split into independent sensors library)
- ottodisplay.py v2.0- display faces (pending rename and update)
- ottomp3.py v1.0- mp3 player
- ottoble.py v2.1- bluetooth communication for block coding
- ottoiot.py v1.0- internet of things
- adxl345.py v1.0- default accelerometer chip
- ssd1306.py v0.0 - default OLED driver
- directory.py - index 

These libraries are used and must be in sync with the main Webcode repository [python/libraries](https://github.com/cparrapa/webcode/blob/main/python/libraries/)

## [blocks examples](https://github.com/cparrapa/micropythonlibs/tree/main/blocks%20examples)
Examples that work in [webcode icons, words or AI](https://hprobots.com/otto-code/webcode/webcode.html). 
The best [guide to get started in blocks is here](https://hprobots.com/otto-robot/code/#flipbook-hp-robots-otto-starter-coding-intro/1/)
This will help beginners to do the transition to text code. The idea is to have for every example both block and text version.

## [code examples](https://github.com/cparrapa/micropythonlibs/tree/main/code%20examples)
The actual micropython text code demos, navigate by folder/component:

* accelerometer: examples with ADXL345 sensor but we need games with it (TESTED)
* biped: it is supposed to be a replica of the classic Otto, needs to be tested (WIP)
* bluetooth: everything related to Bluetooth, includes webcontrol and webcode programming with BLE. (TESTED)
* botbit: 3rd party files need to be adapted to HP Otto pins. (WIP)
* button: simple digital input (TESTED)
* buzzer: sounds for embedded PCB piezo. (TESTED)
* color: sensor based on tcs34725 but chip is or was End Of Life. (WIP)
* encoder: The use of encoder needs to be converted into the ottoencoder.py library. which library is best? (WIP)
* IoT: internet of things examples with the use of WiFi. (WIP)
* koi: AI camera, compatibillity pending. (WIP)
* light: simple LDR sensor. (TESTED)
* line: infrared sensors for line tracking but could be adapted for other applications. (TESTED)
* matrix: multiple LED matrix, RGB 8x8 will be the main; missing mouths and emojis and ottomatrix.py library. (TESTED)
* microphone:  needs a way to detect better in analog. (TESTED)
* motorangle:  use of fix angle servo motors 180. (TESTED)
* motorwheel:  use of continuous rotation servo motors 360. (TESTED)
* mp3: music player works but needs an independent library from buzzer (TESTED)
* ninja: Walk and Roll transformer remix. (TESTED)
* oled: 128x64 monochrome display, missing more faces. (TESTED)
* omni: From the Alex remix, it can be adapted to the current Otto. (WIP)
* potentiometer: simple analog input. (TESTED)
* ring: use of the LED RGB ring and also built-in LED. (TESTED)
* temphumi: DHT 11 & 22 temperature and humidity sensor. (TESTED)
* tilt: simple digital input. (TESTED)
* showcase: set of selected codes for demostrations. (TESTED)
* ultrasonic: Distance sonar sensor needs more examples. (TESTED)
* wifi: everything related to the use of WiFi web server. (WIP)

New components and examples are always welcome!

## [wirings](https://github.com/cparrapa/micropythonlibs/tree/main/wirings)
Includes the "DEFAULT" connections and circuit diagrams that are mostly used in the examples, as well as the GPIO pin numbers for the main circuit board,
![Main circuit board](https://github.com/cparrapa/micropythonlibs/blob/main/wirings/Otto%20circuitboardpinout.png)

In any case always double check GPIO pins defined within the code and their respective connector #:

* Built in LED:    GPIO 2
* Built in Buzzer: GPIO 25
* Battery voltage: GPIO 39 
* Connector #1:  GPIO 18 & 19 (ultrasonic or OLED)
* Connector #2:  GPIO 16 & 17 (mp3 or encoder)
* Connector #3:  GPIO 22 & 21 I2C SCL & SDA (matrix or accelerometer)
* Connector #4:  GPIO 26 (tilt or button)
* Connector #5:  GPIO 4  (LED ring or temperature sensor)
* Connector #6:  GPIO 32 ADC good for analog inputs (line sensor left or microphone) 
* Connector #7:  GPIO 33 ADC good for analog inputs (line sensor right or potentiometer or light sensor) 
* Connector #8:  GPIO 27 (servo angle right)
* Connector #9:  GPIO 15 (servo angle right)
* Connector #10: GPIO 13 (servo wheel left)
* Connector #11: GPIO 33 (servo wheel right)

The components assigment to the GPIO are only default connections, you can rearrange depending on your application.

## [3D print .STL](https://github.com/cparrapa/micropythonlibs/tree/main/3d%20print%20stl)
You will find all 3D printable files in this folder sorted by type of modularity, with some exception prebuilds. There are also some neutral .STP files that work as templates for importing in any CAD software.
* top:  head part commonly use for LED ring or sensors, it could allocate anything that fits or make it taller if required.
* middle: the band that initially fits only the main circuit board and battery but also for spacers.
* face: this modifies greatly the appearance of the robot you could fit multiple displays and even sensors.
* bottom: any propulsion system you want is going to be likely here.
* bumper: more on the accessory side but it has great potential for multiple extra devices and attachments. 