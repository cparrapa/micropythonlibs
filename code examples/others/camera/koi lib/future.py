import displayio
import digitalio
import analogio
import pwmio
import board
from busio import UART
import math
from time import sleep,monotonic_ns
from adafruit_display_shapes.rect import Rect
from board_map import usePin, saveObj, checkObj

__version__ = "1.1.0"

# display = board.DISPLAY
board.DISPLAY.auto_refresh = False
servo_pins = {}

noteMap = [440, 494, 262, 294, 330, 349, 392]

uartMap = {
    "uart0":("RX","TX"),
    "uart1":("RX1","TX1"),
}

CORRECT = "c6:1 f6:2"
NOTICE = "d5:1 b4:1"
ERROR = "a3:2 r a3:2"
DADA = "r4:2 g g g eb:8 r:2 f f f d:8 "
ENTERTAINER = "d4:1 d# e c5:2 e4:1 c5:2 e4:1 c5:3 c:1 d d# e c d e:2 b4:1 d5:2 c:4 "
PRELUDE = "c4:1 e g c5 e g4 c5 e c4 e g c5 e g4 c5 e c4 d g d5 f g4 d5 f c4 d g d5 f g4 d5 f b3 d4 g d5 f g4 d5 f b3 d4 g d5 f g4 d5 f c4 e g c5 e g4 c5 e c4 e g c5 e g4 c5 e "
ODE = "e4 e f g g f e d c c d e e:6 d:2 d:8 e:4 e f g g f e d c c d e d:6 c:2 c:8 "
NYAN = "f#5:2 g# c#:1 d#:2 b4:1 d5:1 c# b4:2 b c#5 d d:1 c# b4:1 c#5:1 d# f# g# d# f# c# d b4 c#5 b4 d#5:2 f# g#:1 d# f# c# d# b4 d5 d# d c# b4 c#5 d:2 b4:1 c#5 d# f# c# d c# b4 c#5:2 b4 c#5 b4 f#:1 g# b:2 f#:1 g# b c#5 d# b4 e5 d# e f# b4:2 b f#:1 g# b f# e5 d# c# b4 f# d# e f# b:2 f#:1 g# b:2 f#:1 g# b b c#5 d# b4 f# g# f# b:2 b:1 a# b f# g# b e5 d# e f# b4:2 c#5 "
RING = "c4:1 d e:2 g d:1 e f:2 a e:1 f g:2 b c5:4 "
FUNK = "c2:2 c d# c:1 f:2 c:1 f:2 f# g c c g c:1 f#:2 c:1 f#:2 f d# "
BLUES = "c2:2 e g a a# a g e c2:2 e g a a# a g e f a c3 d d# d c a2 c2:2 e g a a# a g e g b d3 f f2 a c3 d# c2:2 e g e g f e d "
BIRTHDAY = "c4:3 c:1 d:4 c:4 f e:8 c:3 c:1 d:4 c:4 g f:8 c:3 c:1 c5:4 a4 f e d a#:3 a#:1 a:4 f g f:8 "
WEDDING = "c4:4 f:3 f:1 f:8 c:4 g:3 e:1 f:8 c:4 f:3 a:1 c5:4 a4:3 f:1 f:4 e:3 f:1 g:8 "
FUNERAL = "c3:4 c:3 c:1 c:4 d#:3 d:1 d:3 c:1 c:3 b2:1 c3:4 "
PUNCHLINE = "c4:3 g3:1 f# g g#:3 g r b c4 "
BADDY = "c3:3 r d:2 d# r c r f#:8 "
CHASE = "a4:1 b c5 b4 a:2 r a:1 b c5 b4 a:2 r a:2 e5 d# e f e d# e b4:1 c5 d c b4:2 r b:1 c5 d c b4:2 r b:2 e5 d# e f e d# e "
BA_DING = "b5:1 e6:3 "
WAWA = "e3:3 r:1 d#:3 r:1 d:4 r:1 c#:8 "
JUMP_UP = "c5:1 d e f g "
JUMP_DOWN = "g5:1 f e d c "
POWER_UP = "g4:1 c5 e g:2 e:1 g:3 "
POWER_DOWN = "g5:1 d# c g4:2 b:1 c5:3 "

melodyMap = ['',CORRECT,ERROR,NOTICE,BA_DING,JUMP_UP,JUMP_DOWN,POWER_UP,POWER_DOWN,BADDY,DADA, \
    WAWA,PUNCHLINE,RING,FUNK,ENTERTAINER,ODE,WEDDING,BIRTHDAY,CHASE,BLUES,PRELUDE,NYAN,FUNERAL]

