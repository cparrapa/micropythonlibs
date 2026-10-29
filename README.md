<div align="center">
<br>

# HP Robots Otto – MicroPython Libraries
Welcome to the official repo for Code Libraries, Example programs & Diagrams for [HP Robots Otto](https://shop.moravia.education/educational-and-interactive-robots/hp-robots/hp-robots-otto-creator-kit.html)

[![Thoony IDE](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://thonny.org/)
[![MicroPython v1.26.1.](https://img.shields.io/badge/MicroPython-v1.26.1-blue.svg)](https://micropython.org/download/ESP32_GENERIC/)
[![ESP32-WROOM](https://img.shields.io/badge/Platform-ESP32--WROOM-lightgrey.svg)](https://www.espressif.com/en/products/socs/esp32)
[![Code License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Contribute](https://img.shields.io/badge/Contributions-Welcome-brightgreen.svg)](https://github.com/cparrapa/micropythonlibs/pulls)
[![Discord](https://img.shields.io/badge/Discord-%235865F2.svg?&logo=discord&logoColor=white)](https://discord.gg/CZZytnw)
[![Website](https://img.shields.io/badge/Website-hprobots?logo=google-chrome&logoColor=white)](https://hprobots.com/)
</div>

* A full collection of MicroPython libraries for HP Robots Otto
* Example code for every sensor, expansion, and robot behavior
* Wiring diagrams & pinouts
* Basic coding Guides for both MicroPython with Thonny IDE or C++ with Arduino IDE

## 🚀 Quick Start
1. Use the Quick Flasher to install [MicroPython firmware with all  Core libraries](https://hprobots.com/app/)
2. Open [Thonny IDE](https://thonny.org/) → select **MicroPython (ESP32)**  
3. Run examples from `/code examples/` with the right components connected.

Or use [`mip`](https://docs.micropython.org/en/latest/reference/packages.html) (`mpremote mip install github:cparrapa/micropythonlibs/libraries`).

---

## 🔌 ESP32 Wiring & Pinout
Pin references and wiring diagrams. Circuit diagrams and “default wiring” reference used across most examples.
### Mainboard GPIO Reference
![Main circuit board](/wirings/HPOttodefaultconnections.jpg)

Always verify that the number of the GPIO used in your code match the connector you are using:
| Connector| GPIO | Main Purpose |
|----------|------|----------|
| #1 | 18 & 19 | Ultrasonic sensor + 6 RGB LEDs / OLED Display |
| #2 | 16 & 17 | MP3 Player / Digital Encoder |
| #3 | 22 SCL & 21 SDA | RGB Matrix (64 LEDs) / Accelerometer / or other I²C |
| #4 | 26 | Tilt sensor / Button (Encoder) |
| #5 | 4 | RGB Ring (13 LEDs) | Temperature & Humidity sensor
| #6 | 32 | Line sensor L / Sound sensor | 
| #7 | 33 | Line sensor R / Light sensor / Potentiomer | 
| #8 | 27 | Servo angle 180° Left  / Button |
| #9 | 15 | Servo angle 180° Right |
| #10 | 14 | Servo Wheel Left |
| #11 | 13 | Servo Wheel Right |

### Integrated / Built‑in parts:
|  Component  |  GPIO  |  Function     |
|-------------|--------|---------------|
| Blue LED      | 2 | Status Light |
| Piezo Buzzer | 25 | Basic Beeps |
| Battery Sense | 39 | ADC Voltage Level Check |

[More diagrams here](https://github.com/cparrapa/micropythonlibs/tree/main/wirings)  

## 📦 MicroPython Libraries
Below is the full list of current [libraries](https://github.com/cparrapa/micropythonlibs/tree/main/libraries)   and modules included in the `micropythonlibs` repository.

### Core Modules
- `ottobuzzer.py` — Beeps, Notes & RTTTL  
- `ottomotor.py`   — Servo motor control  
- `ottoneopixel.py` — RGB LED Ring / RGB Matrix / RGB Ultrasonic and general NeoPixel
- `ottooled.py` — Faces/emoji rendering for OLED     
- `ottosensors.py` —  Multi‑sensors utilities  
- `ottowalkroll.py` —   Ninja + wheeled movement behaviors  

### Pending Modules (WIP)
- `otto4wd.py` —  4 wheel drive & Mecanum wheels
- `ottoble.py` — BLE connectivity 
- `ottoencoder.py` — rotary encoder own library
- `ottoiot.py`    —  Broader Wi‑Fi IoT features  

### Third-Party Drivers
- `ssd1306.py`    — OLED Display driver
- `adxl345.py`    — Accelerometer driver  

### App config files
- `config.py` — App events handling
- `main.py` — Main code that wasits to connect with app 
- `rc.py` — API for bluetooth remote control
- `update_library.py` — OTA updates  
- `util.py` — ble and nvs for kit type
- `wifi_manager.py` — WiFi connectivity 
- `package.json` — List of all libraries and version 

## 🧪 MicroPython Code Examples  
Organized by component, sensors, motors, displays & more.  [all here](https://github.com/cparrapa/micropythonlibs/tree/main/code%20examples)
> ⚠️ **Reminder:** Make sure  ALL files in `/libraries/` are in the circuit board before running examples.
✅ Tested  
🛠 Work in Progress  

| Component | Folder | Status |
|----------|--------|--------|
| Buzzer        | `/buzzer` | ✅ Piezo melodies          |
| RGB Ring | `/rgbring` | ✅RGB LED ring + built LED   |
| RGB Matrix      | `/rgbmatrix`, `/games` | ✅ LED matrix examples |
| Motor Angle    | `/motorangle` | ✅ 180° servo examples|
| Motor Wheel    | `/motorwheel` | ✅ 360° wheel servos|
| MP3           | `/mp3` | ✅ MP3 module|
| OLED          | `/oled`, `/games` | ✅ 128×64 display         |
| Showcase      | `/showcase` | ✅ Bundles & Kit demos|
| ESPNOW         | `/espnow`    | ✅ Wireless communication|
| Mecanum        | `/mecanum`     | ✅ From Alex remix|

| Sensor | Folder | Status |
|----------|--------|--------|
| Accelerometer | `/sensors/accelerometer` | ✅  games will be nice  |
| Button        | `/sensors/button` | ✅ Simple digital input     |
| Encoder       | `/sensors/encoder`| 🛠  ottoencoder.py |
| Light        | `/sensors/light` | ✅ LDR analog sensor|
| Line  | `/sensors/line` | ✅ Tracking InfraRed sensors  |
| Microphone    | `/sensors/microphone` | ✅ Basic  sound detection|
| Potentiometer | `/sensors/light` | ✅ Analog input|
| Tempeature & Humidity      | `/sensors/temphumi` | ✅ DHT11/22|
| Tilt          | `/sensors/tilt` | ✅ Digital position switch|
| Ultrasonic    | `/sensors/ultrasonic` | ✅ Distance sensor      |

---
## ❤️ Contribute

Pull requests for:

➡️ New sensors  
➡️ Better demos  
➡️ Library improvements  
➡️ Bug fixes  
➡️ Teaching materials  

…are always welcome! Feel [free to submit PRs](https://github.com/cparrapa/micropythonlibs/pulls) or [open issues](https://github.com/cparrapa/micropythonlibs/issues) if you’d like to help expand the HP Otto ecosystem.
