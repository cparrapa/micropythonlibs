#!/usr/bin/python
#coding:utf-8

import board
from busio import UART
import time
from future import uartMap
from board_map import usePin,saveObj

__version__ = "1.0.2"
class KOI:
    def __init__(self,uart):
        self.space = ['0']*8
        self.re_temp = []
        self.cmd = None
        self.uart = UART(usePin(uartMap[uart][0]),usePin(uartMap[uart][1]),baudrate=115200,timeout = 0)
        saveObj(uartMap[uart][0],self.uart)
        saveObj(uartMap[uart][1],self.uart)
        
        self.uart.write(bytes('\n\n','utf-8'))
        self.uart.write(bytes('K0\r\n','utf-8'))
        time.sleep(0.4)
        flag = ''
        while not('K0' in flag):
            data = self.uart.readline()
            if data:
                try:
                    flag = str(data,'UTF-8')
                    if 'K0' in flag:
                        pass
                        #screen.clear()
                        break
                    else:
                        pass
                        #screen.showmsg(translate("KOI Init Fail,Please Reset"), translate('Warning'))
                except:
                    pass
                    #screen.showmsg(translate("KOI Init Fail,Please Reset"), translate('Warning'))
                    flag = ''
            else:
                self.uart.write(bytes('K0\r\n','utf-8'))
                time.sleep(1)

    """
    接收来自KOI对应的K指令，并取出有用的数据
    """
    def _uart_re(self,cmd):
        data = self.uart.read()
        if data:
            re = str(data,'utf-8')
            re = re.splitlines()
            for i in re:
                i = i.strip()
                i = i.split(' ')
                if i.pop(0) == cmd:
                    self.re_temp = i
                    return i
            return False
        return False


    def get_re(self,cmd):
        if cmd == self.cmd and self.re_temp:
            return self.re_temp
        else:
            return self.space
        

    """
    KOI资源基础
    """
    # KOI摄像头旋转 / eg: 0:前置 2:后置
    def screen_mode(self,mode,cmd="K6"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,mode),'utf-8'))
    
    # KOI显示字符串
    def text(self,x,y,delay,text,cmd="K4"):
        self.uart.write(bytes("%s %s %s %s %s\r\n" %(cmd,str(x),str(y),str(delay),str(text)),'utf-8'))
    
    # KOI拍照截屏 / eg: pic='test.jpg'
    def screen_save(self,pic,cmd="K2"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,pic),'utf-8'))
    
    # KOI显示图片
    def screen_show(self,pic,cmd="K1"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,pic),'utf-8'))

    # KOI按键
    def btnValue(self,cmd="K3"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))
        self.cmd = cmd
        time.sleep(0.2)
        return self._uart_re(cmd)


    """
    yolo模型人脸追踪
    """
    # 人脸模型
    def face_yolo_load(self,cmd="K30"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))
        time.sleep(0.3)

    # 追踪人脸
    def face_detect(self,cmd="K31"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))
        time.sleep(0.3)
        self.cmd = cmd
        return self._uart_re(cmd)
        
    # 人脸数量
    def face_count(self,cmd="K32"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))
        time.sleep(0.3)
        self.cmd = cmd
        return self._uart_re(cmd)

    """
    连接WiFi
    """
    #连接WiFi / eg: router='hogan' pwd='12345678'
    def connect_wifi(self,router,pwd,cmd="K50"):
        self.uart.write(bytes("%s %s %s\r\n" %(cmd,router,pwd),'utf-8'))
    
    #获取IP并显示
    def get_ip(self,cmd="K54"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))
        self.cmd = cmd
        return self._uart_re(cmd)


    """
    baiduAI
    """
    # baiduAI人脸识别
    def baiduAI_face_detect(self,cmd="K75"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))
        time.sleep(2)
        self.cmd = cmd
        return self._uart_re(cmd)
        
    # 将最后一次识别到的人脸添加到baiduAI人脸组
    def baiduAI_face_add(self,face_token,groupName,faceName,cmd="K76"):
        self.uart.write(bytes("%s %s %s %s\r\n" %(cmd, face_token, groupName, faceName),'utf-8'))

    # 在baiduAI人脸组中搜索人脸 
    def baiduAI_face_search(self,face_token,groupName,cmd="K77"):
        self.uart.write(bytes("%s %s %s\r\n" %(cmd, face_token, groupName),'utf-8'))
        time.sleep(2)
        self.cmd = cmd
        return self._uart_re(cmd)
  
    # koi百度文字转语音
    def baiduAI_tts(self,txt,cmd="K78"):
        self.uart.write(bytes("%s %s\r\n" %(cmd, txt),'utf-8'))


    """
    KNN特征分类
    """
    # 初始化特征分类器
    def init_cls(self):
        self.uart.write(bytes("K40\r\n",'utf-8'))

    # 分类器增加标签
    def cls_add_tag(self,id,cmd="K41"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,id),'utf-8'))

    # 运行分类器
    def cls_run(self,cmd="K42"):
        self.uart.write(bytes(cmd + "\r\n",'utf-8'))
        time.sleep(1)
        self.cmd = cmd
        self._uart_re(cmd)
        return self.get_re(cmd)[0]

    # 分类器保存模型文件 / eg:'cls.json'
    def cls_save_model(self,model,cmd="K43"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,model),'utf-8'))

    # 分类器加载模型文件 / eg:'cls.json'
    def cls_load_model(self,model,cmd="K44"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,model),'utf-8'))


    """
    音频
    """
    # 录制音频 / eg: name='sound.wav'
    def audio_record(self,wav,cmd="K61"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,wav),'utf-8'))
    
    # 播放音频 / eg: name='sound.wav'
    def audio_play(self,wav,cmd="K62"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,wav),'utf-8'))
    
    # 设置环境噪声基准
    def audio_noisetap(self):
        self.uart.write(bytes("K63\r\n",'utf-8'))
    
    # 添加语音关键词标签 
    def speech_add_tag(self,id,cmd="K64"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,id),'utf-8'))
    
    # 识别语音关键词
    def speech_run(self,cmd="K65"):
        self.uart.write(bytes(cmd + "\r\n",'utf-8'))
        time.sleep(3)
        self.cmd = cmd
        self._uart_re(cmd)
        return self.get_re(cmd)[0]

    # 保存语音关键词模型文件 / eg:'cmd.json'
    def speech_save_model(self,model,cmd="K66"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,model),'utf-8'))

    # 加载语音关键词模型文件 / eg:'cmd.json'
    def speech_load_model(self,model,cmd="K67"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,model),'utf-8'))



    """
    扫码
    """
    def scan_qrcode(self,cmd="K20"):
        self.uart.write(bytes(cmd + "\r\n",'utf-8'))
        time.sleep(1)
        self.cmd = cmd
        self._uart_re(cmd)
        return self.get_re(cmd)[0]

    def scan_barcode(self,cmd="K22"):
        self.uart.write(bytes(cmd + "\r\n",'utf-8'))
        time.sleep(1)
        self.cmd = cmd
        self._uart_re(cmd)
        return self.get_re(cmd)[0]

    def scan_Apriltag(self,cmd="K23"):
        self.uart.write(bytes(cmd + "\r\n",'utf-8'))
        time.sleep(1)
        self.cmd = cmd
        return self._uart_re(cmd)

    """
    颜色识别
    """
    # 校准颜色 / eg: name='blue'
    def color_cali(self,name,cmd="K16"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,name),'utf-8'))
    
    # KOI色块追踪 / eg: name='blue'
    def color_tracking(self,name,cmd="K15"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,name),'utf-8'))
        time.sleep(0.1)
        self.cmd = cmd
        return self._uart_re(cmd)

    #线条识别（name为线条颜色）
    def line_tracking(self,name,cmd="K12"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,name),'utf-8'))
        time.sleep(0.1)
        self.cmd = cmd
        return self._uart_re(cmd)

    # 圆形识别（th为阈值）
    def circle_detect(self,th=2000,cmd="K10"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,th),'utf-8'))
        time.sleep(0.1)
        self.cmd = cmd
        return self._uart_re(cmd)
        
    # 矩形识别（th为阈值）
    def rectangle_detect(self,th=6000,cmd="K11"):
        self.uart.write(bytes("%s %s\r\n" %(cmd,th),'utf-8'))
        time.sleep(0.1)
        self.cmd = cmd
        return self._uart_re(cmd)


    """
    更多
    """
    # 停止人脸追踪yolo模型和特征分类模型
    def stop_kpu(self,cmd="K98"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))
    
    # 重启KOI   
    def reset(self,cmd="K99"):
        self.uart.write(bytes("%s\r\n" %(cmd),'utf-8'))