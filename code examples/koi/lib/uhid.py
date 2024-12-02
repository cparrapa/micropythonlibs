import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

__version__ = "1.0.0"

keyMap = {
"C" : Keycode.C,
"M" : Keycode.M,
"H" : Keycode.H,
"DELETE" : Keycode.DELETE,
"X" : Keycode.X,
"Y" : Keycode.Y,
"P" : Keycode.P,
"Z" : Keycode.Z,
"F" : Keycode.F,
"A" : Keycode.A,
"B" : Keycode.B,
"D" : Keycode.D,
"E" : Keycode.E,
"G" : Keycode.G,
"I" : Keycode.I,
"J" : Keycode.J,
"K" : Keycode.K,
"L" : Keycode.L,
"N" : Keycode.N,
"O" : Keycode.O,
"Q" : Keycode.Q,
"R" : Keycode.R,
"S" : Keycode.S,
"T" : Keycode.T,
"U" : Keycode.U,
"V" : Keycode.V,
"W" : Keycode.W,
"ONE" : Keycode.ONE,
"TWO" : Keycode.TWO,
"THREE" : Keycode.THREE,
"FOUR" : Keycode.FOUR,
"FIVE" : Keycode.FIVE,
"SIX" : Keycode.SIX,
"SEVEN" : Keycode.SEVEN,
"EIGHT" : Keycode.EIGHT,
"NINE" : Keycode.NINE,
"ZERO" : Keycode.ZERO,
"ENTER" : Keycode.ENTER,
"RETURN" : Keycode.RETURN,
"ESCAPE" : Keycode.ESCAPE,
"BACKSPACE" : Keycode.BACKSPACE,
"TAB" : Keycode.TAB,
"SPACEBAR" : Keycode.SPACEBAR,
"SPACE" : Keycode.SPACE,
"MINUS" : Keycode.MINUS,
"EQUALS" : Keycode.EQUALS,
"LEFT_BRACKET" : Keycode.LEFT_BRACKET,
"RIGHT_BRACKET" : Keycode.RIGHT_BRACKET,
"BACKSLASH" : Keycode.BACKSLASH,
"POUND" : Keycode.POUND,
"SEMICOLON" : Keycode.SEMICOLON,
"QUOTE" : Keycode.QUOTE,
"GRAVE_ACCENT" : Keycode.GRAVE_ACCENT,
"COMMA" : Keycode.COMMA,
"PERIOD" : Keycode.PERIOD,
"FORWARD_SLASH" : Keycode.FORWARD_SLASH,
"CAPS_LOCK" : Keycode.CAPS_LOCK,
"F1" : Keycode.F1,
"F2" : Keycode.F2,
"F3" : Keycode.F3,
"F4" : Keycode.F4,
"F5" : Keycode.F5,
"F6" : Keycode.F6,
"F7" : Keycode.F7,
"F8" : Keycode.F8,
"F9" : Keycode.F9,
"F10" : Keycode.F10,
"F11" : Keycode.F11,
"F12" : Keycode.F12,
"PRINT_SCREEN" : Keycode.PRINT_SCREEN,
"SCROLL_LOCK" : Keycode.SCROLL_LOCK,
"PAUSE" : Keycode.PAUSE,
"INSERT" : Keycode.INSERT,
"HOME" : Keycode.HOME,
"PAGE_UP" : Keycode.PAGE_UP,
"END" : Keycode.END,
"PAGE_DOWN" : Keycode.PAGE_DOWN,
"RIGHT_ARROW" : Keycode.RIGHT_ARROW,
"LEFT_ARROW" : Keycode.LEFT_ARROW,
"DOWN_ARROW" : Keycode.DOWN_ARROW,
"UP_ARROW" : Keycode.UP_ARROW,
"KEYPAD_NUMLOCK" : Keycode.KEYPAD_NUMLOCK,
"KEYPAD_FORWARD_SLASH" : Keycode.KEYPAD_FORWARD_SLASH,
"KEYPAD_ASTERISK" : Keycode.KEYPAD_ASTERISK,
"KEYPAD_MINUS" : Keycode.KEYPAD_MINUS,
"KEYPAD_PLUS" : Keycode.KEYPAD_PLUS,
"KEYPAD_ENTER" : Keycode.KEYPAD_ENTER,
"KEYPAD_ONE" : Keycode.KEYPAD_ONE,
"KEYPAD_TWO" : Keycode.KEYPAD_TWO,
"KEYPAD_THREE" : Keycode.KEYPAD_THREE,
"KEYPAD_FOUR" : Keycode.KEYPAD_FOUR,
"KEYPAD_FIVE" : Keycode.KEYPAD_FIVE,
"KEYPAD_SIX" : Keycode.KEYPAD_SIX,
"KEYPAD_SEVEN" : Keycode.KEYPAD_SEVEN,
"KEYPAD_EIGHT" : Keycode.KEYPAD_EIGHT,
"KEYPAD_NINE" : Keycode.KEYPAD_NINE,
"KEYPAD_ZERO" : Keycode.KEYPAD_ZERO,
"KEYPAD_PERIOD" : Keycode.KEYPAD_PERIOD,
"KEYPAD_BACKSLASH" : Keycode.KEYPAD_BACKSLASH,
"APPLICATION" : Keycode.APPLICATION,
"POWER" : Keycode.POWER,
"KEYPAD_EQUALS" : Keycode.KEYPAD_EQUALS,
"F13" : Keycode.F13,
"F14" : Keycode.F14,
"F15" : Keycode.F15,
"F16" : Keycode.F16,
"F17" : Keycode.F17,
"F18" : Keycode.F18,
"F19" : Keycode.F19,
"F20" : Keycode.F20,
"F21" : Keycode.F21,
"F22" : Keycode.F22,
"F23" : Keycode.F23,
"F24" : Keycode.F24,
"LEFT_CONTROL" : Keycode.LEFT_CONTROL,
"CONTROL" : Keycode.CONTROL,
"LEFT_SHIFT" : Keycode.LEFT_SHIFT,
"SHIFT" : Keycode.SHIFT,
"LEFT_ALT" : Keycode.LEFT_ALT,
"ALT" : Keycode.ALT,
"OPTION" : Keycode.OPTION,
"LEFT_GUI" : Keycode.LEFT_GUI,
"GUI" : Keycode.GUI,
"WINDOWS" : Keycode.WINDOWS,
"COMMAND" : Keycode.COMMAND,
"RIGHT_CONTROL" : Keycode.RIGHT_CONTROL,
"RIGHT_SHIFT" : Keycode.RIGHT_SHIFT,
"RIGHT_ALT" : Keycode.RIGHT_ALT,
"RIGHT_GUI" : Keycode.RIGHT_GUI,
"modifier_bit" : Keycode.modifier_bit
}

class UKeyboard:
    def __init__(self):
        #延时是必须得否则可能会无法连接电脑
        time.sleep(1)
        self.kbd = Keyboard(usb_hid.devices)
    
    def to_uppercase(self,s):
        return s.upper()
    
    def press_and_release(self,key,delay):
        key = self.to_uppercase(key)
        try:
            self.kbd.press(keyMap[key])
            time.sleep(delay)
            self.kbd.release(keyMap[key])
        except KeyError:
            print("Error:The corresponding key is not found")

    def press_key(self,key):
        key = self.to_uppercase(key)
        try:
            self.kbd.press(keyMap[key])
        except KeyError:
            print("Error:The corresponding key is not found")
    
    def release_key(self,key):
        key = self.to_uppercase(key)
        try:
            self.kbd.release(keyMap[key])
        except KeyError:
            print("Error:The corresponding key is not found")
        
    def release_all(self):
        self.kbd.release_all()

