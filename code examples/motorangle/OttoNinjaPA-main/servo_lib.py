import struct
import time
import json
import network  # type: ignore
import espnow   # type: ignore
from machine import Pin, PWM  # type: ignore

# --------------- KONFIGURACJA PINÓW ---------------
#                   ESP32-C3 Zero
#                      TOP VIEW
#                ____________________
#               |    USB-C           |
#               |_____________ ______|
#               | [ ] 5V      21 [ ] |
#               | [ ] GND     20 [ ] |
#               | [ ] 3.3v    19 [ ] |
#               | [ ] 0       18 [ ] |
#               | [ ] 1       10 [ ] |
#               | [ ] 2        9 [ ] |
#     (RA) CH3  | [ ] 3        8 [ ] | CH7 (LA)
#     (RL) CH2  | [ ] 4        7 [ ] | CH6 (LL)
#     (RF) CH1  | [ ] 5        6 [ ] | CH5 (LF)
#               |____________________|

# Ekrany/tryby zgodne z nadajnikiem FusionPad (mode_robot.py) - przeniesione do RobotReceiver

class NeutralPositions:
    def __init__(self):
        self.RFN = 0        # right foot neutral position
        self.RLN = 120      # right leg neutral position
        self.RAN = 90       # right arm neutral position
        self.LFN = 0        # left foot neutral position
        self.LLN = 60       # left leg neutral position
        self.LAN = 90       # left arm neutral position

        self.RLTR = 90      # right leg tilt right
        self.RLTL = 170     # right leg tilt left
        self.LLTR = 10      # left leg tilt right
        self.LLTL = 90      # left leg tilt left

        self.RLR = 25       # right leg ride position
        self.LLR = 155      # left leg ride position

        self.RFF = -16       # right foot forward speed
        self.RFB = 16        # right foot back speed
        self.LFF = 15        # left foot forward speed
        self.LFB = -16       # left foot back speed
        
        self.turn_sensitivity = 0.6  # The higher the value, the faster the outside wheel spins.
        
        # Limits for 360° servos - map joystick's full range to usefull range,
        # if servo reacts in full range of joystick drift, values should be 100
        self.JOY_DEAD     = 3
        self.LF_SERVO_MIN = -16
        self.LF_SERVO_MAX = +15
        self.RF_SERVO_MIN = -16
        self.RF_SERVO_MAX = +16
        
        # --- Indeksy serw ---
        self.RF = 0  
        self.RL = 1  
        self.RA = 2  
        self.LF = 3  
        self.LL = 4  
        self.LA = 5  

        # Adjust the pin numbers of the microcontroller to match the scheme [RF, RL, RA, LF, LL, LA]
        ################# [RF, RL, RA, LF, LL, LA] #######################
        self.servo_pins = [5, 4, 3, 6, 7, 8]
        self.continuous_servo_indices = [0, 3]  # RF, LF indices
        

class RobotReceiver:
    # --- Stałe ekranów ---
    SCREEN_MAIN = 0
    SCREEN_2 = 1
    SCREEN_3 = 2
    
    def __init__(self, espnow_instance):
        self.e = espnow_instance
        # Joystick returns values from -100 to 100
        self.lx, self.ly, self.rx, self.ry = 0, 0, 0, 0
        self.pot1 = 0
        self.screen = 0
        self.mask = 0

    def update(self):
        host, msg = self.e.recv(0)
        if msg:
            try:
                packet_type = msg[0]
                
                if packet_type == 0x01:  # CONTROL packet
                    # struct.pack('B4bBBH', 1, j1x, j1y, j2x, j2y, pot, mode, mask)
                    self.lx, self.ly, self.rx, self.ry, self.pot1, self.screen, self.mask = struct.unpack('B4bBBH', msg)[1:]
                    return 'control'
                
                elif packet_type == 0x02:  # TRIM_SYNC packet
                    # struct.pack('B6b', 2, t0, t1, t2, t3, t4, t5)
                    trim_values = struct.unpack('B6b', msg)[1:]
                    return ('trim_sync', trim_values)
                
                elif packet_type == 0x03:  # SAVE packet
                    # struct.pack('BB', 3, 1)
                    return ('save', msg[1])
                
            except:
                pass
        return None

    @property
    def bt1(self): return bool(self.mask & (1 << 0))
    @property
    def bt2(self): return bool(self.mask & (1 << 1))
    @property
    def bt3(self): return bool(self.mask & (1 << 3)) # intentionally swapped with bt4
    @property
    def bt4(self): return bool(self.mask & (1 << 2)) # intentionally swapped with bt3
    @property
    def bt5(self): return bool(self.mask & (1 << 4))
    @property
    def bt6(self): return bool(self.mask & (1 << 5))
    @property
    def bt7(self): return bool(self.mask & (1 << 6))
    @property
    def bt8(self): return bool(self.mask & (1 << 7))
    @property
    def sw3(self): return bool(self.mask & (1 << 8))
    @property
    def sw4(self): return bool(self.mask & (1 << 9))


