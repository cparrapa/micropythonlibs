# micropythonlibs
Set of micro Python libraries and example codes to use with HP Otto.

In order for the examples to work, all the files in libs must be uploaded to the circuit board in advance. Then navigate by folder or component:

* accelerometer: examples with ADXL345 (TESTED)
* biped: it is supposed to be a replica of the classic Otto (WIP).
* bluetooth: everything related to the use of Bluetooth, including webcontrol and webcode BLE. (TESTED but can be improved)
* botbit: 3rd party files need to be adapted to HP Otto pins. (WIP)
* encoder: The use of encoder needs to be converted into the ottoencoder.py library. (WIP)
* lights: use of the LED RGB ring and also built-in LED. (TESTED)
* line: infrared sensors for line tracking but could be adapted for other applications (TESTED)
* matrix: multiple LED matrix, 8x8 will be the main; missing mouths and emojis, make into a ottomatrix.py library. (WIP)
* mp3: music (WIP)
* ninja: Code for Walk and Transform as Ninja Remix (TESTED)
* oled: 128x64 monochrome display, missing more faces (TESTED)
* omni: From the Alex remix, it can be adapted to the current Otto. (WIP)
* sensors: general use of sensors (TESTED)
* servo: general use of motors, angles, and wheels (TESTED)
* temphumi: DHT 11 temperature and humidity sensor use (TESTED)
* WiFi: everything related to the use of WiFi web servers, IoT applications, etc. (WIP)

New components and examples are always welcome!

* wirings folder includes some of the default connections and circuit diagrams that are mostly used in the examples, as well as the GPIO pin numbers for the main circuit board.

* blocks folder is for examples that work in webcode. This will help beginners to do transition. The idea is to have for every example both text and block versions.

The best version of MicroPython to use the remote control is v1.19.

The most recent version of MicroPython (v1.22) has problems handling Modes widget changes but has good update on the OLED library for using elipses.