font_5 = b'\x00\x00\x00\x00\x00\x00\x17\x00\x00\x00\x00\x03\x00\x03\x00\n\x1f\n\x1f\n\n\x17\x15\x1d\n\x13\t\x04\x12\x19\n\x15\x15\n\x10\x00\x03\x00\x00\x00\x00\x0e\x11\x00\x00\x00\x11\x0e\x00\x00\x00\n\x04\n\x00\x00\x04\x0e\x04\x00\x00\x10\x08\x00\x00\x00\x04\x04\x04\x00\x00\x08\x00\x00\x00\x10\x08\x04\x02\x01\x0e\x11\x11\x0e\x00\x00\x12\x1f\x10\x00\x19\x15\x15\x12\x00\t\x11\x15\x0b\x00\x0c\n\t\x1f\x08\x17\x15\x15\x15\t\x08\x14\x16\x15\x08\x11\t\x05\x03\x01\n\x15\x15\x15\n\x02\x15\r\x05\x02\x00\n\x00\x00\x00\x00\x10\n\x00\x00\x00\x04\n\x11\x00\x00\n\n\n\x00\x00\x11\n\x04\x00\x02\x01\x15\x05\x02\x0e\x11\x15\t\x0e\x1e\x05\x05\x1e\x00\x1f\x15\x15\n\x00\x0e\x11\x11\x11\x00\x1f\x11\x11\x0e\x00\x1f\x15\x15\x11\x00\x1f\x05\x05\x01\x00\x0e\x11\x11\x15\x0c\x1f\x04\x04\x1f\x00\x11\x1f\x11\x00\x00\t\x11\x11\x0f\x01\x1f\x04\n\x11\x00\x1f\x10\x10\x10\x00\x1f\x02\x04\x02\x1f\x1f\x02\x04\x08\x1f\x0e\x11\x11\x0e\x00\x1f\x05\x05\x02\x00\x06\t\x19\x16\x00\x1f\x05\x05\n\x10\x12\x15\x15\t\x00\x01\x01\x1f\x01\x01\x0f\x10\x10\x0f\x00\x07\x08\x10\x08\x07\x1f\x08\x04\x08\x1f\x1b\x04\x04\x1b\x00\x01\x02\x1c\x02\x01\x19\x15\x13\x11\x00\x00\x1f\x11\x11\x00\x01\x02\x04\x08\x10\x00\x11\x11\x1f\x00\x00\x02\x01\x02\x00\x10\x10\x10\x10\x10\x00\x01\x02\x00\x00\x0c\x12\x12\x1e\x10\x1f\x14\x14\x08\x00\x0c\x12\x12\x12\x00\x08\x14\x14\x1f\x00\x0e\x15\x15\x12\x00\x04\x1e\x05\x01\x00\x02\x15\x15\x0f\x00\x1f\x04\x04\x18\x00\x00\x1d\x00\x00\x00\x00\x10\x10\r\x00\x1f\x04\n\x10\x00\x00\x0f\x10\x10\x00\x1e\x02\x04\x02\x1e\x1e\x02\x02\x1c\x00\x0c\x12\x12\x0c\x00\x1e\n\n\x04\x00\x04\n\n\x1e\x00\x1c\x02\x02\x02\x00\x10\x14\n\x02\x00\x00\x0f\x14\x14\x10\x0e\x10\x10\x1e\x10\x06\x08\x10\x08\x06\x1e\x10\x08\x10\x1e\x12\x0c\x0c\x12\x00\x12\x14\x08\x04\x02\x12\x1a\x16\x12\x00\x00\x04\x1f\x11\x00\x00\x1f\x00\x00\x00\x11\x1f\x04\x00\x00\x00\x04\x04\x08\x08'
font_8 = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x5F\x00\x00\x00\x00\x00\x00\x07\x00\x07\x00\x00\x00\x00\x14\x7F\x14\x7F\x14\x00\x00\x00\x24\x2E\x7B\x2A\x12\x00\x00\x00\x23\x13\x08\x64\x62\x00\x00\x00\x36\x49\x56\x20\x50\x00\x00\x00\x00\x04\x03\x01\x00\x00\x00\x00\x00\x1C\x22\x41\x00\x00\x00\x00\x00\x41\x22\x1C\x00\x00\x00\x00\x22\x14\x7F\x14\x22\x00\x00\x00\x08\x08\x7F\x08\x08\x00\x00\x00\x40\x30\x10\x00\x00\x00\x00\x00\x08\x08\x08\x08\x08\x00\x00\x00\x00\x60\x60\x00\x00\x00\x00\x00\x20\x10\x08\x04\x02\x00\x00\x00\x3E\x51\x49\x45\x3E\x00\x00\x00\x00\x42\x7F\x40\x00\x00\x00\x00\x62\x51\x49\x49\x46\x00\x00\x00\x21\x41\x49\x4D\x33\x00\x00\x00\x18\x14\x12\x7F\x10\x00\x00\x00\x27\x45\x45\x45\x39\x00\x00\x00\x3C\x4A\x49\x49\x31\x00\x00\x00\x01\x71\x09\x05\x03\x00\x00\x00\x36\x49\x49\x49\x36\x00\x00\x00\x46\x49\x49\x29\x1E\x00\x00\x00\x00\x36\x36\x00\x00\x00\x00\x00\x40\x36\x36\x00\x00\x00\x00\x00\x08\x14\x22\x41\x00\x00\x00\x00\x14\x14\x14\x14\x14\x00\x00\x00\x00\x41\x22\x14\x08\x00\x00\x00\x02\x01\x59\x05\x02\x00\x00\x00\x3E\x41\x5D\x55\x5E\x00\x00\x00\x7C\x12\x11\x12\x7C\x00\x00\x00\x7F\x49\x49\x49\x36\x00\x00\x00\x3E\x41\x41\x41\x22\x00\x00\x00\x7F\x41\x41\x41\x3E\x00\x00\x00\x7F\x49\x49\x49\x41\x00\x00\x00\x7F\x09\x09\x09\x01\x00\x00\x00\x3E\x41\x51\x51\x72\x00\x00\x00\x7F\x08\x08\x08\x7F\x00\x00\x00\x00\x41\x7F\x41\x00\x00\x00\x00\x20\x40\x41\x3F\x01\x00\x00\x00\x7F\x08\x14\x22\x41\x00\x00\x00\x7F\x40\x40\x40\x40\x00\x00\x00\x7F\x02\x0C\x02\x7F\x00\x00\x00\x7F\x04\x08\x10\x7F\x00\x00\x00\x3E\x41\x41\x41\x3E\x00\x00\x00\x7F\x09\x09\x09\x06\x00\x00\x00\x3E\x41\x51\x21\x5E\x00\x00\x00\x7F\x09\x19\x29\x46\x00\x00\x00\x26\x49\x49\x49\x32\x00\x00\x00\x01\x01\x7F\x01\x01\x00\x00\x00\x3F\x40\x40\x40\x3F\x00\x00\x00\x1F\x20\x40\x20\x1F\x00\x00\x00\x7F\x20\x18\x20\x7F\x00\x00\x00\x63\x14\x08\x14\x63\x00\x00\x00\x03\x04\x78\x04\x03\x00\x00\x00\x61\x51\x49\x45\x43\x00\x00\x00\x7F\x7F\x41\x41\x00\x00\x00\x00\x02\x04\x08\x10\x20\x00\x00\x00\x00\x41\x41\x7F\x7F\x00\x00\x00\x04\x02\x7F\x02\x04\x00\x00\x00\x08\x1C\x2A\x08\x08\x00\x00\x00\x00\x00\x01\x02\x04\x00\x00\x00\x24\x54\x54\x38\x40\x00\x00\x00\x7F\x28\x44\x44\x38\x00\x00\x00\x38\x44\x44\x44\x08\x00\x00\x00\x38\x44\x44\x28\x7F\x00\x00\x00\x38\x54\x54\x54\x08\x00\x00\x00\x08\x7E\x09\x09\x02\x00\x00\x00\x98\xA4\xA4\xA4\x78\x00\x00\x00\x7F\x08\x04\x04\x78\x00\x00\x00\x00\x00\x79\x00\x00\x00\x00\x00\x00\x80\x88\x79\x00\x00\x00\x00\x7F\x10\x28\x44\x40\x00\x00\x00\x00\x41\x7F\x40\x00\x00\x00\x00\x78\x04\x78\x04\x78\x00\x00\x00\x04\x78\x04\x04\x78\x00\x00\x00\x38\x44\x44\x44\x38\x00\x00\x00\xFC\x24\x24\x24\x18\x00\x00\x00\x18\x24\x24\x24\xFC\x00\x00\x00\x04\x78\x04\x04\x08\x00\x00\x00\x48\x54\x54\x54\x24\x00\x00\x00\x04\x3F\x44\x44\x24\x00\x00\x00\x3C\x40\x40\x3C\x40\x00\x00\x00\x1C\x20\x40\x20\x1C\x00\x00\x00\x3C\x40\x3C\x40\x3C\x00\x00\x00\x44\x28\x10\x28\x44\x00\x00\x00\x9C\xA0\xA0\x90\x7C\x00\x00\x00\x44\x64\x54\x4C\x44\x00\x00\x00\x08\x36\x41\x00\x00\x00\x00\x00\x00\x00\x77\x00\x00\x00\x00\x00\x00\x00\x41\x36\x08\x00\x00\x00\x08\x04\x08\x10\x08\x00\x00\x00\x55\x2A\x55\x2A\x55\x00\x00'
pinMap = {
    "P1":board.P1,
    "P2":board.P2,
    "P3":board.P3,
    "P4":board.P4,
    "NEOPIX":board.NEOPIX
}



