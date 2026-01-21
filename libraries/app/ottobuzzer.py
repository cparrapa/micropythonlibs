# ottobuzzer v2.2 11.12.2024
import machine, time
from machine import Pin, PWM, Timer, UART

IDLE = 0
PAUSED = 1
PLAYING = 2

# define frequency for each tone
B1  = 31
C2  = 33
CS2 = 35
D2  = 37
DS2 = 39
E2  = 41
F2  = 44
FS2 = 46
G2  = 49
GS2 = 52
A2  = 55
AS2 = 58
B2  = 62
C3  = 65
CS3 = 69
D3  = 73
DS3 = 78
E3  = 82
F3  = 87
FS3 = 93
G3  = 98
GS3 = 104
A3  = 110
AS3 = 117
B3  = 123
C4  = 131
CS4 = 139
D4  = 147
DS4 = 156
E4  = 165
F4  = 175
FS4 = 185
G4  = 196
GS4 = 208
A4  = 220
AS4 = 233
B4  = 247
C5  = 262
CS5 = 277
D5  = 294
DS5 = 311
E5  = 330
F5  = 349
FS5 = 370
G5  = 392
GS5 = 415
A5  = 440
AS5 = 466
B5  = 494
C6  = 523
CS6 = 554
D6  = 587
DS6 = 622
E6  = 659
F6  = 698
FS6 = 740
G6  = 784
GS6 = 831
A6  = 880
AS6 = 932
B6  = 988
C7  = 1047
CS7 = 1109
D7  = 1175
DS7 = 1245
E7  = 1319
F7  = 1397
FS7 = 1480
G7  = 1568
GS7 = 1661
A7  = 1760
AS7 = 1865
B7  = 1976
C8  = 2093
CS8 = 2217
D8  = 2349
DS8 = 2489
E8  = 2637
F8  = 2794
FS8 = 2960
G8  = 3136
GS8 = 3322
A8  = 3520
AS8 = 3729
B8  = 3951
C9  = 4186
CS9 = 4435
D9  = 4699
DS9 = 4978
P = 0

