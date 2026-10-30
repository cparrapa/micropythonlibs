## OttoNinjaPA – ESP32-C3 Robot (MicroPython)

OttoNinjaPA is a MicroPython-based firmware for a small biped Otto Ninja robot controlled over ESP‑NOW.  
An ESP32‑C3 Zero board receives joystick and button data from a custom wireless controller - [FusionPad32000](https://github.com/boryspimpek/FusionPad32000.git) and drives six servos to perform different walking and gesture motions.

<img src="images/foto.jpg" width="400">

### Features

- **ESP‑NOW receiver**: Listens for joystick and button states from a custom wireless controller.
- **Servo abstraction layer**: Smooth, coordinated movement of multiple servos with trims and soft transitions.
- **Predefined moves**: Walking steps, tilts, leg swings, waving, and more.
- **Ride mode**: Direct joystick control of the feet in a special “ride” position.
- **Interactive calibration tool**: `servo_calib.py` for fine‑tuning servo angles via REPL.

### Hardware Requirements

- **MCU**: ESP32‑C3 Zero (or compatible ESP32 board) running MicroPython.
- **Servos**:
  - 2 × continuous‑rotation servos for feet (`LF`, `RF`)
  - 4 × standard servos for legs and arms (`LL`, `RL`, `LA`, `RA`)
- **Power**: Separate, adequately rated 5V supply for servos (recommended), common GND with the ESP32.
- **Wireless controller** that sends ESP‑NOW packets matching the expected data format (joysticks, buttons, pot).

### Pinout (ESP32‑C3 Zero)

Servos are driven via `PWM` on these pins (see `ServoController` in `servo_lib.py`):

- `RF` (right foot)  – PWM on pin **5** (index 0)
- `RL` (right leg)   – PWM on pin **4** (index 1)
- `RA` (right arm)   – PWM on pin **3** (index 2)
- `LF` (left foot)   – PWM on pin **6** (index 3)
- `LL` (left leg)    – PWM on pin **7** (index 4)
- `LA` (left arm)    – PWM on pin **8** (index 5)

### Project Structure

- `main.py`  
  Main control loop. Reads data from `RobotConfig().robot` (ESP‑NOW receiver), debounces buttons, and triggers high‑level moves in `RobotMoves`.

- `servo_lib.py`  
  Low‑level servo and robot configuration:
  - `ServoController`: angle/speed API, soft `move_to_angles`, joystick mapping, trims.
  - `RobotReceiver`: parses ESP‑NOW packets into joystick axes, buttons and switches.
  - `RobotConfig`: hardware setup (Wi‑Fi, ESP‑NOW, servo trims, initial pose) and `tick()` method for receiving controller packets.

- `moves.py`  
  High‑level movement routines implemented in `RobotMoves`:
  - `return_to_neutral`, `tilt_left`, `tilt_right`
  - `steps`, `tilt`, `wave`
  - leg swing moves: `left_leg_swing_forward/back`, `right_leg_swing_forward/back`
  - a randomized `weird` motion pattern.

- `servo_calib.py`  
  Interactive calibration utility for legs and arms over the MicroPython REPL. Lets you adjust logical angles with keyboard shortcuts and prints the resulting positions.

- `boot.py`  
  Standard MicroPython boot script; you can use it to automatically start `main.py` on boot.

### Getting Started

1. **Flash MicroPython**  
   - Install MicroPython firmware for ESP32‑C3 on your board (see official MicroPython documentation for the exact steps).

2. **Copy project files to the board**  
   - Use a tool like Thonny, or the Pymakr plugin to upload:
     - `main.py`
     - `servo_lib.py`
     - `moves.py`
     - `servo_calib.py`
     - `boot.py`

3. **Configure the controller (transmitter)**  
   - Ensure the transmitter is set up to send ESP‑NOW packets with the same structure as expected in `RobotReceiver.update()`:
     - 4 signed bytes (`lx`, `ly`, `rx`, `ry`)
     - 1 unsigned short (`pot1`)
     - 1 unsigned short (`mask`) with button bits.
   - Pair the transmitter MAC address with the receiver if required by your controller firmware.

4. **Power and wiring**  
   - Connect the servos to the pins listed above.
   - Provide a suitable 5V supply for all servos and **share GND** between the power supply and the ESP32 board.

5. **Run the main firmware**  
   - Reset or power‑cycle the board.
   - In the serial console you should see boot messages from `RobotConfig`:
     - Servo initialization
     - Wi‑Fi + ESP‑NOW setup
     - Connection status.
   - Once the controller connects, button presses and joystick movements should trigger robot motions.

### Using the Servo Calibration Tool

1. Connect to the board’s REPL.
2. Import and run the calibration module:

```python
import servo_calib
servo_calib.run()
```

3. Use the keys listed at the top of `servo_calib.py` (e.g. `a/d`, `j/l`, `w/e`, `s/c`, `r`, `p`, `q`) to adjust angles and read out final positions.
4. Apply discovered offsets back into `RobotConfig`’s trim settings in `servo_lib.py` if you change the mechanical setup.

### Development Notes

- The main loop in `main.py` relies on `cfg.tick()`; new moves should follow the same pattern (trigger on button press, clean up on release).
- `ServoController.move_to_angles()` performs smooth, multi‑servo interpolation; use it for complex sequences rather than abrupt `set_angle` calls.
- For new actions, add methods to `RobotMoves` and map them to free buttons or switch combinations in `main.py`.

