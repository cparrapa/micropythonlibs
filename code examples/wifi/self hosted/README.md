These 3 files provide a proof of concept self hosted web control  

ottoSelfHostedWebControl.py is the main program  
ottoWebInterface.py creates the web page  
edit secrets.py to contain your wif details  

we also need micripyserver.py from https://github.com/troublegum/micropyserver   I've added a copy here for convenience
  
I lifted the code from my Otto Mini and so there are buttons that do nothing (Moves and Gestrues)  
  
Control and Songs should work  
  
For the ip address display code uncomment out  102 to 132 in ottoSelfHostedWebControl.py     
ip address is also given in serial monitor  

open this ip in a browser on a device on the same network and off you go (hopefully)