class Matrix:
    def __init__(self):
        self.matrix = None

    def init(self,x,y):
        board.DISPLAY.rotation = 90
        instance = 'matrix_{}_{}'.format(x,y)
        if self.matrix:
            del self.matrix
        self._x = x
        self._y = y
        self._pixlen = x*y
        if x == 5:
            self.font = font_5
        elif x == 8:
            self.font = font_8
        self._col0 = 0x323232
        self._col1 = 0xff0000
        self.matrix = displayio.Group()
        n = 120 // y
        for y in range(self._x):
            for x in range(self._y):
                _pix = Rect(22 + x*n, 6 + y*n, n-4, n-4, fill=self._col0)
                self.matrix.append(_pix)
        board.DISPLAY.show(self.matrix)
        board.DISPLAY.refresh()
        Screen.mode = instance

    def pix(self, x, y, color=255, refresh=True):
        if color!= 0:
            color = color << 16
        else:
            color = 0x323232
        if x > self._x-1 or y > self._y-1:
            print("Out of maximum coordinates")
            return
        self.matrix[y*self._x+x].fill = color
        board.DISPLAY.refresh()

    def showary(self, img):
        if len(img) == self._pixlen:
            for n in range(self._pixlen):
                if img[n]:
                    self.pix(n % self._y, int(n / self._x), 255, False)
                else:
                    self.pix(n % self._y, int(n / self._x), 0, False)
        elif len(img) == self._y:
            for x in range(self._y):
                for y in range(self._x):
                    if img[x] & (1 << y):
                        self.pix(x, y, 255, False)
                    else:
                        self.pix(x, y, 0, False)
        board.DISPLAY.refresh()

    def scroll(self, txt, delay=0.1):
        if len(txt) == 1:
            code = (ord(txt[0]) - 32) * self._y
            self.showary(self.font[code : code + self._x])
        elif len(txt) > 1:
            txt += " "
            sleep(delay)
            for n in range(len(txt) - 1):
                code = (ord(txt[n]) - 32) * self._y
                code1 = (ord(txt[n + 1]) - 32) * self._x
                tmp = self.font[code : code + self._y] + self.font[code1 : code1 + self._y]
                for bias in range(self._y):
                    self.showary(tmp[bias : bias + self._y])
                    sleep(delay)
            self.showary([0, 0, 0, 0, 0])

    def show(self, t):
        if len(t) == self._pixlen:
            self.showary(t)
        if type(t) == str:
            self.scroll(t)

    def clear(self):
        self.showary([0]*self._y)



