# HP Robots Otto – MicroPython Libraries

A complete collection of MicroPython libraries, example programs, 3D STL files, and resources for use with the [HP Robots Otto starter and all expansions.](https://hprobots.com/otto-robot/product/) 
Compatible with MicroPython v1.26.1.
[👉 Recommended: Use our Quick Flasher to install MicroPython easily)](https://hprobots.com/otto-code/webcode/pythonuploader/pythonuploader.html)

If you prefer using Arduino IDE, follow the Arduino alternative programming guide included in this repository.

📌 This repository includes:

* MicroPython libraries for each robot component
* Example code for both block-based and text programming
* Wiring diagrams and pinouts

## [wirings](https://github.com/cparrapa/micropythonlibs/tree/main/wirings)
Circuit diagrams and “default wiring” reference used across all examples.
![Main circuit board](https://github.com/cparrapa/micropythonlibs/blob/main/wirings/Otto%20circuitboardpinout.png)

Always verify that the pins used in your code match the connector you are using:

|        Function       |        GPIO        |                 Notes                |
|:---------------------:|:------------------:|:------------------------------------:|
| Built‑in LED          | 2                  | Status LED                           |
| Built‑in Buzzer       | 25                 | Piezo buzzer                         |
| Battery voltage (ADC) | 39                 | Battery sense                        |
| Connector #1          | 18, 19             | Ultrasonic / SPI OLED                |
| Connector #2          | 16, 17             | MP3 module / Digital encoder         |
| Connector #3 (I²C)    | 22 (SCL), 21 (SDA) | Matrix, accelerometer, OLED (I²C)    |
| Connector #4          | 26                 | Tilt switch / Button                 |
| Connector #5          | 4                  | RGB LED ring (13 LEDs) / Temp sensor |
| Connector #6 (ADC)    | 32                 | Line sensor L / Microphone           |
| Connector #7 (ADC)    | 33                 | Line sensor R / Potentiometer / LDR  |
| Connector #8          | 27                 | Servo angle right                    |
| Connector #9          | 15                 | Servo angle left                     |
| Connector #10         | 14                 | Wheel servo (left)                   |
| Connector #11         | 13                 | Wheel servo (right)                  |

## [libraries](https://github.com/cparrapa/micropythonlibs/tree/main/libraries)
MicroPython modules organized by functionality.
⚠️ Important: Examples require that you upload [**all library**](https://github.com/cparrapa/micropythonlibs/tree/main/libraries) files to the Otto board first using [Thonny IDE](https://thonny.org/) or any other Micropython IDE.

Core Modules
|          File          |                Description                |
|:----------------------:|:-----------------------------------------:|
| ottomotor.py (v2.0)    | Servo motor classes (split pending)       |
| ottoangle.py           | Angle‑servo utilities                     |
| ottowalkroll.py        | Biped + wheeled movement behaviors        |
| ottobattery.py         | Battery monitoring                        |
| otto4wd.py             | 4‑wheel drive (not available as blocks)   |
| ottobuzzer.py (v2.2)   | RTTTL melodies + piezo tones              |
| ottoline.py            | IR line sensors                           |
| ottoneopixel.py (v2.3) | RGB LEDs and NeoPixel devices             |
| ottoring.py            | ❗ Pending: 13‑LED ring wrapper            |
| ottomatrix.py          | ❗ Pending: 8×8 LED matrix wrapper         |
| ottoultrasonic.py      | ❗ Pending: ultrasonic + LED combo         |
| ottosensors.py (v2.1)  | Multi‑sensor utilities (split pending)    |
| ottodht.py             | DHT11 temperature/humidity                |
| ottoldr.py             | ❗ Pending: Light sensor                   |
| ottomic.py             | ❗ Pending: analog sound detection         |
| ottotilt.py            | ❗ Pending: tilt switch utilities          |
| ottobutton.py          | ❗ Pending: button debouncing              |
| ottoencoder.py         | ❗ Pending: encoder abstraction            |
| adxl345.py (v1.0)      | Accelerometer driver                      |
| ottoaccelerometer.py   | ❗ Pending: high‑level accelerometer class |
| ssd1306.py (v0.0)      | OLED driver (third‑party)                 |
| ottodisplay.py (v2.1)  | Faces/emoji rendering for OLED            |
| ottomp3.py (v1.0)      | MP3 module control                        |
| ottoble.py (v2.1)      | Deprecated BLE communication              |
| ottoiot.py (v1.0)      | Wi‑Fi IoT features                        |
| directory.py           | Index file                                |
| wifi                   | WIP                                       |

### Naming Conventions
To maintain consistency:
* Classes → CamelCase
* Functions → CamelCase
* Variables → snake_case
* Files/Modules → snake_case.py
* Constants → UPPER_CASE_WITH_UNDERSCORES

## [blocks examples](https://github.com/cparrapa/micropythonlibs/tree/main/blocks%20examples)
Examples compatible with the [WebCode block editor (icons or words)](https://hprobots.com/otto-code/webcode/webcode.html) and head to the [Beginner guide (highly recommended)](https://hprobots.com/otto-robot/code/#flipbook-hp-robots-otto-starter-coding-intro/1/)

🧩 Goal:
Every example should have both a block version and a MicroPython text version to help students transition smoothly.

## [code examples](https://github.com/cparrapa/micropythonlibs/tree/main/code%20examples)
Full MicroPython demo programs organized by component/sensor module.

|     Folder    | Status |                    Notes                    |
|:-------------:|:------:|:-------------------------------------------:|
| accelerometer | TESTED | ADXL345 examples — needs more games         |
| biped         | WIP    | Classic Otto walking                        |
| bluetooth     | TESTED | BLE WebControl & WebCode                    |
| botbit        | WIP    | Requires adaptation to HP Otto pins         |
| button        | TESTED | Simple digital input                        |
| buzzer        | TESTED | Piezo melodies                              |
| color         | WIP    | TCS34725 sensor (EOL chip)                  |
| encoder       | WIP    | Needs ottoencoder.py integration            |
| IoT           | WIP    | Wi‑Fi examples                              |
| koi           | WIP    | AI camera integration                       |
| light         | TESTED | LDR analog sensor                           |
| line          | TESTED | Line tracking IR sensors                    |
| matrix        | TESTED | LED matrix examples (missing mouths/emojis) |
| microphone    | TESTED | Basic analog sound detection                |
| motorangle    | TESTED | 180° servo examples                         |
| motorwheel    | TESTED | 360° wheel servos                           |
| mp3           | TESTED | MP3 module (needs separate lib)             |
| ninja         | TESTED | Walk‑and‑Roll hybrid                        |
| oled          | TESTED | 128×64 display — more faces needed          |
| omni          | WIP    | From Alex remix                             |
| potentiometer | TESTED | Analog input                                |
| ring          | TESTED | RGB LED ring + built‑in LED                 |
| temphumi      | TESTED | DHT11/22                                    |
| tilt          | TESTED | Digital tilt switch                         |
| showcase      | TESTED | Demo bundle                                 |
| ultrasonic    | TESTED | Distance sensor (needs more examples)       |
| wifi          | WIP    | Web server + Wi‑Fi control                  |

🤝 Contributions
New components, sensors, libraries, and examples are always welcome!
Feel free to submit PRs or open issues if you’d like to help expand the Otto ecosystem.