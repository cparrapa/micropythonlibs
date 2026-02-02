# ESP32 Sequencer (Updated)

## ESP-NOW FIX
MicroPython ESPNow does NOT use .init().
Use:
    esp = espnow.ESPNow()
    esp.active(True)

## New Features
- Function definition and reuse (DEF FUNC / CALL FUNC)
- Nested functions supported
- Sender can execute locally or remotely
- Clean interpreter-based execution

## Example Function
See routines/routine_with_func.json