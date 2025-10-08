'''
Tetris Game Implementation for MicroPython
Author: Iván R. Artiles
Assisted by Claude Sonnet 4 :)

A classic Tetris game implementation for microcontroller boards.
Game Features:
- Score tracking with level progression
- Line clearing mechanics
- Adaptive falling speed based on level
- Game over detection

Hardware Connections:
- OLED Display (128x64): connector 1
- Rotary Encoder:
    4 pins connector: connector 3
    3 pins connector: connector 10
- Hard Drop Button: connector 11
'''
import time
import random
from machine import Pin, SoftI2C
from ssd1306 import SSD1306_I2C

# OLED Setup
i2c = SoftI2C(sda=Pin(19), scl=Pin(18))
oled = SSD1306_I2C(128, 64, i2c)

# Encoder Setup
rot = Rotary(21, 22)
btn_enc = Pin(14, Pin.IN, Pin.PULL_UP)
btn_hard_drop = Pin(13, Pin.IN, Pin.PULL_UP)

# --- Rotary Encoder ---
class Rotary:
    def __init__(self, clk, dt):
        self.clk = Pin(clk, Pin.IN, Pin.PULL_UP)
        self.dt = Pin(dt, Pin.IN, Pin.PULL_UP)
        self.pos = 0
        self.last_status = self.clk.value()
        self.clk.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self._tick)
    
    def _tick(self, pin):
        if self.clk.value() != self.last_status:
            if self.dt.value() != self.clk.value():
                self.pos += 1
            else:
                self.pos -= 1
            self.last_status = self.clk.value()
    
    def get(self):
        if self.pos != 0:
            step = self.pos
            self.pos = 0
            return step
        return 0


