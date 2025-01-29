import time                       #importing time libraries
from ottobuzzer import Player

dfplayer = Player(16, 17)         # Connector 2
#dfplayer.module_reset()
#dfplayer.PlayFolder(1,1)
dfplayer.volume(50)
dfplayer.stop()

dfplayer.play()
time.sleep(2)
dfplayer.pause()

for count in range(21):

    dfplayer.play('next')
    dfplayer.volume_up()
    #dfplayer.volume_down()
    time.sleep(2)