class Buzz():
    def __init__(self):
        self.pwm = pwmio.PWMOut(usePin("BUZZ"), frequency=250, variable_frequency=True)
        saveObj("BUZZ",self.pwm)
        self.playing = 0
        self.volume = 30
        self.pwm.duty_cycle = 0

    def tone(self, freq, d=0.5):  
        if freq == 0:
            sleep(d)
            return
        self.pwm.frequency = freq
        self.pwm.duty_cycle = 0x8000
        if d == -1:
            return
        else:
            sleep(d)
            self.pwm.duty_cycle = 0

    def note(self, note, rest=0.5):
        freq = int(440.0*math.pow(2, (note-69)/12))
        self.tone(freq,rest)

    def rest(self, rest):
        sleep(rest)

    def melody(self,m,bpm=125):
        if type(m) == int:
            m = melodyMap[m]
        m = m.lower()
        if not m.endswith(' '):
            m = m+' '
        octave = 4
        n = 0
        tnote = 60.0/bpm/4
        duration=0.5
        self.playing = 1
        while n < len(m):
            if not self.playing:
                return
            note = ord(m[n])
            if note >= ord('a') and note <= ord('g'):
                freq = noteMap[note-ord('a')]
            elif note == ord('r'):
                freq = 0
            elif note >= ord('2') and note <= ord('6'):
                octave = note - ord('0')
            elif note == ord(':'):
                n+=1
                note = ord(m[n])
                duration = (note - ord('0'))*tnote
            elif note == ord(' '):
                freq *= pow(2, octave-4)
                self.tone(int(freq), duration)
            n+=1

    def stop(self):
        self.playing = 0
        self.pwm.duty_cycle = 0