class ServoController:
    def __init__(self, pins):
        self.servos = []
        for p in pins:
            pwm = PWM(Pin(p), freq=50)
            self.servos.append(pwm)
        self._angle_trims = {}
        self._speed_trims = {}
        self._current_angles = {}  # <- śledzenie pozycji
        self.speed_multiplier = 1.0
        self.continuous_servo_indices = []

    def set_trim_angle(self, index, delta):
        self._angle_trims[index] = delta

    def set_trim_speed(self, index, delta):
        self._speed_trims[index] = delta

    def set_angle(self, index, angle):
    # set single angle in degrees
        self._current_angles[index] = angle  # <- zapis pozycji
        angle = angle + self._angle_trims.get(index, 0)
        angle = max(0, min(180, angle))
        duty = int(((angle / 180) * (8192 - 1638)) + 1638)
        self.servos[index].duty_u16(duty)

    def set_speed(self, index, speed):
        # set speed, 0 = stop
        if index in self.continuous_servo_indices:
            speed = speed * self.speed_multiplier

        speed = speed + self._speed_trims.get(index, 0)
        speed = max(-100, min(100, speed))
        angle = int(((speed + 100) / 200) * 180)
        self.set_angle(index, angle)

    def set_speeds(self, *args):
    # set multiple speeds at once
        it = iter(args)
        for index, speed in zip(it, it):
            self.set_speed(index, speed)

    def move_to_angles(self, *args, step=2, delay=0.02):
    # Smooth movement of multiple servos simultaneously.
        pairs = []
        it = iter(args)
        for index, target in zip(it, it):
            current = self._current_angles.get(index, target)
            pairs.append((index, current, target))

        max_steps = max(int(abs(t - c) / step) for _, c, t in pairs) or 1

        for s in range(max_steps + 1):
            for index, current, target in pairs:
                angle = current + (target - current) * s / max_steps
                self.set_angle(index, int(angle))
            time.sleep(delay)

        # dokładna pozycja końcowa
        for index, _, target in pairs:
            self.set_angle(index, target)

    @staticmethod
    def map_joystick(value, joy_dead, min, max):
        if abs(value) <= joy_dead:
            return 0
        if value > 0:
            return int((value / 100) * max)
        else:
            return int((value / 100) * (-min))


