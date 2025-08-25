# OttoMini

Web Control for Otto Mini

DISCLAIMER: Clunky and liable to falling over (both the code and Otto himself!!). This is a proof of concept/work in progress.  

If anyone improves on this please let me know!!  

![MiniOttoDimensions](https://github.com/user-attachments/assets/eedbeead-a1c8-400b-bb97-cb20c0b94d31)

Otto Mini is a smaller Otto robot running on an ESP32-C3 supermini  

Printing instructions are here https://www.printables.com/model/1066390-otto-mini

micropyserver.py cones from https://github.com/troublegum/micropyserver/tree/master    

Most of the Otto code (unless stated otherwise) is from https://github.com/OttoDIY/OttoDIYPython  

Otto_servo.py has been edited to suit the DSPower DS-M005 2g servo

MiniOtto.py has been derived from Otto.py in the OttoDIY Python Project  

main.py runs the webserver on the ESP32-C3
edit line 168 (at time of writing) otto.setTrims(0,0,0,0) to suit your bot

MO_WebInterface.py contains much of the code for drawing the web page

secrets.py is for your wifi details