class OttoBuzzer:
    buzzer: PWM | None = None
    NOTE_C0 = 16.35
    NOTE_Db0 = 17.32
    NOTE_D0 = 18.35
    NOTE_Eb0 = 19.45
    NOTE_E0 = 20.6
    NOTE_F0 = 21.83
    NOTE_Gb0 = 23.12
    NOTE_G0 = 24.5
    NOTE_Ab0 = 25.96
    NOTE_A0 = 27.5
    NOTE_Bb0 = 29.14
    NOTE_B0 = 30.87
    NOTE_C1 = 32.7
    NOTE_Db1 = 34.65
    NOTE_D1 = 36.71
    NOTE_Eb1 = 38.89
    NOTE_E1 = 41.2
    NOTE_F1 = 43.65
    NOTE_Gb1 = 46.25
    NOTE_G1 = 49
    NOTE_Ab1 = 51.91
    NOTE_A1 = 55
    NOTE_Bb1 = 58.27
    NOTE_B1 = 61.74
    NOTE_C2 = 65.41
    NOTE_Db2 = 69.3
    NOTE_D2 = 73.42
    NOTE_Eb2 = 77.78
    NOTE_E2 = 82.41
    NOTE_F2 = 87.31
    NOTE_Gb2 = 92.5
    NOTE_G2 = 98
    NOTE_Ab2 = 103.83
    NOTE_A2 = 110
    NOTE_Bb2 = 116.54
    NOTE_B2 = 123.47
    NOTE_C3 = 130.81
    NOTE_Db3 = 138.59
    NOTE_D3 = 146.83
    NOTE_Eb3 = 155.56
    NOTE_E3 = 164.81
    NOTE_F3 = 174.61
    NOTE_Gb3 = 185
    NOTE_G3 = 196
    NOTE_Ab3 = 207.65
    NOTE_A3 = 220
    NOTE_Bb3 = 233.08
    NOTE_B3 = 246.94
    NOTE_C4 = 261.63
    NOTE_Db4 = 277.18
    NOTE_D4 = 293.66
    NOTE_Eb4 = 311.13
    NOTE_E4 = 329.63
    NOTE_F4 = 349.23
    NOTE_Gb4 = 369.99
    NOTE_G4 = 392
    NOTE_Ab4 = 415.3
    NOTE_A4 = 440
    NOTE_Bb4 = 466.16
    NOTE_B4 = 493.88
    NOTE_C5 = 523.25
    NOTE_Db5 = 554.37
    NOTE_D5 = 587.33
    NOTE_Eb5 = 622.25
    NOTE_E5 = 659.26
    NOTE_F5 = 698.46
    NOTE_Gb5 = 739.99
    NOTE_G5 = 783.99
    NOTE_Ab5 = 830.61
    NOTE_A5 = 880
    NOTE_Bb5 = 932.33
    NOTE_B5 = 987.77
    NOTE_C6 = 1046.5
    NOTE_Db6 = 1108.73
    NOTE_D6 = 1174.66
    NOTE_Eb6 = 1244.51
    NOTE_E6 = 1318.51
    NOTE_F6 = 1396.91
    NOTE_Gb6 = 1479.98
    NOTE_G6 = 1567.98
    NOTE_Ab6 = 1661.22
    NOTE_A6 = 1760
    NOTE_Bb6 = 1864.66
    NOTE_B6 = 1975.53
    NOTE_C7 = 2093
    NOTE_Db7 = 2217.46
    NOTE_D7 = 2349.32
    NOTE_Eb7 = 2489.02
    NOTE_E7 = 2637.02
    NOTE_F7 = 2793.83
    NOTE_Gb7 = 2959.96
    NOTE_G7 = 3135.96
    NOTE_Ab7 = 3322.44
    NOTE_A7 = 3520
    NOTE_Bb7 = 3729.31
    NOTE_B7 = 3951.07
    NOTE_C8 = 4186.01
    NOTE_Db8 = 4434.92
    NOTE_D8 = 4698.64
    NOTE_Eb8 = 4978.03

    SONGS = [
    'A-Team:d=8,o=5,b=125:4d#6,a#,2d#6,16p,g#,4a#,4d#.,p,16g,16a#,d#6,a#,f6,2d#6,16p,c#.6,16c6,16a#,g#.,2a#',
    'Adams:d=4,o=5,b=160:8c,8d,8e,8f,1p,8d,8e,8f#,8g,1p,8d,8e,8f#,8g,p,8d,8e,8f#,8g,p,8c,8d,8e,8f',
    'Beethoben:d=4,o=5,b=140:8e6,8d#6,8e6,8d#6,8e6,8b,8d6,8c6,a,8p,8c,8e,8a,b,8p,8e,8g#,8b,c6',
    'Bond:d=4,o=5,b=80:32p,16c#6,32d#6,32d#6,16d#6,8d#6,16c#6,16c#6,16c#6,16c#6,32e6,32e6,16e6,8e6,16d#6,16d#6,16d#6,16c#6,32d#6,32d#6,16d#6,8d#6,16c#6,16c#6,16c#6,16c#6,32e6,32e6,16e6,8e6,16d#6,16d6,16c#6,16c#7,c.7,16g#6,16f#6,g#.6',
    'Dryer_Song:d=4,o=5,b=70:8c#.6,16f#6,16f6,16d#6,8c#.6,8a#.,16b,16c#6,16d#6,16g#,16a#,16b,8a#.,8c#.6,8c#.6,16f#6,16f6,16d#6,8c#.6,8f#.6,16f#6,16g#6,16f#6,16f6,16d#6,16f6,8f#.6',
    'Entertainer:d=4,o=5,b=140:8d,8d#,8e,c6,8e,c6,8e,2c.6,8c6,8d6,8d#6,8e6,8c6,8d6,e6,8b,d6,2c6,p,8d,8d#,8e,c6,8e,c6,8e,2c.6,8p,8a,8g,8f#,8a,8c6,e6,8d6,8c6,8a,2d6',
    'Flinstones:d=4,o=5,b=40:32p,16f6,16a#,16a#6,32g6,16f6,16a#.,16f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c6,d6,16f6,16a#.,16a#6,32g6,16f6,16a#.,32f6,32f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c6,a#,16a6,16d.6,16a#6,32a6,32a6,32g6,32f#6,32a6,8g6,16g6,16c.6,32a6,32a6,32g6,32g6,32f6,32e6,32g6,8f6,16f6,16a#.,16a#6,32g6,16f6,16a#.,16f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c.6,32d6,32d#6,32f6,16a#,16c.6,32d6,32d#6,32f6,16a#6,16c7,8a#.6',
    'Gadget:d=16,o=5,b=50:32d#,32f,32f#,32g#,a#,f#,a,f,g#,f#,32d#,32f,32f#,32g#,a#,d#6,4d6,32d#,32f,32f#,32g#,a#,f#,a,f,g#,f#,8d#',
    'Ghostbusters:d=16,o=5,b=112:g,g,8b,8g,8a,4f.,g,g,g ,g,8f,4g.,g,g,8b,8g,8a,4f.,g,g,g,g,8f,8a,8g,4d.,g,g,8b,8g,8a,4f.,g,g,g,g,8f ,4g',
    'GoodBad:d=4,o=5,b=56:32p,32a#,32d#6,32a#,32d#6,8a#.,16f#.,16g#.,d#,32a#,32d#6,32a#,32d#6,8a#.,16f#.,16g#.,c#6,32a#,32d#6,32a#,32d#6,8a#.,16f#.,32f.,32d#.,c#,32a#,32d#6,32a#,32d#6,8a#.,16g#.,d#',
    'Halloween:d=4,o=5,b=180:8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8d6,8g,8g,8d6,8g,8g,8d6,8g,8d#6,8g,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#,8c#6,8f#,8f#,8c#6,8f#,8f#,8c#6,8f#,8d6,8f#',
    'Indiana:d=4,o=5,b=250:e,8p,8f,8g,8p,1c6,8p.,d,8p,8e,1f,p.,g,8p,8a,8b,8p,1f6,p,a,8p,8b,2c6,2d6,2e6,e,8p,8f,8g,8p,1c6,p,d6,8p,8e6,1f.6,g,8p,8g,e.6,8p,d6,8p,8g,e.6,8p,d6,8p,8g,f.6,8p,e6,8p,8d6,2c6',
    'Jeopardy:d=4,o=6,b=125:c,f,c,f5,c,f,2c,c,f,c,f,a.,8g,8f,8e,8d,8c#,c,f,c,f5,c,f,2c,f.,8d,c,a#5,a5,g5,f5,p,d#,g#,d#,g#5,d#,g#,2d#,d#,g#,d#,g#,c.7,8a#,8g#,8g,8f,8e,d#,g#,d#,g#5,d#,g#,2d#,g#.,8f,d#,c#,c,p,a#5,p,g#.5,d#,g#',
    'JingleBell:d=8,o=5,b=112:a,a,4a,a,a,4a,a,c6,f.,16g,2a,a#,a#,a#.,16a#,a#,a,a.,16a,a,g,g,a,4g,4c6,16p,a,a,4a,a,a,4a,a,c6,f.,16g,2a,a#,a#,a#.,16a#,a#,a,a.,16a,c6,c6,a#,g,2f',
    'LeisureSuit:d=16,o=6,b=56:f.5,f#.5,g.5,g#5,32a#5,f5,g#.5,a#.5,32f5,g#5,32a#5,g#5,8c#.,a#5,32c#,a5,a#.5,c#.,32a5,a#5,32c#,d#,8e,c#.,f.,f.,f.,f.,f,32e,d#,8d,a#.5,e,32f,e,32f,c#,d#.,c#',
    'Looney:d=4,o=5,b=140:32p,c6,8f6,8e6,8d6,8c6,a.,8c6,8f6,8e6,8d6,8d#6,e.6,8e6,8e6,8c6,8d6,8c6,8e6,8c6,8d6,8a,8c6,8g,8a#,8a,8f',
    'MahnaMahna:d=16,o=6,b=125:c#,c.,b5,8a#.5,8f.,4g#,a#,g.,4d#,8p,c#,c.,b5,8a#.5,8f.,g#.,8a#.,4g,8p,c#,c.,b5,8a#.5,8f.,4g#,f,g.,8d#.,f,g.,8d#.,f,8g,8d#.,f,8g,d#,8c,a#5,8d#.,8d#.,4d#,8d#.',
    'MASH:d=8,o=5,b=140:4a,4g,f#,g,p,f#,p,g,p,f#,p,2e.,p,f#,e,4f#,e,f#,p,e,p,4d.,p,f#,4e,d,e,p,d,p,e,p,d,p,2c#.,p,d,c#,4d,c#,d,p,e,p,4f#,p,a,p,4b,a,b,p,a,p,b,p,2a.,4p,a,b,a,4b,a,b,p,2a.,a,4f#,a,b,p,d6,p,4e.6,d6,b,p,a,p,2b',
    'MissionImp:d=16,o=6,b=95:32d,32d#,32d,32d#,32d,32d#,32d,32d#,32d,32d,32d#,32e,32f,32f#,32g,g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,f,p,f#,p,g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,f,p,f#,p,a#,g,2d,32p,a#,g,2c#,32p,a#,g,2c,a#5,8c,2p,32p,a#5,g5,2f#,32p,a#5,g5,2f,32p,a#5,g5,2e,d#,8d',
    'Muppets:d=4,o=5,b=250:c6,c6,a,b,8a,b,g,p,c6,c6,a,8b,8a,8p,g.,p,e,e,g,f,8e,f,8c6,8c,8d,e,8e,8e,8p,8e,g,2p,c6,c6,a,b,8a,b,g,p,c6,c6,a,8b,a,g.,p,e,e,g,f,8e,f,8c6,8c,8d,e,8e,d,8d,c',
    'One:d=4,o=5,b=120:2f6,38p,g6,74p,8g#6,137p,g6,74p,8f6,137p,f6,74p,e6,74p,f6,74p,2f6,38p,g6,74p,8g#6,137p,a#6,74p,8f6,137p,f6,74p,e6,74p,f6,74p,2c7,38p,a#6,74p,8g#6,137p,g6,74p,17g#.6,192p,8g.6,101p,g6,77p,17g#.6,175p,8g.6,96p,17g6,240p,g6,74p,8f6,137p,2f6',
    'PinkPanther:d=16,o=5,b=160:8d#,8e,2p,8f#,8g,2p,8d#,8e,p,8f#,8g,p,8c6,8b,p,8d#,8e,p,8b,2a#,2p,a,g,e,d,2e',
    'Picaxe:d=4,o=6,b=101:g5,c,8c,c,e,d,8c,d,8e,8d,c,8c,e,g,2a,a,g,8e,e,c,d,8c,d,8e,8d,c,8a5,a5,g5,2c',
    'Rudolph:d=16,o=6,b=100:32p,g#5,8a#5,g#5,8f5,8c#,8a#5,4g#.5,g#5,a#5,g#5,a#5,8g#5,8c#,2c,f#5,8g#5,f#5,8d#5,8c,8a#5,4g#.5,g#5,a#5,g#5,a#5,8g#5,8a#5,2f5,g#5,8a#5,a#5,8f5,8c#,8a#5,4g#.5,g#5,a#5,g#5,a#5,8g#5,8c#,2c,f#5,8g#5,f#5,8d#5,8c,8a#5,4g#.5,g#5,a#5,g#5,a#5,8g#5,8d#,2c#',
    'SilentNight:d=4,o=5,b=112:g.,8a,g,2e.,g.,8a,g,2e.,2d6,d6,2b.,2c6,c6,2g.,2a,a,c6.,8b,a,g.,8a,g,2e.,2a,a,c6.,8b,a,g.,8a,g,2e.,2d6,d6,f6.,8d6,b,2c6.,2e6.,c6,g,e,g.,8f,d,2c.',
    'Smurfs:d=32,o=5,b=200:4c#6,16p,4f#6,p,16c#6,p,8d#6,p,8b,p,4g#,16p,4c#6,p,16a#,p,8f#,p,8a#,p,4g#,4p,g#,p,a#,p,b,p,c6,p,4c#6,16p,4f#6,p,16c#6,p,8d#6,p,8b,p,4g#,16p,4c#6,p,16a#,p,8b,p,8f,p,4f#',
    'Super Mario - Main Theme:d=4,o=5,b=125:a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16f,16p,8c6,8a.,g,16c,a,8f.,16c,16d,16f,16p,f,16d,16c,16p,16f,16p,16a#,16a,16g,2f,16p,8a.,8f.,8c,8a.,f,16g#,16f,16c,16p,8g#.,2g,8a.,8f.,8c,8a.,f,16g#,16f,8c,2c6',
    'Super Mario - Title Music:d=4,o=5,b=125:8d7,8d7,8d7,8d6,8d7,8d7,8d7,8d6,2d#7,8d7,p,32p,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,16b6,16c7,b6,8a6,8d6,8a6,8a6,8a6,8d6,8a6,8a6,8a6,8d6,8a6,8a6,8a6,16a6,16b6,a6,8g6,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,8d6,8b6,8b6,8b6,16a6,16b6,c7,e7,8d7,8d7,8d7,8d6,8c7,8c7,8c7,8f#6,2g6',
    'SMBtheme:d=4,o=5,b=100:16e6,16e6,32p,8e6,16c6,8e6,8g6,8p,8g,8p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,16p,8c6,16p,8g,16p,8e,16p,8a,8b,16a#,8a,16g.,16e6,16g6,8a6,16f6,8g6,8e6,16c6,16d6,8b,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16c7,16p,16c7,16c7,p,16g6,16f#6,16f6,16d#6,16p,16e6,16p,16g#,16a,16c6,16p,16a,16c6,16d6,8p,16d#6,8p,16d6,8p,16c6',
    'SMBwater:d=8,o=6,b=225:4d5,4e5,4f#5,4g5,4a5,4a#5,b5,b5,b5,p,b5,p,2b5,p,g5,2e.,2d#.,2e.,p,g5,a5,b5,c,d,2e.,2d#,4f,2e.,2p,p,g5,2d.,2c#.,2d.,p,g5,a5,b5,c,c#,2d.,2g5,4f,2e.,2p,p,g5,2g.,2g.,2g.,4g,4a,p,g,2f.,2f.,2f.,4f,4g,p,f,2e.,4a5,4b5,4f,e,e,4e.,b5,2c.',
    'SMBunderground:d=16,o=6,b=100:c,c5,a5,a,a#5,a#,2p,8p,c,c5,a5,a,a#5,a#,2p,8p,f5,f,d5,d,d#5,d#,2p,8p,f5,f,d5,d,d#5,d#,2p,32d#,d,32c#,c,p,d#,p,d,p,g#5,p,g5,p,c#,p,32c,f#,32f,32e,a#,32a,g#,32p,d#,b5,32p,a#5,32p,a5,g#5',
    'StarWars:d=4,o=5,b=45:32p,32f#,32f#,32f#,8b.,8f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32e6,8c#.6,32f#,32f#,32f#,8b.,8f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32c#6,8b.6,16f#.6,32e6,32d#6,32e6,8c#6',
    'TakeOnMe:d=4,o=4,b=160:8f#5,8f#5,8f#5,8d5,8p,8b,8p,8e5,8p,8e5,8p,8e5,8g#5,8g#5,8a5,8b5,8a5,8a5,8a5,8e5,8p,8d5,8p,8f#5,8p,8f#5,8p,8f#5,8e5,8e5,8f#5,8e5,8f#5,8f#5,8f#5,8d5,8p,8b,8p,8e5,8p,8e5,8p,8e5,8g#5,8g#5,8a5,8b5,8a5,8a5,8a5,8e5,8p,8d5,8p,8f#5,8p,8f#5,8p,8f#5,8e5,8e5',
    'tetris:d=4,o=5,b=160:e6,8b,8c6,8d6,16e6,16d6,8c6,8b,a,8a,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,2a,8p,d6,8f6,a6,8g6,8f6,e6,8e6,8c6,e6,8d6,8c6,b,8b,8c6,d6,e6,c6,a,a',
    'The_Simpsons:d=4,o=5,b=160:c.6,e6,f#6,8a6,g.6,e6,c6,8a,8f#,8f#,8f#,2g,8p,8p,8f#,8f#,8f#,8g,a#.,8c6,8c6,8c6,c6',
    'Toccata:d=4,o=5,b=160:16a4,16g4,1a4,16g4,16f4,16d4,16e4,2c#4,16p,d.4,2p,16a4,16g4,1a4,8e.4,8f.4,8c#.4,2d4',
    'TopGun:d=4,o=4,b=31:32p,16c#,16g#,16g#,32f#,32f,32f#,32f,16d#,16d#,32c#,32d#,16f,32d#,32f,16f#,32f,32c#,16f,d#,16c#,16g#,16g#,32f#,32f,32f#,32f,16d#,16d#,32c#,32d#,16f,32d#,32f,16f#,32f,32c#,g#',
    'WeWishYou:d=4,o=5,b=200:d,g,8g,8a,8g,8f#,e,e,e,a,8a,8b,8a,8g,f#,d,d,b,8b,8c6,8b,8a,g,e,d,e,a,f#,2g,d,g,8g,8a,8g,8f#,e,e,e,a,8a,8b,8a,8g,f#,d,d,b,8b,8c6,8b,8a,g,e,d,e,a,f#,1g,d,g,g,g,2f#,f#,g,f#,e,2d,a,b,8a,8a,8g,8g,d6,d,d,e,a,f#,2g',
    'Wii_Fit_Ob:d=4,o=5,b=149:1p,g,512p,g6,512p,7f6,15e.6,256p,7d6,15c.6,256p,7d6,e6,512p,g.,256p,7a,15c.6,p,g.6,15g.6,256p,7a6,15g.6,256p,28a6,512p,10a#6,128p,a6,512p,g.6,p,a6,512p,c6,512p,7c6,15c.6,256p,7d6,d#6,512p,g#6,512p,d#6,512p,d6,512p,15c.6,256p,e6,512p,g6,512p,g6,512p,7a6,15g.6,256p,7a#6,a6,512p,15g.6,2p,7a6,15c.7,256p,7d7,15c.7,256p,7d#7,d7,512p,15c.7,256p,d7,512p,7f#6,g6,512p,15g.6,256p,7a6,15c.7',
    'Xfiles:d=4,o=5,b=125:e,b,a,b,d6,2b.,1p,e,b,a,b,e6,2b.,1p,g6,f#6,e6,d6,e6,2b.,1p,g6,f#6,e6,d6,f#6,2b.,1p,e,b,a,b,d6,2b.,1p,e,b,a,b,e6,2b.,1p,e6,2b.',
    '20thCenFox:d=16,o=5,b=140:b,8p,b,b,2b,p,c6,32p,b,32p,c6,32p,b,32p,c6,32p,b,8p,b,b,b,32p,b,32p,b,32p,b,32p,b,32p,b,32p,b,32p,g#,32p,a,32p,b,8p,b,b,2b,4p,8e,8g#,8b,1c#6,8f#,8a,8c#6,1e6,8a,8c#6,8e6,1e6,8b,8g#,8a,2b',
]

    def __init__(self, pin):
        self._pin = Pin(pin)

    def __get_buzzer(self) -> PWM:
        if not self.buzzer:
            self.buzzer = PWM(self._pin)
            return self.buzzer
        return self.buzzer

    def playNote(self, freq, interval):
        if freq > 0:
            buzzer = PWM(self._pin)
            buzzer.freq(freq)
            buzzer.duty(512)
            time.sleep(interval / 1000)
            buzzer.duty(0)

    def tone_on(self, freq):
        buzz = self.__get_buzzer()
        buzz.freq(int(freq))
        buzz.duty(512)

    def tone_off(self):
        buzz = self.__get_buzzer()
        buzz.duty(0)

    def tone(self, freq, noteDuration, silentDuration):
        if freq > 0:
            buzzer = PWM(self._pin)
            buzzer.freq(int(freq))
            buzzer.duty(512)
            time.sleep(noteDuration / 1000)
            time.sleep(silentDuration / 1000)
            buzzer.duty(0)


    def play_emoji(self, emoji):
        if emoji == "connect":
            self.tone(self.NOTE_E5,50,30)
            self.tone(self.NOTE_E6,55,25)
            self.tone(self.NOTE_A6,60,10)
            return

        if emoji == "disconnect":
            self.tone(self.NOTE_E5,50,30)
            self.tone(self.NOTE_A6,55,25)
            self.tone(self.NOTE_E6,50,60)
            return

        if emoji == "button":
            self.bendTones(self.NOTE_E6, self.NOTE_G6, 1.03, 20, 2)
            time.sleep(30 / 1000)
            self.bendTones (self.NOTE_E6, self.NOTE_D7, 1.04, 10, 2)
            return

        if emoji == "mode1":
            self.bendTones(self.NOTE_E6, self.NOTE_A6, 1.02, 30, 10)
            return

        if emoji == "mode2":
            self.bendTones(self.NOTE_G6, self.NOTE_D7, 1.03, 30, 10)
            return

        if emoji == "mode3":
            self.tone(self.NOTE_E6,50,100)
            self.tone(self.NOTE_G6,50,80)
            self.tone(self.NOTE_D7,300,0)
            return

        if emoji == "surprise":
            self.bendTones(800, 2150, 1.02, 10, 1)
            self.bendTones(2149, 800, 1.03, 7, 1)
            return

        if emoji == "jump":
            self.bendTones(880, 2000, 1.04, 8, 3)
            time.sleep(200 / 1000)
            return

        if emoji == "oh":
            self.bendTones(880, 2000, 1.04, 8, 3)
            time.sleep(200 / 1000)
            i = 880
            while i < 2000:
                self.tone(self.NOTE_B5,5,10)
                i = i * 1.04
            return

        if emoji == "oh2":
            self.bendTones(1880, 3000, 1.03, 8, 3)
            time.sleep(200 / 1000)
            i = 1880
            while i < 3000:
                self.tone(self.NOTE_C6,10,10)
                i = i * 1.03
            return

        if emoji == "cuddle":
            self.bendTones(700, 900, 1.03, 16, 4)
            self.bendTones(899, 650, 1.01, 18, 7)
            return

        if emoji == "sleep":
            self.bendTones(100, 500, 1.04, 10, 10)
            time.sleep(500 / 1000)
            self.bendTones(400, 100, 1.04, 10, 1)
            return

        if emoji == "happy":
            self.bendTones(1500, 2500, 1.05, 20, 8)
            self.bendTones(2499, 1500, 1.05, 25, 8)
            return

        if emoji == "superhappy":
            self.bendTones(2000, 6000, 1.05, 8, 3)
            time.sleep(50 / 1000)
            self.bendTones(5999, 2000, 1.05, 13, 2)
            return

        if emoji == "happyshort":
            self.bendTones(1500, 2000, 1.05, 15, 8)
            time.sleep(100 / 1000)
            self.bendTones(1900, 2500, 1.05, 10, 8)
            return

        if emoji == "sad":
            self.bendTones(880, 669, 1.02, 20, 200)
            return

        if emoji == "confused":
            self.bendTones(1000, 1700, 1.03, 8, 2)
            self.bendTones(1699, 500, 1.04, 8, 3)
            self.bendTones(1000, 1700, 1.05, 9, 10)
            return

        if emoji == "fart1":
            self.bendTones(1600, 3000, 1.02, 2, 15)
            return

        if emoji == "fart2":
            self.bendTones(2000, 6000, 1.02, 2, 20)
            return

        if emoji == "fart3":
            self.bendTones(1600, 4000, 1.02, 2, 20)
            self.bendTones(4000, 3000, 1.02, 2, 20)
            return

    def bendTones (self, initFrequency, finalFrequency, prop, noteDuration, silentDuration):
        if(silentDuration == 0):
            silentDuration = 1

        if initFrequency < finalFrequency:
            i = initFrequency
            while i < finalFrequency:
                self.tone(int(i), noteDuration, silentDuration)
                i *= prop
        else:
            i = initFrequency
            while i > finalFrequency:
                self.tone(int(i), noteDuration, silentDuration)
                i /= prop

    def RTTTL_notes(self,text):
        try:
            title, defaults, song = text.split(':')
            d, o, b = defaults.split(',')
            d = int(d.split('=')[1])
            o = int(o.split('=')[1])
            b = int(b.split('=')[1])
            whole = (60000/b)*4
            noteList = song.split(',')
        except:
            return 'Please enter a valid RTTTL string.'
        notes = 'abcdefgp'
        outList = []
        for note in noteList:
            index = 0
            for i in note:
                if i in notes:
                    index = note.find(i)
                    break
            length = note[0:index]
            value = note[index:].replace('#','s').replace('.','')
            if not any(char.isdigit() for char in value):
                value += str(o)
            if 'p' in value:
                value = 'p'
            if length == '':
                length = d
            else:
                length = int(length)
            length = whole/length
            if '.' in note:
                length += length/2
            print(eval(value.upper()));
            outList.append((eval(value.upper()), length))
        return outList

    def find(self,name):
        for song in self.SONGS:
            song_name = song.split(':')[0]
            if song_name == name:
                return song

    def execute_RTTTL(self,name):
        song=self.find(name)
        tune = self.RTTTL_notes(song)
        for freqc, msec in tune:
            self.playNote(freqc, msec)

    def execute_RTTTL_song(self,songRTTTL):
        tune = self.RTTTL_notes(songRTTTL)
        for freqc, msec in tune:
            self.playNote(freqc, msec)