class RobotConfig:
    def __init__(self):
        print("[BOOT] Inicjalizacja serwomechanizmow...")

        self.neutral_positions = NeutralPositions()
        self.RF = self.neutral_positions.RF
        self.RL = self.neutral_positions.RL
        self.RA = self.neutral_positions.RA
        self.LF = self.neutral_positions.LF
        self.LL = self.neutral_positions.LL
        self.LA = self.neutral_positions.LA

        self.servos = ServoController(self.neutral_positions.servo_pins)
        self.servos.continuous_servo_indices = self.neutral_positions.continuous_servo_indices
        print("[BOOT] ServoController OK")

        self.load_from_json()

        print("[BOOT] Uruchamianie WiFi...")
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        print("[BOOT] MAC adres:", ':'.join('%02x' % b for b in sta.config('mac')))

        print("[BOOT] Uruchamianie ESP-NOW...")
        e = espnow.ESPNow()
        e.active(True)
        self.robot = RobotReceiver(e)
        print("[BOOT] ESP-NOW gotowy, czekam na dane...")

        self.servos.set_speed(self.LF,   0)
        self.servos.set_angle(self.LL,  60)
        self.servos.set_angle(self.LA,  90)
        self.servos.set_speed(self.RF,   0)
        self.servos.set_angle(self.RL, 120)
        self.servos.set_angle(self.RA,  90)

        print("[BOOT] Serwa ustawione na pozycje startowe")
        print("[BOOT] Petla glowna start!")
        print("-" * 40)

        self._connected     = False
        self._packet_count  = 0
        self._last_warn     = 0
        self._last_packet   = time.ticks_ms()
        
        # Stan przycisków - zamiast globalnych zmiennych
        self.button_states = {
            'bt1': False, 'bt2': False, 'bt3': False, 'bt4': False,
            'bt5': False, 'bt6': False, 'bt7': False, 'bt8': False,
            'sw3': False, 'sw4': False
        }

    def handle_button_state(self, button_name, current_state, on_press, on_release=None):
        """Obsługa przycisku z wewnętrznym stanem"""
        was_pressed = self.button_states[button_name]
        result = self.handle_button(current_state, was_pressed, on_press, on_release)
        self.button_states[button_name] = result
        return result

    @staticmethod
    def handle_button(current_state, was_pressed, on_press, on_release=None):
        if current_state and not was_pressed:
            on_press()
            return True
        if not current_state and was_pressed:
            if on_release is not None:
                on_release()
            return False
        return was_pressed

    def _apply_combined_trims(self, offset_trims):
        # Sumujemy bazę z pliku z tym, co aktualnie przysłano w pakiecie
        combined = [b + o for b, o in zip(self.base_trims, offset_trims)]
        
        # Przekazujemy zsumowane wartości do sterownika serw
        self.servos.set_trim_speed(self.RF, combined[0])
        self.servos.set_trim_angle(self.RL, combined[1])
        self.servos.set_trim_angle(self.RA, combined[2])
        self.servos.set_trim_speed(self.LF, combined[3])
        self.servos.set_trim_angle(self.LL, combined[4])
        self.servos.set_trim_angle(self.LA, combined[5])
        
    def load_from_json(self):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                # Zapisujemy to jako naszą BAZĘ, której nie zmieniamy pakietami trim
                self.base_trims = config.get('servo_trims', [0, 0, 0, 0, 0, 0])
                print(f"[CONFIG] Baza wczytana: {self.base_trims}")
        except:
            self.base_trims = [-3, -8, 0, -3, 2, 0] # Twoje domyślne
        
        # Na starcie aplikujemy bazę jako aktualne trimy
        self._apply_combined_trims([0, 0, 0, 0, 0, 0])

    def save_to_json(self):
        """Zapisuje AKTUALNE (zsumowane) wartości trimów do pliku i aktualizuje bazę"""
        try:
            # 1. Pobieramy zsumowane wartości, które są obecnie w kontrolerze serw
            new_total_trims = [
                self.servos._speed_trims.get(self.RF, 0),
                self.servos._angle_trims.get(self.RL, 0),
                self.servos._angle_trims.get(self.RA, 0),
                self.servos._speed_trims.get(self.LF, 0),
                self.servos._angle_trims.get(self.LL, 0),
                self.servos._angle_trims.get(self.LA, 0)
            ]
            
            config = {'servo_trims': new_total_trims}
            
            with open('config.json', 'w') as f:
                json.dump(config, f)
            
            # --- KLUCZOWA POPRAWKA ---
            # Nowa suma staje się nową bazą w pamięci robota
            self.base_trims = new_total_trims
            # -------------------------
            
            print(f"[SAVE] Nowa baza zapisana i ustawiona: {self.base_trims}")
            return True
        except Exception as e:
            print(f"[SAVE] Błąd: {e}")
            return False

    def handle_trim_sync(self, trim_values):
        # 1. Oblicz i zaaplikuj sumę (Baza z JSON + Offset z Pilota)
        self._apply_combined_trims(trim_values)
        
        # 2. Wymuś ruch do pozycji "neutralnych" 
        # Dzięki temu widzisz efekt trimowania na żywo!
        
        # Serwa 360 (stopy) - ustawiamy speed na 0 (czyli 90 stopni + trim)
        self.servos.set_speed(self.RF, 0)
        self.servos.set_speed(self.LF, 0)
        
        # Serwa kątowe - ustawiamy ich domyślne kąty "stania"
        self.servos.set_angle(self.RL, 120)
        self.servos.set_angle(self.LL, 60)
        self.servos.set_angle(self.RA, 90)
        self.servos.set_angle(self.LA, 90)
        
        print(f"[TRIM LIVE] Offset: {trim_values}")

    def handle_save_command(self):
        """Obsługa pakietu SAVE - zapisuje konfigurację"""
        if self.save_to_json():
            print("[SAVE] Konfiguracja zapisana pomyślnie")
        else:
            print("[SAVE] Błąd zapisu konfiguracji")

    def tick(self):
        now = time.ticks_ms()

        result = self.robot.update()
        if result:
            self._packet_count += 1
            self._last_packet = now

            if not self._connected:
                self._connected = True
                print("[OK] Polaczono! Odebrano pierwszy pakiet.")

            # Obsługa różnych typów pakietów
            if result == 'control':
                # Standardowy pakiet sterowania - nic specjalnego nie robimy
                pass
            elif result[0] == 'trim_sync':
                # Pakiet synchronizacji trimów
                self.handle_trim_sync(result[1])
            elif result[0] == 'save':
                # Pakiet zapisu konfiguracji
                if result[1] == 1:
                    self.handle_save_command()

            if self._packet_count % 100 == 0 and result == 'control':
                r = self.robot
                print(f"[STATUS] Pakiety: {self._packet_count} | "
                      f"LX:{r.lx:4d} LY:{r.ly:4d} RX:{r.rx:4d} RY:{r.ry:4d} | POT1:{r.pot1}")
            return True

        else:
            # Komunikaty tylko, jeśli NAPRAWDĘ długo nie było nowych pakietów
            if time.ticks_diff(now, self._last_packet) > 3000 and time.ticks_diff(now, self._last_warn) > 3000:
                if self._connected:
                    print("[WARN] Brak danych od kontrolera...")
                else:
                    print("[WAIT] Czekam na polaczenie...")
                self._last_warn = now
            return False
