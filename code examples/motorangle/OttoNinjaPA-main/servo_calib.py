"""
servo_calib.py — interaktywny kalibratory serw LL i RL przez REPL
=================================================================
Sterowanie:
  a / d  — RL  lewo/prawo (−1 / +1 stopień)
  j / l  — LL  lewo/prawo (−1 / +1 stopień)
  w / e  — RA  lewo/prawo (−1 / +1 stopień)
  s / c  — LA  lewo/prawo (−1 / +1 stopień)
  r      — reset obu serw do 90°
  p      — wypisz aktualne pozycje
  q      — wyjście (serwa zostają na ostatniej pozycji)

Użycie:
  >>> import servo_calib
  >>> servo_calib.run()
"""

import sys
import select
from machine import Pin, PWM  # type: ignore

# ── Piny (zgodnie z servo_lib.py) ──────────────────────────────────────
PIN_RL = 4   # RL = index 1 → pin 4
PIN_LL = 7   # LL = index 4 → pin 7
PIN_RA = 3   # RA = index 2 → pin 3
PIN_LA = 8   # LA = index 5 → pin 8

TRIM_RL = -5  # trim z RobotConfig
TRIM_LL = +2  # trim z RobotConfig
TRIM_RA = 0   # trim z RobotConfig
TRIM_LA = 6   # trim z RobotConfig

# ── PWM helpers ────────────────────────────────────────────────────────
def _make_pwm(pin_no):
    return PWM(Pin(pin_no), freq=50)

def _angle_to_duty(angle):
    angle = max(0, min(180, angle))
    return int(((angle / 180) * (8192 - 1638)) + 1638)

def _set_angle_raw(pwm, angle):
    pwm.duty_u16(_angle_to_duty(angle))

def _set_angle(pwm, logical_angle, trim):
    """Ustawia kąt z trymem — dokładnie jak ServoController.set_angle()"""
    _set_angle_raw(pwm, logical_angle + trim)

# ── Główna pętla ────────────────────────────────────────────────────────
def run(start_ll=60, start_rl=120, start_ra=90, start_la=90):

    pwm_rf = PWM(Pin(5), freq=50)
    pwm_lf = PWM(Pin(6), freq=50)
    pwm_ra = PWM(Pin(3), freq=50)
    pwm_la = PWM(Pin(8), freq=50)
    _set_angle_raw(pwm_rf, 90-3)  # 90° = stop dla serwa 360
    _set_angle_raw(pwm_lf, 90-3)

    pwm_rl = _make_pwm(PIN_RL)
    pwm_ll = _make_pwm(PIN_LL)
    pwm_ra = _make_pwm(PIN_RA)
    pwm_la = _make_pwm(PIN_LA)

    pos_rl = start_rl
    pos_ll = start_ll
    pos_ra = start_ra
    pos_la = start_la

    _set_angle(pwm_rl, pos_rl, TRIM_RL)
    _set_angle(pwm_ll, pos_ll, TRIM_LL)
    _set_angle(pwm_ra, pos_ra, TRIM_RA)
    _set_angle(pwm_la, pos_la, TRIM_LA)

    print("=== KALIBRACJA SERW ===")
    print(f"RL (pin {PIN_RL}, trim {TRIM_RL:+d}):  a/d = ±1°,  A/D = ±10°")
    print(f"LL (pin {PIN_LL}, trim {TRIM_LL:+d}):  j/l = ±1°,  J/L = ±10°")
    print(f"RA (pin {PIN_RA}, trim {TRIM_RA:+d}):  w/e = ±1°,  W/E = ±10°")
    print(f"LA (pin {PIN_LA}, trim {TRIM_LA:+d}):  s/c = ±1°,  S/C = ±10°")
    print("r = reset do 90° | p = pokaż pozycje | q = wyjście")
    print(f"Start: RL={pos_rl}°  LL={pos_ll}°  RA={pos_ra}°  LA={pos_la}°")
    print("-" * 40)

    KEYMAP = {
        'a': ('rl', -1),  'd': ('rl', +1),
        'A': ('rl', -10), 'D': ('rl', +10),
        'j': ('ll', -1),  'l': ('ll', +1),
        'J': ('ll', -10), 'L': ('ll', +10),
        'w': ('ra', -1),  'e': ('ra', +1),
        'W': ('ra', -10), 'E': ('ra', +10),
        's': ('la', -1),  'c': ('la', +1),
        'S': ('la', -10), 'C': ('la', +10),
    }

    while True:
        # Czytaj znak bez blokowania (działa w MicroPython REPL)
        if sys.stdin in select.select([sys.stdin], [], [], 0.05)[0]:
            ch = sys.stdin.read(1)
        else:
            continue

        if ch == 'q':
            print(f"[EXIT] RL={pos_rl}°  LL={pos_ll}°")
            pwm_rl.deinit()
            pwm_ll.deinit()
            pwm_rf.deinit()
            pwm_lf.deinit()
            break

        elif ch == 'r':
            pos_rl = 120
            pos_ll = 60
            pos_ra = 90
            pos_la = 90
            _set_angle(pwm_rl, pos_rl, TRIM_RL)
            _set_angle(pwm_ll, pos_ll, TRIM_LL)
            _set_angle(pwm_ra, pos_ra, TRIM_RA)
            _set_angle(pwm_la, pos_la, TRIM_LA)
            print(f"[RESET] RL=120°  LL=60°  RA=90°  LA=90°")

        elif ch == 'p':
            print(f"[POS]  RL={pos_rl}°  LL={pos_ll}°  RA={pos_ra}°  LA={pos_la}°")

        elif ch in KEYMAP:
            servo, delta = KEYMAP[ch]
            if servo == 'rl':
                pos_rl = max(0, min(180, pos_rl + delta))
                _set_angle(pwm_rl, pos_rl, TRIM_RL)
                print(f"  RL = {pos_rl:3d}°")
            elif servo == 'll':
                pos_ll = max(0, min(180, pos_ll + delta))
                _set_angle(pwm_ll, pos_ll, TRIM_LL)
                print(f"  LL = {pos_ll:3d}°")
            elif servo == 'ra':
                pos_ra = max(0, min(180, pos_ra + delta))
                _set_angle(pwm_ra, pos_ra, TRIM_RA)
                print(f"  RA = {pos_ra:3d}°")
            elif servo == 'la':
                pos_la = max(0, min(180, pos_la + delta))
                _set_angle(pwm_la, pos_la, TRIM_LA)
                print(f"  LA = {pos_la:3d}°")