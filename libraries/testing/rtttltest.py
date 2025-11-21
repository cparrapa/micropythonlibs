import rtttl
from ottomotor import OttoMotor
from ottobuzzer import OttoBuzzer

motor = OttoMotor(13, 14)             # Connectors 10 & 11
buzzer = OttoBuzzer(25)               # Built in Buzzer

abba = 'AbbaMammaMia:d=4,o=5,b=40:32f6,32d#6,32f6,32d#6,8p,32d#6,32d#6,32f6,32g6,32f6,32d#6,16p,16f6,32d#6,16p,16g#6,32g#6,32g#6,32g#6,16g6,16d#6,16p,32f6,32d#6,32f6,32d#6,8p,32d#6,32d#6,32f6,32g6,32f6,32d#6,16p,16f6,32d#6,16p,16g#6,32g#6,32g#6,32g#6,16g6,16d#6,16p,16a#.6,32a#6,32a#6,16a#6,16f6,16g6,16g#6,16p,32p,16g.6,32g6,32g6,16g6,16d6,16d#6,16f6,16p,32p,16f6,16d#6,32p,16g#6,32g#6,32g#6,32g#6,32g6,32d#6,32f6,32d#6'
song ='JingleBell:d=8,o=5,b=112:a,a,4a,a,a,4a,a,c6,f.,16g,2a,a#,a#,a#.,16a#,a#,a,a.,16a,a,g,g,a,4g,4c6,16p,a,a,4a,a,a,4a,a,c6,f.,16g,2a,a#,a#,a#.,16a#,a#,a,a.,16a,c6,c6,a#,g,2f'
   
buzzer.execute_RTTTL('JingleBell')
rtttl.play(song)