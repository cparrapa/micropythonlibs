[![Morpx-bbs](http://bbs.morpx.com/template/mu/images/logo.png)](http://bbs.morpx.com/forum.php)
[![Git-rep](https://img.shields.io/github/repo-size/mu-opensource/MuVisionSensor3-MicroPython.svg)](https://github.com/mu-opensource/MuVisionSensor3-MicroPython)
[![Git-release](https://img.shields.io/github/downloads/mu-opensource/MuVisionSensor3-MicroPython/total.svg)](https://github.com/mu-opensource/MuVisionSensor3-MicroPython/releases)

MicroPython for the BBC micro:bit with MU vision sensor
=======================================================
- 在官方runtime固件基础上增加了MuVisionSensor模块，适用于小Mu视觉传感器
- 暂不支持Serial模式

Morpx官方文档：[https://morpx-docs.readthedocs.io/en/latest/MUVS3/MUVS3_MicroPython/index.html](https://morpx-docs.readthedocs.io/en/latest/MUVS3/MUVS3_MicroPython/index.html)

编译方法及通用模块参考micro:bit官方文档 [https://github.com/bbcmicrobit/micropython](https://github.com/bbcmicrobit/micropython)

How to use
==========

将microbit-micropython.hex上传到microbit，随后用终端工具（putty/picocom等等）打开对应的端口

Upon reset you will have a REPL on the USB CDC serial port, with baudrate
115200 (eg picocom /dev/ttyACM0 -b 115200).

Then try:
```py
#导入MuVisionSensor模块
>>> from MuVisionSensor import *
#初始化MuVisionSensor对象，默认I2C地址0x60
>>> mu=MuVisionSensor(0x60)
#启动模块
>>> mu.begin()
#启动视觉算法
>>> mu.VisionBegin(VISION_SHAPE_CARD_DETECT)
#获取结果
>>> ret = mu.GetValue(VISION_SHAPE_CARD_DETECT,Status)
```

在Mu Editor中使用该固件的方法
==========================
- 添加microbit-micropython.hex的路径,替换默认固件

![image](https://raw.githubusercontent.com/zjuxumang/micropython/master/docs/MuEditor.png)

- 形状卡片检测测试程序：`/tests/test_shape_card_detect.py`