class TetrisGame:
    def __init__(self):
        self.width = 10
        self.height = 16
        self.block_size = 4
        self.board_x = 24  # Center the board on screen
        self.board_y = 0
        
        # Tetris pieces (tetrominos)
        self.pieces = [
            # I-piece
            [['....', 
              '####', 
              '....', 
              '....']],
            
            # O-piece
            [['....', 
              '.##.', 
              '.##.', 
              '....']],
            
            # T-piece
            [['....', 
              '.#..', 
              '###.', 
              '....'],
             ['....', 
              '.#..', 
              '.##.', 
              '.#..'],
             ['....', 
              '....', 
              '###.', 
              '.#..'],
             ['....', 
              '.#..', 
              '##..', 
              '.#..']],
            
            # S-piece
            [['....', 
              '.##.', 
              '##..', 
              '....'],
             ['....', 
              '.#..', 
              '.##.', 
              '..#.']],
            
            # Z-piece
            [['....', 
              '##..', 
              '.##.', 
              '....'],
             ['....', 
              '..#.', 
              '.##.', 
              '.#..']],
            
            # J-piece
            [['....', 
              '#...', 
              '###.', 
              '....'],
             ['....', 
              '.##.', 
              '.#..', 
              '.#..'],
             ['....', 
              '....', 
              '###.', 
              '..#.'],
             ['....', 
              '.#..', 
              '.#..', 
              '##..']],
            
            # L-piece
            [['....', 
              '..#.', 
              '###.', 
              '....'],
             ['....', 
              '.#..', 
              '.#..', 
              '.##.'],
             ['....', 
              '....', 
              '###.', 
              '#...'],
             ['....', 
              '##..', 
              '.#..', 
              '.#..']]
        ]
        
        self.reset_game()
    
    def reset_game(self):
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.game_over = False
        self.spawn_piece()
        self.fall_time = 0
        self.fall_speed = 500  # milliseconds
        
    def spawn_piece(self):
        self.current_piece = random.choice(self.pieces)
        self.current_rotation = 0
        self.piece_x = self.width // 2 - 2
        self.piece_y = 0
        
        # Check if game over
        if self.check_collision(self.piece_x, self.piece_y, self.current_rotation):
            self.game_over = True
    
    def get_current_piece(self):
        return self.current_piece[self.current_rotation]
    
    def check_collision(self, x, y, rotation):
        piece = self.current_piece[rotation]
        for py in range(4):
            for px in range(4):
                if piece[py][px] == '#':
                    new_x = x + px
                    new_y = y + py
                    
                    # Check boundaries
                    if (new_x < 0 or new_x >= self.width or 
                        new_y >= self.height):
                        return True
                    
                    # Check collision with placed pieces
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return True
        return False
    
    def place_piece(self):
        piece = self.get_current_piece()
        for py in range(4):
            for px in range(4):
                if piece[py][px] == '#':
                    board_x = self.piece_x + px
                    board_y = self.piece_y + py
                    if board_y >= 0:
                        self.board[board_y][board_x] = 1
        
        # Check for completed lines
        self.clear_lines()
        self.spawn_piece()
    
    def clear_lines(self):
        lines_to_clear = []
        for y in range(self.height):
            if all(self.board[y]):
                lines_to_clear.append(y)
        
        for y in lines_to_clear:
            del self.board[y]
            self.board.insert(0, [0 for _ in range(self.width)])
        
        lines_cleared = len(lines_to_clear)
        self.lines_cleared += lines_cleared
        self.score += lines_cleared * 100 * self.level
        
        # Increase level every 10 lines
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(100, 500 - (self.level - 1) * 50)
    
    def move_left(self):
        if not self.check_collision(self.piece_x - 1, self.piece_y, self.current_rotation):
            self.piece_x -= 1
    
    def move_right(self):
        if not self.check_collision(self.piece_x + 1, self.piece_y, self.current_rotation):
            self.piece_x += 1
    
    def rotate(self):
        new_rotation = (self.current_rotation + 1) % len(self.current_piece)
        if not self.check_collision(self.piece_x, self.piece_y, new_rotation):
            self.current_rotation = new_rotation
    
    def drop(self):
        if not self.check_collision(self.piece_x, self.piece_y + 1, self.current_rotation):
            self.piece_y += 1
            return True
        else:
            self.place_piece()
            return False
    
    def hard_drop(self):
        while self.drop():
            pass
    
    def update(self, dt):
        if self.game_over:
            return
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            self.drop()
            self.fall_time = 0
    
    def draw(self):
        oled.fill(0)
        
        if self.game_over:
            oled.text("GAME OVER", 30, 15, 1)
            oled.text("Score:" + str(self.score), 30, 30, 1)
            oled.text("Lines:" + str(self.lines_cleared), 30, 40, 1)
            oled.text("Press button", 20, 50, 1)
        else:
            # Draw board border
            border_x = self.board_x - 1
            border_y = self.board_y - 1
            border_w = self.width * self.block_size + 2
            border_h = min(16, self.height) * self.block_size + 2
            oled.rect(border_x, border_y, border_w, border_h, 1)
            
            # Draw placed pieces (only visible portion)
            for y in range(min(16, self.height)):
                for x in range(self.width):
                    if self.board[y][x]:
                        px = self.board_x + x * self.block_size
                        py = self.board_y + y * self.block_size
                        oled.fill_rect(px, py, self.block_size, self.block_size, 1)
            
            # Draw current piece
            piece = self.get_current_piece()
            for py in range(4):
                for px in range(4):
                    if piece[py][px] == '#':
                        screen_x = self.board_x + (self.piece_x + px) * self.block_size
                        screen_y = self.board_y + (self.piece_y + py) * self.block_size
                        if screen_y >= 0 and screen_y < 64:  # Only draw visible parts
                            oled.fill_rect(screen_x, screen_y, self.block_size, self.block_size, 1)
            
            # Draw UI
            oled.text(str(self.score), 0, 0, 1)
            oled.text("L" + str(self.level), 0, 10, 1)
            oled.text(str(self.lines_cleared), 0, 20, 1)
            
            # Draw controls hint
            oled.text("Turn:Move", 65, 0, 1)
            oled.text("14:Rotate", 65, 10, 1)
            oled.text("13:Drop", 72, 20, 1)
        
        oled.show()

