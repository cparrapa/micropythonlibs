#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matatalab
import math, time, random
import machine, neopixel, _thread

version = 0.6

NUM_LEDS = 15

_leds = neopixel.NeoPixel(machine.Pin(7), NUM_LEDS)

THREAD_SIZE = 4 * 1024

thread_flag = 0
effect_type = 0
effect_time = 0
led_count = 0
thread_stop = 0

led_color = {
1:[0,0,255],
2:[0,255,0],
3:[255,0,0],
4:[255,255,0],
5:[255,0,255],
6:[0,255,255],
7:[202,235,216],
8:[255,127,80],
9:[0,191,255],
10:[0,255,127],
}

led_index = 1

def get_version():
    return version

def show_all(r, g, b):
    v = (r, g, b)
    _leds.fill(v)
    _leds.write()

def show_side(mode, r, g, b):
    if mode == 0:
        _leds[0] = (r,g,b)
        _leds[1] = (r,g,b)
        _leds[2] = (r,g,b)
    elif mode == 1:
        _leds[3] = (r,g,b)
        _leds[4] = (r,g,b)
        _leds[5] = (r,g,b)
    _leds.write()

def display(data):
    if(type(data) == str):
        print("not support now!")
        return
    data_len = len(data)
    for i in range(data_len / 3):
        _leds[i] = (data[3 * i], data[3 * i + 1], data[3 * i + 2])
    _leds.write()

def show_single(id, r, g, b):
    if(id < 0) or (id > 6):
        pass
    if(id == 0):
        show_all(r,g,b)
    else:
        _leds[id - 1] = (r,g,b)
        _leds.write()

def led_twinkle():
    global led_count
    led_count = 5
    for i in range(3):
        leds.show_all(255, 0, 0)
        time.sleep(0.16)
        leds.show_all(0, 0, 0)
        time.sleep(0.16)
    led_count = 0

def random_shuffle(seq):
    l = len(seq)
    for i in range(l):
        j = random.randrange(l)
        seq[i], seq[j] = seq[j], seq[i]
    return seq

def cyclic_color(np):
    color = [0, 0, 0]

    for i in range(NUM_LEDS):
        if i == 0:
            color[0] = random.randint(0, 50)  # 随机颜色
            color[1] = random.randint(0, 50)
            color[2] = random.randint(0, 50)
            np[i] = tuple(color)
        else:
            np[i] = prev
        prev = tuple(np[i])
        np.write()
        time.sleep_ms(50)  # 每个像素之间间隔50毫秒

# 定义颜色渐变函数
def fade_color(color, val):
    return tuple(int(x * val / 255) for x in color)