pinModeMap = {
    'IN': 'DigitalInOut',
    'OUT': 'DigitalInOut',
    'ANALOG': 'AnalogIn',
    'PWM': 'PWMOut'
}

class MeowPin:

    def __init__(self, port, mode='OUT'):
        self.mode = mode
        self.port = port
        self.p = self.setMode()
        saveObj(self.port,self.p)
        
    def setMode(self):
        if self.mode == 'IN':
            return digitalio.DigitalInOut(usePin(self.port))
        elif self.mode == 'OUT':
            return digitalio.DigitalInOut(usePin(self.port))
        elif self.mode == 'ANALOG':
            return analogio.AnalogIn(usePin(self.port))
        elif self.mode == 'PWM':
            return pwmio.PWMOut(usePin(self.port), frequency=50, variable_frequency=True)
     
    def getAnalog(self):
        return min(int(self.p.value/15.009),4095)   

    def getDigital(self):
        if self.p.direction == digitalio.Direction.OUTPUT:
            self.p.switch_to_input()
        return self.p.value

    def setDigital(self, v):
        if self.p.direction == digitalio.Direction.INPUT:
            self.p.switch_to_output()
        self.p.value = v
    
    def setFrequency(self,hz):
        hz = max(min(122,hz),1)
        if self.mode != 'PWM':
            pass
        elif self.mode == 'PWM':
            self.p.frequency = hz
        else:
            pass


    def setAnalog(self, v):
        v = max(min(4095,v),0)
        self.p.duty_cycle = v<<4

    # def read(self):
    #     if self.adc:
    #         return self.adc.value
    #     elif self.p:
    #         return self.p.value

    # def write(self, v):
    #     if self.pwm:
    #         self.pwm.duty_cycle = v
    #     elif self.p:
    #         self.p.value = v

    # def set_pulse_width(self, v):
    #     v = round(v / 200, 1)
    #     if v < 0:
    #         raise Exception("Analog value should > 0")
    #     if self.pwm:
    #         self.pwm.duty_cycle = v


"""""""""""""""""""""""""""
Actuator  
"""""""""""""""""""""""""""

def initialize_servo(pin):
    if not isinstance(checkObj(pin), pwmio.PWMOut):
        servopin = pwmio.PWMOut(usePin(pin), frequency=50)
        saveObj(pin,servopin)
        servo_pins[pin] = servopin      

def servo(pin,value):
    initialize_servo(pin)
    servopin = servo_pins[pin]
    angle = int((value / 180 * 2 + 0.5) / 20 * 65535)
    servopin.duty_cycle = angle

def geekservo9g(pin,value):
    initialize_servo(pin)
    servopin = servo_pins[pin]
    value = (value+45)/1.5
    angle = int((value / 180 * 2 + 0.5) / 20 * 65535)
    servopin.duty_cycle = angle


class Motor:
    def __init__(self):
        self.m1an = pwmio.PWMOut(usePin("M1AN"))
        self.m1ap = pwmio.PWMOut(usePin("M1AP"))
        self.m1bn = pwmio.PWMOut(usePin("M1BN"))
        self.m1bp = pwmio.PWMOut(usePin("M1BP"))
        saveObj("M1AN",self.m1an)
        saveObj("M1AP",self.m1ap)
        saveObj("M1BN",self.m1bn)
        saveObj("M1BP",self.m1bp)
        
    
    def setSpeed(self,port,value,second=0):
        value = max(min(100,value),-100)
        value = int(value * 655.35)
        port1 = None
        port2 = None
        if port == 1:
            port1 = self.m1an
            port2 = self.m1ap
        else:
            port1 = self.m1bn
            port2 = self.m1bp
        if value >= 0:
            port1.duty_cycle = value
            port2.duty_cycle = 0
        else:
            port1.duty_cycle = 0
            port2.duty_cycle = abs(value)
        second = max(0,second)
        if second == 0:
            pass
        else:
            sleep(second)
            port1.duty_cycle = 0
            port2.duty_cycle = 0

    def stopMotor(self,port):
        if port == 1:
            self.m1an.duty_cycle = 0
            self.m1ap.duty_cycle = 0
        elif port == 2:
            self.m1bn.duty_cycle = 0
            self.m1bp.duty_cycle = 0
        else:
            self.m1an.duty_cycle = 0
            self.m1ap.duty_cycle = 0
            self.m1bn.duty_cycle = 0 
            self.m1bp.duty_cycle = 0