def main():
    game = TetrisGame()
    last_time = time.ticks_ms()
    
    # Button state tracking for debouncing
    last_btn_enc = True
    last_btn_hard_drop = True
    btn_enc_time = 0
    btn_hard_drop_time = 0
    
    print("Tetris Game Started!")
    print("Controls:")
    print("- Rotary Encoder (pins 21,22): Turn left/right to move piece")
    print("- Encoder Button (pin 14): Press to rotate, hold for soft drop")
    print("- Hard Drop Button (pin 13): Instant drop to bottom")
    
    while True:
        current_time = time.ticks_ms()
        dt = time.ticks_diff(current_time, last_time)
        last_time = current_time
        
        # Read encoder rotation
        encoder_step = rot.get()
        
        # Read buttons
        btn_enc_val = btn_enc.value()
        btn_hard_drop_val = btn_hard_drop.value()
        
        if not game.game_over:
            # Handle encoder rotation - move piece left/right
            if encoder_step != 0:
                if encoder_step > 0:
                    # Clockwise rotation - move right
                    for _ in range(abs(encoder_step)):
                        game.move_right()
                else:
                    # Counter-clockwise rotation - move left
                    for _ in range(abs(encoder_step)):
                        game.move_left()
            
            # Handle encoder button press
            if not btn_enc_val and last_btn_enc and time.ticks_diff(current_time, btn_enc_time) > 200:
                # Quick press - rotate piece
                game.rotate()
                btn_enc_time = current_time
            
            # Handle encoder button hold - soft drop (continuous)
            if not btn_enc_val and time.ticks_diff(current_time, btn_enc_time) > 300:
                # Long press - soft drop repeatedly
                if time.ticks_diff(current_time, btn_enc_time) % 100 < 50:  # Drop every 100ms while held
                    game.drop()
            
            # Handle hard drop button - instant drop to bottom
            if not btn_hard_drop_val and last_btn_hard_drop and time.ticks_diff(current_time, btn_hard_drop_time) > 150:
                game.hard_drop()
                btn_hard_drop_time = current_time
            
            game.update(dt)
        
        else:
            # Game over - restart on any button press
            if (not btn_enc_val and last_btn_enc) or (not btn_hard_drop_val and last_btn_hard_drop):
                game.reset_game()
                time.sleep_ms(300)  # Debounce
        
        # Update button states
        last_btn_enc = btn_enc_val
        last_btn_hard_drop = btn_hard_drop_val
        
        game.draw()
        time.sleep_ms(50)

# Demo mode for testing without buttons
def demo_mode():
    oled.fill(0)
    oled.text("Tetris Demo", 30, 10, 1)
    oled.text("Auto-play mode", 20, 25, 1)
    oled.text("Turn encoder to", 10, 40, 1)
    oled.text("move left/right", 10, 50, 1)
    oled.show()
    time.sleep(3)
    
    # Show some tetris pieces
    pieces = ['####', '.##.', '.##.', '....']
    for i in range(5):
        oled.fill(0)
        oled.text("Tetris pieces:", 10, 0, 1)
        
        # Draw a simple piece animation
        for j, line in enumerate(pieces):
            y = 15 + j * 8
            for k, char in enumerate(line):
                if char == '#':
                    x = 30 + k * 8 + (i * 5)
                    oled.fill_rect(x, y, 6, 6, 1)
        
        oled.show()
        time.sleep(0.5)

if __name__ == "__main__":
    try:
        # Uncomment for demo mode
        # demo_mode()
        # Main game
        main()
    except KeyboardInterrupt:
        print("Game stopped")
        oled.fill(0)
        oled.text("Tetris Stopped", 20, 30, 1)
        oled.show()