def breathe_animation(np, start_time, effect_time):
    global thread_stop, effect_type
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # 定义颜色列表，可以根据需要修改
    
    for i in range(256):  # 呼吸效果的循环
        brightness = int(abs(math.sin(i / 256 * math.pi)) * 255)  # 计算亮度
        
        for j in range(NUM_LEDS):  # 逐个LED设置颜色
            color = random.choice(colors)  # 随机选择颜色
            np[j] = tuple(map(lambda x: x * brightness // 255, color))  # 设置颜色和亮度
        
        np.write()  # 更新LED的显示
        time.sleep(0.05)  # 等待一段时间
        current_time = time.ticks_ms()
        if effect_time != "None":
            if current_time - start_time > effect_time * 1000:
                break
        if effect_type != 3 or thread_stop == 1:
            break

# 定义颜色渐变函数
def fade_color(color, val):
    return tuple(int(x * val / 255) for x in color)

# 定义循环呼吸效果函数
def cyclic_breathe(np, start_time, effect_time):
    global thread_stop
    # 随机颜色（R, G, B）值
    r, g, b = tuple(random.randint(0, 255) for _ in range(3))
    for val in range(0, 256, 2):
        # 渐变亮度
        val_normalized = int((val / 255) * 80)
        for i in range(NUM_LEDS):
            np[i] = fade_color((r, g, b), val_normalized)
        np.write()
        time.sleep_ms(10)
        current_time = time.ticks_ms()
        if effect_time != "None":
            if current_time - start_time > effect_time * 1000:
                break
        if effect_type != 1 or thread_stop == 1:
            break
    for val in range(0, 256, 2):
        # 渐变亮度
        val_normalized = int(((255 - val) / 255) * 80)
        for i in range(NUM_LEDS):
            np[i] = fade_color((r, g, b), val_normalized)
        np.write()
        time.sleep_ms(10)
        current_time = time.ticks_ms()
        if effect_time != "None":
            if current_time - start_time > effect_time * 1000:
                break
        if effect_type != 1 or thread_stop == 1:
            break

def waterfall_light(start_time, effect_time):
    global led_index
    led_color = 0

    while True:
        show_single((led_index + 2), 0, 0, 50)
        show_single((led_index + 1), 0, 50, 0)
        show_single(led_index, 50, 0, 0)
        if (led_index > 1):
            led_color = ((led_index - 1))
            while not ((led_color == 0)):
                if (led_color == 1):
                    show_single(led_color, 0, 0, 50)
                if (led_color == 2):
                    show_single(led_color, 0, 0, 50)
                    led_color = ((led_color - 1))
                    show_single(led_color, 0, 50, 0)
                if (led_color > 2):
                    show_single(led_color, 0, 0, 50)
                    led_color = ((led_color - 1))
                    show_single(led_color, 0, 50, 0)
                    led_color = ((led_color - 1))
                    show_single(led_color, 50, 0, 0)
                led_color = ((led_color - 1))
        time.sleep(0.2)
        led_index += 1
        if(led_index > NUM_LEDS - 2):
            led_index = 1
            show_all(0,0,0)

        current_time = time.ticks_ms()
        if effect_time != "None":
            if current_time - start_time > effect_time * 1000:
                led_index = 1
                break
        if effect_type != 4 or thread_stop == 1:
            led_index = 1
            break

def led_task():
    global effect_type, led_color, thread_flag, thread_stop, thread_stop_flag
    thread_flag = 1
    r_led = 0
    g_led = 120
    b_led = 255
    r_led_tepm = 5
    g_led_tepm = 5
    b_led_tepm = -5
    led_sleep_time = 0
    mode_3_stop_falg = 0
    led_mode2_index = [1,2,3]
    random_list = [1,2,3,4,5,6,7,8,9,10]
    led_mode3_index = 0
    start_time = time.ticks_ms()

    while(True):
        time.sleep(0.02)
        if(effect_type == 1):
            cyclic_breathe(_leds, start_time, effect_time)
        elif(effect_type == 4):
            #跑马灯
            # time.sleep(0.2)
            # show_all(0, 0, 0)
            # led_mode2_index[0] = led_mode2_index[0] + 1
            # led_mode2_index[1] = led_mode2_index[1] + 1
            # led_mode2_index[2] = led_mode2_index[2] + 1
            # if(led_mode2_index[0] > 10):
            #     led_mode2_index[0] = led_mode2_index[0] - 10
            # if(led_mode2_index[1] > 10):
            #     led_mode2_index[1] = led_mode2_index[1] - 10
            # if(led_mode2_index[2] > 10):
            #     led_mode2_index[2] = led_mode2_index[2] - 10
            # show_single(led_mode2_index[0],255,0,0)
            # show_single(led_mode2_index[1],0,255,0)
            # show_single(led_mode2_index[2],0,0,255)
            waterfall_light(start_time, effect_time)
            
        elif(effect_type == 0):
            #随机逐个点亮
            if(mode_3_stop_falg == 1):
                mode_3_stop_falg = 0            
                show_all(0, 0, 0)
            time.sleep(0.2)
            led_sleep_time = led_sleep_time + 1
            if(led_mode3_index >= 10):
                random_list = random_shuffle(random_list)
                show_all(0, 0, 0)
                led_mode3_index = 0
            if(led_sleep_time >= 5):
                led_mode3_index = led_mode3_index + 1
                led_sleep_time = 0
            led_color_index = random.randint(1,10)
            led_rgb_color = led_color.get(led_color_index,[])
            show_single(random_list[led_mode3_index - 1], led_rgb_color[0],led_rgb_color[1],led_rgb_color[2])
        elif(effect_type == 3):
            breathe_animation(_leds, start_time, effect_time)
        elif(effect_type == 2):
            # time.sleep(0.02)
            cyclic_color(_leds)
            
        
        current_time = time.ticks_ms()
        if effect_time != "None":
            if current_time - start_time > effect_time * 1000:
                thread_stop_flag = 1
                show_all(0, 0, 0)
                break
        if thread_stop == 1:
            show_all(0, 0, 0)
            thread_stop = 0
            break
    thread_flag = 0

def effect(type, time_arg = "None"):
    global effect_type, effect_time, thread_flag, thread_stop, thread_stop_flag, thread_stop
    thread_stop = 1
    time.sleep(0.2)
    effect_type = type
    effect_time = time_arg
    if thread_flag == 0:
        _thread.stack_size(THREAD_SIZE)
        thread_stop_flag = 0
        thread_stop = 0
        _thread.start_new_thread(led_task,())
    while effect_time != "None" and thread_stop_flag == 0:
        time.sleep(0.5)


def effect_stop():
    global thread_stop
    thread_stop = 1