# class MeowSonar:
#     def __init__(self,pin,timeout=30000000):
#         self.timeout  = timeout
#         self.holePin = digitalio.DigitalInOut(usePin(pin))
#         saveObj(pin,self.holePin)

#     def checkdist(self):
#         self.holePin.switch_to_output()
#         self.holePin.value = True
#         sleep(0.00001)
#         self.holePin.value = False
#         self.holePin.switch_to_input()
#         timestamp = monotonic_ns()
#         while self.holePin.value == False:
#             if monotonic_ns() - timestamp > self.timeout:
#                 return 999 
#         timestamp = monotonic_ns()
#         while self.holePin.value == True:
#             if monotonic_ns() - timestamp > self.timeout:
#                 return 999 
#         pulselen = monotonic_ns() - timestamp
#         return round((pulselen / 2) / 29 / 1000)


colorMap={'white':(255,255,255), 'black':(0,0,0), 'red':(255,0,0), 'orange':(255,165,0), 'yellow':(255,255,0),
'green':(0,255,0), 'blue':(0,0,255), 'cyan':(0,127,255), 'purple':(148,0,211), 'pink':(255,105,180) }

def getColHex(t):
    if type(t) == str:
        if len(t) == 7 and t[0] == '#':
            t = (int(t[1:3], 16), int(t[3:5], 16),int(t[5:8], 16))
        else:
            t = colorMap[t]
    if type(t) == int:
        color = (t << 16) + (t << 8) + (t)
    elif type(t) == tuple:
        if len(t) == 3:
            color = ((t[0]&0xff) << 16) + ((t[1]&0xff) << 8) + (t[2]&0xff)
        elif len(t) == 1:
            t = t[0]&0xff
            color = (t << 16) + (t << 8) + (t)
    else:
        color = 0
    return color


import neopixel
class NeoPixel():
    def __init__(self,pn,num=10):
        self.np = neopixel.NeoPixel(usePin(pn),num)
        saveObj(pn,self.np)
        self.np.auto_write = False

    def _trimcolor(self, c):
        c = getColHex(c)
        return ((c>>16)&0xff, (c>>8)&0xff, c&0xff)

    def setColor(self,i,color):
        self.np[i]=self._trimcolor(color)

    def setColorAll(self,*args):
        color = (0,0,0)
        if len(args)==1:
            color = self._trimcolor(args[0])
        if len(args) == 3:
            color = (args[0],args[1],args[2])
        self.np.fill(color)
        self.np.write()

    def setbrightness(self,brightness):
        self.np.brightness = brightness/100

    def update(self):
        self.np.write()   


class Uart:
    def __init__(self,uart,baudrate):
        self.uart = UART(usePin(uartMap[uart][0]),usePin(uartMap[uart][1]),baudrate=baudrate,timeout=0)
        saveObj(uartMap[uart][0],self.uart)
        saveObj(uartMap[uart][1],self.uart)
    
    def readAll(self):
        value = self.uart.read()
        return value
    
    def readLine(self):
        value = self.uart.readline()
        return value
    
    def readLen(self,len):
        value = self.uart.read()
        if value:   
            return value[:len]
        else:
            return None
    
    def writeText(self,value,line):
        if line:
            value+="\n"
        self.uart.write(value.encode())

    def writeByte(self,value):
        self.uart.write(value)

    def existData(self):
        return self.uart.in_waiting


def execfile(name):
    with open(name, 'r') as fp:
        exec(fp.read())

    

try:
    from screen import Screen
    from sensor import Sensor

except:
    pass

if __name__ == '__main__':
    matrix = Matrix()
    matrix.init(x=5,y=5)
    matrix.show([0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,0,0,1,0,0])


