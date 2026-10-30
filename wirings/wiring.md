# Wiring Reference

Pin assignments and peripheral wiring for the HP Robots Otto Starter Kit PCB. Ignore the Serial Bus Servo section if you are using the original kit.

---

## Connector Pin Map

The PCB has 11 numbered JST connectors. Each exposes one or two signal GPIOs plus VCC and GND.

| Connector | GPIO | Type | Default Use (Starter Kit) | Alternatives |
|:---------:|:----:|:----:|---------------------------|--------------|
| 1 | 18, 19 | Digital | Ultrasonic sensor (RCWL-9610) | OLED display |
| 2 | 16, 17 | UART | *Unused* | Serial bus servos, MP3 player |
| 3 | 22, 21 | I2C | *Unused* | Matrix display, accelerometer |
| 4 | 26 | Digital | *Unused* | Tilt sensor, button |
| 5 | 4 | Digital | LED ring (13 x WS2812B) | Temperature sensor |
| 6 | 32 | ADC | Left IR line sensor | Microphone |
| 7 | 33 | ADC | Right IR line sensor | Potentiometer, light sensor |
| 8 | 27 | PWM | *Unused* (biped: right hip) | — |
| 9 | 15 | PWM | *Unused* (biped: left hip) | — |
| 10 | 14 | PWM | Left wheel servo | — |
| 11 | 13 | PWM | Right wheel servo | — |

## On-Board Peripherals (No Connector)

| Function | GPIO | Notes |
|----------|:----:|-------|
| Status LED | 2 | Blue, active-high |
| Buzzer | 25 | Passive electromagnetic, PWM driven |
| Battery voltage | 39 | ADC input-only, through voltage divider (2 x 100 kΩ) |

---

## Ultrasonic Sensor (Connector 1)

The RCWL-9610 is wired to Connector 1:

| Pin | GPIO | Function |
|-----|:----:|----------|
| Signal A | 18 | NeoPixel data — 6 x WS2812B LEDs on the sensor PCB |
| Signal B | 19 | Trigger / Echo (single-wire mode) |

In single-wire mode, GPIO 19 toggles between output (10 µs trigger pulse) and input (echo timing) for each reading.

---

## Servo Wiring (Starter Kit — PWM)

Default mode (`SERVO_TYPE_SERIAL_BUS=0`):

| Wheel | Connector | GPIO | Signal |
|-------|:---------:|:----:|--------|
| Left | 10 | 14 | 50 Hz PWM, 1000–2000 µs (1500 µs = stop) |
| Right | 11 | 13 | 50 Hz PWM, 1000–2000 µs (mirror-mounted) |

---

## Serial Bus Servo Mode (Connector 2)

When `SERVO_TYPE_SERIAL_BUS=1` in `platformio.ini`, the servos communicate over a half-duplex UART bus on **Connector 2**:

| Pin | GPIO | Function |
|-----|:----:|----------|
| Signal A | 16 | UART2 RX |
| Signal B | 17 | UART2 TX |

- **Baud rate**: 1 000 000
- **Protocol**: Feetech SCServo (STS/SCS series)
- The ultrasonic sensor on Connector 1 remains available — the two modes are independent.

---

## Line Sensors (Connectors 6 & 7)

Two TCRT5000-based IR reflectance modules for detecting dark lines on light surfaces. Each has an onboard potentiometer — see [calibration.md](calibration.md) for setup instructions.

| Sensor | Connector | GPIO | ADC |
|--------|:---------:|:----:|-----|
| Left | 6 | 32 | 12-bit (0–4095), 20 Hz on `/line_sensors` |
| Right | 7 | 33 | 12-bit (0–4095), 20 Hz on `/line_sensors` |

---

## Battery Monitoring

- **GPIO 39** reads through a 2:1 voltage divider (2 x 100 kΩ resistors)
- LiPo single cell: 3.0 V (empty) → 4.2 V (full)
- Calibrate `BATTERY_DIVIDER_RATIO` in [`otto_config.h`](../firmware/src/otto_config.h) with a multimeter if readings are inaccurate

---

<p align="center">
  <br>
  <img src="images/fame-logo.letterbox.png" alt="FAME logo" width="200">
</p>
