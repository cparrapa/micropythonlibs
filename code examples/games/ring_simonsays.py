import machine
import neopixel
import time
import random
import uos

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    try:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
    except:
        print("⚠️ Failed to save high score")


# === CONFIG ===
NEOPIXEL_PIN = 4
NUM_LEDS = 13
BUTTON_PINS = [13, 14, 15, 27]  # R, G, B, Y
BUZZER_PIN = 25
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]  # RGBY
TONE_FREQS = [440, 523, 659, 784]  # A4, C5, E5, G5

# === SETUP ===
np = neopixel.NeoPixel(machine.Pin(NEOPIXEL_PIN), NUM_LEDS)
buttons = [machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP) for pin in BUTTON_PINS]
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
buzzer.duty(0)  # off

# === LED FUNCTIONS ===
def show_power_led():
    np[0] = (100, 100, 100)  # White center LED
    np.write()

def clear_ring(delay=0):
    time.sleep(delay)
    for i in range(1, NUM_LEDS):
        np[i] = (0, 0, 0)
    np.write()

    
COLOR_LED_MAP = {
    0: [2, 3, 4],    # Red
    1: [5, 6, 7],    # Green
    2: [8, 9, 10],   # Blue
    3: [11, 12, 1]   # Yellow (wraps around)
}

def show_color(index, color, brightness=0.3):
    dimmed = tuple(int(c * brightness) for c in color)
    for led_index in COLOR_LED_MAP[index]:
        np[led_index] = dimmed
    np.write()


def flash_color(index, duration=0.4, play_sound=True):
    show_color(index, COLORS[index])
    if play_sound:
        play_tone(index)
    time.sleep(duration)
    clear_ring()
    if play_sound:
        stop_tone()
    time.sleep(0.1)

def update_score_leds(score):
    leds_on = min(score, 12)
    purple = (50, 0, 50)
    for i in range(1, 13):
        np[i] = purple if i <= leds_on else (0, 0, 0)
    np.write()


# === BUZZER FUNCTIONS ===
def play_tone(index):
    freq = TONE_FREQS[index]
    buzzer.freq(freq)
    buzzer.duty(200)

def stop_tone():
    buzzer.duty(0)

def error_sound():
    buzzer.freq(150)
    buzzer.duty(300)
    time.sleep(0.4)
    buzzer.duty(0)

def victory_jingle():
    melody = [659, 784, 988, 1046, 784, 659]  # A5, G5, B5, C6, G5, A5
    for f in melody:
        buzzer.freq(f)
        buzzer.duty(200)
        time.sleep(0.15)
    buzzer.duty(0)


# === INPUT HANDLING ===
def wait_for_button():
    while True:
        for i, button in enumerate(buttons):
            if button.value() == 0:
                time.sleep(0.05)
                if button.value() == 0:
                    while button.value() == 0:
                        time.sleep(0.01)
                    return i
        time.sleep(0.01)

# === SEQUENCE LOGIC ===
def play_sequence(seq):
    for index in seq:
        flash_color(index, duration=0.4)

def play_level_up_sound():
    melody = [523, 659]  # C5, E5
    for f in melody:
        buzzer.freq(f)
        buzzer.duty(200)
        time.sleep(0.15)
    buzzer.duty(0)


# === GAME MODES ===
def single_player_mode():
    print("Starting Simon Game - Single Player")
    level = 0
    sequence = []
    high_score = load_high_score()

    while True:
        level += 1
        print(f"\nLevel {level}")
        sequence.append(random.randint(0, 3))

        play_sequence(sequence)

        for expected in sequence:
            pressed = wait_for_button()
            flash_color(pressed, duration=0.15)  # Fast feedback!
            if pressed != expected:
                print("❌ Wrong button! Game Over")
                error_sound()
                game_over_effect()
                if level - 1 > high_score:
                    print("🏆 New High Score!", level - 1)
                    save_high_score(level - 1)
                else:
                    print("📊 Score:", level - 1, "| High Score:", high_score)
                return

        # Player completed sequence successfully
        print("✅ Correct!")
        update_score_leds(level)
        play_level_up_sound()
        time.sleep(1)
        clear_ring()


def multiplayer_mode():
    print("Starting Simon Game - Multiplayer")
    sequence = []
    current_player = 1

    while True:
        print(f"\nPlayer {current_player}'s turn!")
        play_sequence(sequence)

        for expected in sequence:
            pressed = wait_for_button()
            flash_color(pressed, 0.2)
            if pressed != expected:
                print(f"❌ Player {current_player} failed!")
                error_sound()
                game_over_effect()
                print(f"🏆 Player {3 - current_player} wins!")
                victory_jingle()
                return

        # Add a new random step and switch players
        new_step = random.randint(0, 3)
        print(f"Player {current_player} adds: {new_step}")
        sequence.append(new_step)
        flash_color(new_step, 0.2)
        current_player = 3 - current_player  # Toggle between 1 and 2
        time.sleep(1)

def game_over_effect():
    for _ in range(3):
        for i in range(4):
            show_color(i, (255, 0, 0), 0.2)
        np.write()
        time.sleep(0.3)
        clear_ring()
        time.sleep(0.3)

# === MAIN ===
show_power_led()
clear_ring(delay=0.2)
time.sleep(1)

print("🕹️ Press RED to play single-player.")
print("👥 Press GREEN to play multiplayer.")

while True:
    np[3] = (255, 100, 0)  # orange for single
    np[6] = (0, 255, 100)  # cyan for multi
    np.write()
    choice = wait_for_button()
    if choice == 0:
        np[3] = (255, 0, 0) 
        np.write()
        time.sleep(0.2)
        clear_ring()
        single_player_mode()
    elif choice == 1:
        np[6] = (0, 255, 0) 
        np.write()
        time.sleep(0.2)
        clear_ring()
        multiplayer_mode()
    
    # After a game ends
    print("\n🔁 Game Over. Press RED or GREEN to play again.")
    clear_ring()
    update_score_leds(0)