class Player:
    def __init__(self, pin_TX, pin_RX):
        self.uart = UART(1, 9600, tx=pin_TX, rx=pin_RX)
        self.cmd(0x3F)  # send initialization parametres
        self._fadeout_timer = Timer(-1)

        self._volume = 15
        self._max_volume = 50
        self._fadeout_speed = 0

    def cmd(self, command, parameter=0x00, parameter2=0x00):
        query = bytes([0x7e, 0xFF, 0x06, command,
                       0x00, parameter2, parameter, 0xEF])
        #print(query)
        self.uart.write(query)
        time.sleep(0.05)

    # with checksum, but it doesnÂ´t work
    def cmd2(self,cmd,param1=0,param2=0):
        out_bytes = bytearray(10)
        out_bytes[0]=126
        out_bytes[1]=255
        out_bytes[2]=6
        out_bytes[3]=cmd
        out_bytes[4]=0
        out_bytes[5]=param1
        out_bytes[6]=param2
        out_bytes[9]=239
        checksum = 0
        for i in range(1,7):
            checksum=checksum+out_bytes[i]
        out_bytes[7]=(checksum>>7)-1
        out_bytes[7]=~out_bytes[7]
        out_bytes[8]=checksum-1
        out_bytes[8]=~out_bytes[8]
        print(out_bytes)
        self.uart.write(out_bytes)

    def _fade_out_process(self, timer):
        new_volume = self._volume - self._fadeout_speed

        if new_volume <= 0:
            print("fadeout finished")
            new_volume = 0
            self._fadeout_timer.deinit()
            self.stop()
            new_volume = self._max_volume # reset volume to max
        self.volume(new_volume)

    # playback

    def play(self, track_id=False):
        if not track_id:
            self.resume()
        elif track_id == 'next':
            self.cmd(0x01)
        elif track_id == 'prev':
            self.cmd(0x02)
        elif isinstance(track_id, int):
            self.cmd(0x03, track_id)

    def pause(self):
        self.cmd(0x0E)

    def resume(self):
        self.cmd(0x0D)

    def stop(self):
        self.cmd(0x16)

    def loop_track(self, track_id):
        self.cmd(0x08, track_id)

    def loop(self):
        self.cmd(0x19)

    def loop_disable(self):
        self.cmd(0x19, 0x01)

    def PlayFolder(self, folder_id, song_id):
        self.cmd(0x0F,song_id,folder_id)

    # volume control

    def volume_up(self):
        self._volume += 1
        self.cmd(0x04)

    def volume_down(self):
        self._volume -= 1
        self.cmd(0x05)

    def volume(self, volume=False):
        if volume:
            self._volume = int(sorted([0, volume, self._max_volume])[1])
            #print("volume", self._volume)
            self.cmd(0x06, self._volume)

        return self._volume

    # hardware

    def module_sleep(self):
        self.cmd(0x0A)

    def module_wake(self):
        self.cmd(0x0B)

    def module_reset(self):
        self.cmd(0x0C)
