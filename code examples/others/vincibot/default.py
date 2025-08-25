import sensor, time
import resources.py.draw as draw
import random
mode = 0
linefollowflag = 10
line_following_mode = 0
draw_mode = 0
draw_select = 0
last_draw_select = 0
volume_data = 70
led_count = 0
drawing_flag = 0
last_ir_code_value = 0
move_flag = 0
display_line_following_start_flag = 0
display_drawing_led_matrix_flag = 0
new_draw_select = 0
trun_more_angle = 0
show_xflag = 0
wait_flag = 0
out_forward = 0
speed_mode = 0
history_count = 0



channel_type = 0

THREAD_SIZE = 4 * 1024
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
face_table = [
    [0x00,0x00,0x1c,0x38,0x3e,0x7c,0x2e,0x5c,0x2e,0x5c,0x22,0x44,0x1c,0x38,0x00,0x00],
    [0x00,0x00,0x00,0x00,0x3e,0x7c,0x2e,0x5c,0x2e,0x5c,0x3e,0x7c,0x00,0x00,0x00,0x00],
    [0x00,0x00,0x00,0x00,0x00,0x00,0x3e,0x7c,0x3e,0x7c,0x00,0x00,0x00,0x00,0x00,0x00]
]

audio.set_volume(volume_data)
led_matrix.picture_bank(0,face_table[0],1)
led_matrix.picture_bank(1,face_table[1],1)
led_matrix.picture_bank(2,face_table[2],1)
led_matrix.picture_bank(3,face_table[1],1)
led_matrix.picture_bank(4,face_table[0],200)
led_matrix.set_orientation('turn pages')
led_matrix.auto_play(5, True)



sensors_value = [0, 0, 0, 0, 0]
sensors_value_history = [[0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0]]

max_speed = 100

turn_left_flag = 0
set_point = 0
kp = 0 #set kp Value
ki = 0 #set ki Value
kd = 0 #set kd Value

proportional = 0
integral = 0
derivative = 0
last_proportional = 0
# position 为正是右偏移，为负是左偏移，数值越大，偏移越大
position = 0
error_value = 0
def set_pid(p, i, d):
    global kp, ki, kd
    kp = p
    ki = i
    kd = d

if sensor.get_sensor_channel() == 1 :
    channel_type = 1
    set_pid(0.25, 0, 0.15)
    WHITE_AREA_VALUE = 98
    BLACK_AREA_VALUE = 80
    MIN_SENSOR_DIFF  = 5
else:
    WHITE_AREA_VALUE = 70
    BLACK_AREA_VALUE = 30
    MIN_SENSOR_DIFF  = 30
    set_pid(0.05, 0, 0.05)
    channel_type = 2
min_value = BLACK_AREA_VALUE
max_value = WHITE_AREA_VALUE

def set_speed():
    global max_speed,speed_mode
    speed_mode = speed_mode + 1
    if speed_mode >= 3:
        speed_mode = 0
    if speed_mode == 0:
        max_speed = 100
        audio.play("/sdcard/music/effect/24-aircraft.mp3")
    elif speed_mode == 1:
        max_speed = 80
        audio.play("/sdcard/music/effect/66-medium speed.mp3")
    elif speed_mode == 2:
        max_speed = 50
        audio.play("/sdcard/music/effect/65-low speed.mp3")
    else:
        max_speed = 100
        audio.play("/sdcard/music/effect/24-aircraft.mp3")
        
def sensor_update():
    global sensors_value, color, min_value, max_value, sensors_average, sensors_sum, position, turn_left_flag, sensors_value_history, history_count
    for i in range(5):
        sensors_value[i] = sensor.get_reflection_light(i + 1)
        sensors_value_history[i][history_count] = sensors_value[i]
    if(channel_type == 1):
        # min_value = min(sensors_value[0], sensors_value[3], sensors_value[4])
        # max_value = max(sensors_value[0], sensors_value[3], sensors_value[4])
        min_value = min(sensors_value[0], sensors_value[4])
        max_value = max(sensors_value[0], sensors_value[4])
    else:
        min_value = min(sensors_value[0], sensors_value[1], sensors_value[3], sensors_value[4])
        max_value = max(sensors_value[0], sensors_value[1], sensors_value[3], sensors_value[4])
    sensors_average = 0
    sensors_sum = 0
    for i in range(-2, 3):
        sensors_average = sensors_average + (max_value - sensors_value[i + 2]) * i
        sensors_sum = sensors_sum + (max_value - sensors_value[i + 2])
    if sensors_sum != 0:
        position = int(round(sensors_average * 1000 / sensors_sum))
    black_mask = 0x00
    for i in range(5):
        if sensors_value[i] < BLACK_AREA_VALUE:
            black_mask = black_mask | ((1 << i) & 0xff)
    sensors_value_history[5][history_count] = black_mask
    
    history_count = history_count + 1
    if(history_count == 12):
        history_count = 0
        
def history_direction_offset():
    global history_count, sensors_value_history
    sensors_sum_list = [0, 0, 0, 0 ,0]
    sensors_sum_total = 0
    sensors_sum_average = 0
    for j in range(5):
        for i in range(12):
            if i == history_count or i == (12 + history_count) % 12:
                continue
            sensors_sum_list[j] = sensors_sum_list[j] + sensors_value_history[j][i]

    max_value = max(sensors_sum_list[0], sensors_sum_list[1], sensors_sum_list[2], sensors_sum_list[3], sensors_sum_list[4])
    for i in range(-2, 3):
        sensors_sum_average = sensors_sum_average + (max_value - sensors_sum_list[i + 2]) * i
        sensors_sum_total = sensors_sum_total + (max_value - sensors_sum_list[i + 2])
    if sensors_sum_total != 0:
        direction_offset = int(round(sensors_sum_average * 1000 / sensors_sum_total))
    # print("dir:%d" %(direction_offset))
    return direction_offset

def car_move(left_speed, right_speed):
    # print("l:%d, r:%d" %(left_speed, right_speed))
    motion.set_pwm(-left_speed, right_speed)

def car_stop():
    motion.set_pwm(0, 0)

def map(x, min_in, max_in, min_out, max_out):
    return (x - min_in) * (max_out - min_out) / (max_in - min_in) + min_out

def car_move_out():
    global min_value, max_value, max_speed, sensors_value, turn_left_flag, line_following_mode, history_count, sensors_value_history
    dir_offset = history_direction_offset()
    turn_flag = False
    forward_count = 0
    turn_count = 0
    while True:
        car_ir_command = get_ir_command()
        if  car_ir_command == "play":
            line_following_mode = not line_following_mode
            return
        elif car_ir_command == "speed":
            set_speed()
        # 如果是默认线路
        if turn_flag == False:
            # 往前走 100ms左右
            car_move(int(max_speed), int(max_speed))
            turn_flag = True
        if forward_count > int(1000 / max_speed):
            if(channel_type == 2):
                #左偏
                if dir_offset >= 0:
                    if dir_offset > 1000:
                        dir_offset = 1000
                    speed = int(map(-dir_offset, -1000, 0, -0.4 * max_speed, 0.8 * max_speed))
                    car_move(-int(0.3 * speed), max_speed)
                else:
                    if dir_offset < -1000:
                        dir_offset = -1000
                    speed = int(map(dir_offset, -1000, 0, -0.4 * max_speed, 0.8 * max_speed))
                    car_move(max_speed, -int(0.3 * speed))
            else:
                turn_count = turn_count + 1
                if(turn_count > 0.7 * max_speed * 4 - 40):
                    turn_count = 0.7 * max_speed * 4 - 40
                if turn_left_flag == 1:
                    car_move(-int(0.7 * max_speed - (turn_count / 2)), int(0.8 * max_speed))
                else:
                    car_move(int(0.8 * max_speed), -int(0.7 * max_speed - (turn_count / 2)))

        sensor_update()
        time.sleep(0.01)
        if turn_flag == True:
            forward_count = forward_count + 1

        #有差值，即找到明显的黑色区域了，退出该程序
        black_mask = sensors_value_history[5][(12 + history_count - 1) % 12]
        if min_value < BLACK_AREA_VALUE:# and (max_value - min_value) >  MIN_SENSOR_DIFF:
            # leds.show_single(1, 0, 0, 0)
            turn_flag = False
            forward_count = 0
            turn_left_flag = 0
            return

def pid_calc():
    global position, integral, set_point, last_proportional, kp, ki, kd, error_value
    proportional = position - set_point
    integral = integral + proportional
    derivative = proportional - last_proportional
    last_proportional = proportional
    error_value = int(round(proportional * kp + integral * ki + derivative * kd))

def calc_turn():
    global max_speed, error_value
    #Restricting the error value between +256. 
    right_speed = 0
    left_speed = 0

    if (error_value < -(1.5 * max_speed)):
        error_value = -int(1.5 * max_speed)
    if (error_value > (1.5 * max_speed)):
        error_value = int(1.5 * max_speed)
    #If error_value is less than zero calculate right turn speed values
    if (error_value < 0):
        if(channel_type == 2):
            if(error_value > -20):
                error_value = int(0.3 * error_value)
        else:
            if(error_value > -80):
                error_value = int(0.4 * error_value)
        right_speed = max_speed + error_value
        left_speed = max_speed
    else:
        if(channel_type == 2):
            if(error_value < 20):
                error_value = int(0.3 * error_value)
        else:
            if(error_value < 80):
                error_value = int(0.4 * error_value)
        if (error_value < -(1.5 * max_speed)):
            error_value = -int(1.5 * max_speed)
        if (error_value > (1.5 * max_speed)):
            error_value = int(1.5 * max_speed)
        right_speed = max_speed
        left_speed = max_speed - error_value
    car_move(left_speed, right_speed)

def display_drawing_led_matrix():
    global display_line_following_start_flag
    display_drawing_delay = 0.2
    print("display_drawing_led_matrix!\n")
    while(display_line_following_start_flag == 1):
        time.sleep(0.1)
    display_drawing_led_matrix_flag = 1
    while True:
        if((draw_mode == 1)|(mode !=2)|(draw_select !=0)):
            print("break!\n")
            led_matrix.clear()
            display_drawing_led_matrix_flag = 0
            break
        led_matrix.clear()
        for i in range(3, 16):
            led_matrix.set_pixel(i, 0, 100)
            led_matrix.set_pixel(i, 1, 100)
            led_matrix.set_pixel(i, 2, 100)

            if(i > 0):
                led_matrix.set_pixel(i-1, 0, 100)
                led_matrix.set_pixel(i-1, 1, 0)
                led_matrix.set_pixel(i-1, 2, 100)

            if(i > 1):
                led_matrix.set_pixel(i-2, 0, 100)
                led_matrix.set_pixel(i-2, 1, 100)
                led_matrix.set_pixel(i-2, 2, 100)

            if(i == 3):
                led_matrix.set_pixel(i-3, 0, 0)
                led_matrix.set_pixel(i-3, 1, 0)
                led_matrix.set_pixel(i-3, 2, 0)
            if(i > 3):
                led_matrix.set_pixel(i-3, 0, 0)
                led_matrix.set_pixel(i-3, 1, 100)
                led_matrix.set_pixel(i-3, 2, 0)
            if((draw_mode == 1)|(mode !=2)|(draw_select !=0)):
                led_matrix.clear()
                display_drawing_led_matrix_flag = 0
                break
            time.sleep(display_drawing_delay)

        for i in range(3, 8):
            led_matrix.set_pixel(13, i, 100)
            led_matrix.set_pixel(14, i, 100)
            led_matrix.set_pixel(15, i, 100)

            led_matrix.set_pixel(13, i-1, 100)
            led_matrix.set_pixel(14, i-1, 0)
            led_matrix.set_pixel(15, i-1, 100)

            led_matrix.set_pixel(13, i-2, 100)
            led_matrix.set_pixel(14, i-2, 100)
            led_matrix.set_pixel(15, i-2, 100)

            if(i == 3):
                led_matrix.set_pixel(13, i-3, 0)
                led_matrix.set_pixel(14, i-3, 0)
                led_matrix.set_pixel(15, i-3, 0)

            if(i == 4):
                led_matrix.set_pixel(15, i-3, 0)

            if(i > 4):
                led_matrix.set_pixel(13, i-3, 0)
                led_matrix.set_pixel(14, i-3, 100)
                led_matrix.set_pixel(15, i-3, 0)
            if((draw_mode == 1)|(mode !=2)|(draw_select !=0)):
                led_matrix.clear()
                display_drawing_led_matrix_flag = 0
                break
            time.sleep(display_drawing_delay)

        for i in range(12, -1, -1):
            led_matrix.set_pixel(i, 5, 100)
            led_matrix.set_pixel(i, 6, 100)
            led_matrix.set_pixel(i, 7, 100)

            if(i < 13):
                led_matrix.set_pixel(i+1, 5, 100)
                led_matrix.set_pixel(i+1, 6, 0)
                led_matrix.set_pixel(i+1, 7, 100)

            if(i < 13):
                led_matrix.set_pixel(i+2, 5, 100)
                led_matrix.set_pixel(i+2, 6, 100)
                led_matrix.set_pixel(i+2, 7, 100)

            if(i == 12):
                led_matrix.set_pixel(i+3, 5, 0)
                led_matrix.set_pixel(i+3, 6, 0)
                led_matrix.set_pixel(i+3, 7, 0)

            if(i == 11):
                led_matrix.set_pixel(i+3, 7, 0)

            if(i < 11):
                led_matrix.set_pixel(i+3, 5, 0)
                led_matrix.set_pixel(i+3, 6, 100)
                led_matrix.set_pixel(i+3, 7, 0)
            if((draw_mode == 1)|(mode !=2)|(draw_select !=0)):
                led_matrix.clear()
                display_drawing_led_matrix_flag = 0
                break
            time.sleep(display_drawing_delay)

        for i in range(4, -1, -1):
            led_matrix.set_pixel(0, i, 100)
            led_matrix.set_pixel(1, i, 100)
            led_matrix.set_pixel(2, i, 100)

            led_matrix.set_pixel(0, i+1, 100)
            led_matrix.set_pixel(1, i+1, 0)
            led_matrix.set_pixel(2, i+1, 100)

            led_matrix.set_pixel(0, i+2, 100)
            led_matrix.set_pixel(1, i+2, 100)
            led_matrix.set_pixel(2, i+2, 100)

            if(i == 4):
                led_matrix.set_pixel(0, i+3, 0)
                led_matrix.set_pixel(1, i+3, 0)
                led_matrix.set_pixel(2, i+3, 0)

            if(i == 3):
                led_matrix.set_pixel(0, i+3, 0)

            if(i < 3):
                led_matrix.set_pixel(0, i+3, 0)
                led_matrix.set_pixel(1, i+3, 100)
                led_matrix.set_pixel(2, i+3, 0)
            if((draw_mode == 1)|(mode !=2)|(draw_select !=0)):
                led_matrix.clear()
                display_drawing_led_matrix_flag = 0
                break
            time.sleep(display_drawing_delay)
    led_matrix.clear()
    display_drawing_led_matrix_flag = 0

def display_line_following_wait_start_led_matrix():
    display_line_following_wait_start_line_delay = 0.01
    display_line_following_wait_start_delay = 0.05
    led_matrix.clear()
    for i in range(1, 15):
        led_matrix.set_pixel(i, 1, 100)
        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_line_delay)
    for i in range(2, 7):
        led_matrix.set_pixel(14, i, 100)
        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_line_delay)
    for i in range(13, 0, -1):
        led_matrix.set_pixel(i, 6, 100)
        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_line_delay)
    for i in range(5, 1, -1):
        led_matrix.set_pixel(1, i, 100)
        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_line_delay)

    for i in range(2, 16):
        led_matrix.set_pixel(i, 0, 100)
        led_matrix.set_pixel(i, 1, 100)
        led_matrix.set_pixel(i, 2, 100)

        if(i > 0):
            led_matrix.set_pixel(i-1, 0, 100)
            led_matrix.set_pixel(i-1, 1, 0)
            led_matrix.set_pixel(i-1, 2, 100)

        if(i > 1):
            led_matrix.set_pixel(i-2, 0, 100)
            led_matrix.set_pixel(i-2, 1, 100)
            led_matrix.set_pixel(i-2, 2, 100)

        if(i == 3):
            led_matrix.set_pixel(i-3, 0, 0)
            led_matrix.set_pixel(i-3, 1, 0)
            led_matrix.set_pixel(i-3, 2, 0)
        
        if(i == 4):
            led_matrix.set_pixel(i-3, 0, 0)
            led_matrix.set_pixel(i-3, 1, 100)
            led_matrix.set_pixel(i-3, 2, 100)

        if(i > 4):
            led_matrix.set_pixel(i-3, 0, 0)
            led_matrix.set_pixel(i-3, 1, 100)
            led_matrix.set_pixel(i-3, 2, 0)

        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_delay)

    for i in range(3, 8):
        led_matrix.set_pixel(13, i, 100)
        led_matrix.set_pixel(14, i, 100)
        led_matrix.set_pixel(15, i, 100)

        led_matrix.set_pixel(13, i-1, 100)
        led_matrix.set_pixel(14, i-1, 0)
        led_matrix.set_pixel(15, i-1, 100)

        led_matrix.set_pixel(13, i-2, 100)
        led_matrix.set_pixel(14, i-2, 100)
        led_matrix.set_pixel(15, i-2, 100)

        if(i == 3):
            led_matrix.set_pixel(13, i-3, 0)
            led_matrix.set_pixel(14, i-3, 0)
            led_matrix.set_pixel(15, i-3, 0)

        if(i == 4):
            led_matrix.set_pixel(15, i-3, 0)

        if(i > 4):
            led_matrix.set_pixel(13, i-3, 0)
            led_matrix.set_pixel(14, i-3, 100)
            led_matrix.set_pixel(15, i-3, 0)
        
        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_delay)

    for i in range(12, -1, -1):
        led_matrix.set_pixel(i, 5, 100)
        led_matrix.set_pixel(i, 6, 100)
        led_matrix.set_pixel(i, 7, 100)

        if(i < 13):
            led_matrix.set_pixel(i+1, 5, 100)
            led_matrix.set_pixel(i+1, 6, 0)
            led_matrix.set_pixel(i+1, 7, 100)

        if(i < 13):
            led_matrix.set_pixel(i+2, 5, 100)
            led_matrix.set_pixel(i+2, 6, 100)
            led_matrix.set_pixel(i+2, 7, 100)

        if(i == 12):
            led_matrix.set_pixel(i+3, 5, 0)
            led_matrix.set_pixel(i+3, 6, 0)
            led_matrix.set_pixel(i+3, 7, 0)

        if(i == 11):
            led_matrix.set_pixel(i+3, 7, 0)

        if(i < 11):
            led_matrix.set_pixel(i+3, 5, 0)
            led_matrix.set_pixel(i+3, 6, 100)
            led_matrix.set_pixel(i+3, 7, 0)

        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_delay)

    for i in range(4, -1, -1):
        led_matrix.set_pixel(0, i, 100)
        led_matrix.set_pixel(1, i, 100)
        led_matrix.set_pixel(2, i, 100)

        led_matrix.set_pixel(0, i+1, 100)
        led_matrix.set_pixel(1, i+1, 0)
        led_matrix.set_pixel(2, i+1, 100)

        led_matrix.set_pixel(0, i+2, 100)
        led_matrix.set_pixel(1, i+2, 100)
        led_matrix.set_pixel(2, i+2, 100)

        if(i == 4):
            led_matrix.set_pixel(0, i+3, 0)
            led_matrix.set_pixel(1, i+3, 0)
            led_matrix.set_pixel(2, i+3, 0)

        if(i == 3):
            led_matrix.set_pixel(0, i+3, 0)

        if(i < 3):
            led_matrix.set_pixel(0, i+3, 0)
            led_matrix.set_pixel(1, i+3, 100)
            led_matrix.set_pixel(2, i+3, 0)

        if((mode != 1)):
            print("return!\n")
            return 1
        time.sleep(display_line_following_wait_start_delay)

def display_line_following_start_led_matrix():
    global mode, line_following_mode, display_line_following_start_flag
    display_line_following_start_flag = 1
    if(display_line_following_wait_start_led_matrix() == 1):
        print("return display_line_following_start_led_matrix!\n")
        display_line_following_start_flag = 0
        led_matrix.clear()
        return

    display_line_following_start_line_delay = 0.01
    display_line_following_start_delay = 0.2
    # led_matrix.clear()
    # for i in range(1, 15):
    #     led_matrix.set_pixel(i, 1, 100)
    #     time.sleep(display_line_following_start_line_delay)
    # for i in range(2, 7):
    #     led_matrix.set_pixel(14, i, 100)
    #     time.sleep(display_line_following_start_line_delay)
    # for i in range(13, 0, -1):
    #     led_matrix.set_pixel(i, 6, 100)
    #     time.sleep(display_line_following_start_line_delay)
    # for i in range(5, 1, -1):
    #     led_matrix.set_pixel(1, i, 100)
    #     time.sleep(display_line_following_start_line_delay)

    while True:
        #led_matrix.clear()
        #暂停模式 不继续执行

        if((mode != 1)):
            print("break!\n")
            display_line_following_start_flag = 0
            led_matrix.clear()
            break
        while((line_following_mode == 0) & (mode == 1)):
            # print("line_following_mode == 0")
            time.sleep(0.5)
        for i in range(2, 16):
            led_matrix.set_pixel(i, 0, 100)
            led_matrix.set_pixel(i, 1, 100)
            led_matrix.set_pixel(i, 2, 100)

            if(i > 0):
                led_matrix.set_pixel(i-1, 0, 100)
                led_matrix.set_pixel(i-1, 1, 0)
                led_matrix.set_pixel(i-1, 2, 100)

            if(i > 1):
                led_matrix.set_pixel(i-2, 0, 100)
                led_matrix.set_pixel(i-2, 1, 100)
                led_matrix.set_pixel(i-2, 2, 100)

            if(i == 3):
                led_matrix.set_pixel(i-3, 0, 0)
                led_matrix.set_pixel(i-3, 1, 0)
                led_matrix.set_pixel(i-3, 2, 0)
            
            if(i == 4):
                led_matrix.set_pixel(i-3, 0, 0)
                led_matrix.set_pixel(i-3, 1, 100)
                led_matrix.set_pixel(i-3, 2, 100)

            if(i > 4):
                led_matrix.set_pixel(i-3, 0, 0)
                led_matrix.set_pixel(i-3, 1, 100)
                led_matrix.set_pixel(i-3, 2, 0)

            if((mode != 1)):
                print("break!\n")
                display_line_following_start_flag = 0
                led_matrix.clear()
                break
            while((line_following_mode == 0) & (mode == 1)):
                # print("line_following_mode == 0")
                time.sleep(0.5)
            time.sleep(display_line_following_start_delay)

        for i in range(3, 8):
            led_matrix.set_pixel(13, i, 100)
            led_matrix.set_pixel(14, i, 100)
            led_matrix.set_pixel(15, i, 100)

            led_matrix.set_pixel(13, i-1, 100)
            led_matrix.set_pixel(14, i-1, 0)
            led_matrix.set_pixel(15, i-1, 100)

            led_matrix.set_pixel(13, i-2, 100)
            led_matrix.set_pixel(14, i-2, 100)
            led_matrix.set_pixel(15, i-2, 100)

            if(i == 3):
                led_matrix.set_pixel(13, i-3, 0)
                led_matrix.set_pixel(14, i-3, 0)
                led_matrix.set_pixel(15, i-3, 0)

            if(i == 4):
                led_matrix.set_pixel(15, i-3, 0)

            if(i > 4):
                led_matrix.set_pixel(13, i-3, 0)
                led_matrix.set_pixel(14, i-3, 100)
                led_matrix.set_pixel(15, i-3, 0)
            
            if((mode != 1)):
                print("break!\n")
                display_line_following_start_flag = 0
                led_matrix.clear()
                break
            while((line_following_mode == 0) & (mode == 1)):
                # print("line_following_mode == 0")
                time.sleep(0.5)
            time.sleep(display_line_following_start_delay)

        for i in range(12, -1, -1):
            led_matrix.set_pixel(i, 5, 100)
            led_matrix.set_pixel(i, 6, 100)
            led_matrix.set_pixel(i, 7, 100)

            if(i < 13):
                led_matrix.set_pixel(i+1, 5, 100)
                led_matrix.set_pixel(i+1, 6, 0)
                led_matrix.set_pixel(i+1, 7, 100)

            if(i < 13):
                led_matrix.set_pixel(i+2, 5, 100)
                led_matrix.set_pixel(i+2, 6, 100)
                led_matrix.set_pixel(i+2, 7, 100)

            if(i == 12):
                led_matrix.set_pixel(i+3, 5, 0)
                led_matrix.set_pixel(i+3, 6, 0)
                led_matrix.set_pixel(i+3, 7, 0)

            if(i == 11):
                led_matrix.set_pixel(i+3, 7, 0)

            if(i < 11):
                led_matrix.set_pixel(i+3, 5, 0)
                led_matrix.set_pixel(i+3, 6, 100)
                led_matrix.set_pixel(i+3, 7, 0)

            if((mode != 1)):
                print("break!\n")
                display_line_following_start_flag = 0
                led_matrix.clear()
                break
            while((line_following_mode == 0) & (mode == 1)):
                # print("line_following_mode == 0")
                time.sleep(0.5)
            time.sleep(display_line_following_start_delay)

        for i in range(4, -1, -1):
            led_matrix.set_pixel(0, i, 100)
            led_matrix.set_pixel(1, i, 100)
            led_matrix.set_pixel(2, i, 100)

            led_matrix.set_pixel(0, i+1, 100)
            led_matrix.set_pixel(1, i+1, 0)
            led_matrix.set_pixel(2, i+1, 100)

            led_matrix.set_pixel(0, i+2, 100)
            led_matrix.set_pixel(1, i+2, 100)
            led_matrix.set_pixel(2, i+2, 100)

            if(i == 4):
                led_matrix.set_pixel(0, i+3, 0)
                led_matrix.set_pixel(1, i+3, 0)
                led_matrix.set_pixel(2, i+3, 0)

            if(i == 3):
                led_matrix.set_pixel(0, i+3, 0)

            if(i < 3):
                led_matrix.set_pixel(0, i+3, 0)
                led_matrix.set_pixel(1, i+3, 100)
                led_matrix.set_pixel(2, i+3, 0)

            if((mode != 1)):
                print("break!\n")
                display_line_following_start_flag = 0
                led_matrix.clear()
                break
            while((line_following_mode == 0) & (mode == 1)):
                # print("line_following_mode == 0")
                time.sleep(0.5)
            time.sleep(display_line_following_start_delay)
        while((line_following_mode == 0) & (mode == 1)):
            # print("line_following_mode == 0")
            time.sleep(0.5)

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

def led_task():
    global led_count,led_color
    r_led = 0
    g_led = 120
    b_led = 255
    r_led_tepm = 5
    g_led_tepm = 5
    b_led_tepm = -5
    led_sleep_time = 0
    mode_3_stop_falg = 0
    led_mode2_index = [1,2,3]
    random_list = [1,2,3,4,5,6]
    while(True):
        time.sleep(0.02)
        if(led_count == 0):
            #关灯
            if(mode_3_stop_falg == 0):
                leds.show_all(0, 0, 0)
                led_mode3_index = 0
                led_mode2_index = [1,2,3]
                random_list = random_shuffle(random_list)
                mode_3_stop_falg = 1
        elif(led_count == 1):
            #呼吸灯
            if(r_led >= 255):
                r_led_tepm = -5
            elif(r_led <= 0):
                r_led_tepm = 5
            if(g_led >= 255):
                g_led_tepm = -5
            elif(g_led <= 0):
                g_led_tepm = 5
            if(b_led >= 255):
                b_led_tepm = -5
            elif(b_led <= 0):
                b_led_tepm = 5
            r_led = r_led + r_led_tepm
            g_led = g_led + g_led_tepm
            b_led = b_led + b_led_tepm
            leds.show_all(r_led, g_led, b_led)
        elif(led_count == 2):
            #跑马灯
            time.sleep(0.2)
            leds.show_all(0, 0, 0)
            led_mode2_index[0] = led_mode2_index[0] + 1
            led_mode2_index[1] = led_mode2_index[1] + 1
            led_mode2_index[2] = led_mode2_index[2] + 1
            if(led_mode2_index[0] > 6):
                led_mode2_index[0] = led_mode2_index[0] -6
            if(led_mode2_index[1] > 6):
                led_mode2_index[1] = led_mode2_index[1] -6
            if(led_mode2_index[2] > 6):
                led_mode2_index[2] = led_mode2_index[2] -6
            leds.show_single(led_mode2_index[0],255,0,0)
            leds.show_single(led_mode2_index[1],0,255,0)
            leds.show_single(led_mode2_index[2],0,0,255)
        elif(led_count == 3):
            #随机逐个点亮
            if(mode_3_stop_falg == 1):
                mode_3_stop_falg = 0            
                leds.show_all(0, 0, 0)
            time.sleep(0.2)
            led_sleep_time = led_sleep_time + 1
            if(led_mode3_index >= 6):
                random_list = random_shuffle(random_list)
                leds.show_all(0, 0, 0)
                led_mode3_index = 0
            if(led_sleep_time >= 5):
                led_mode3_index = led_mode3_index + 1
                led_sleep_time = 0
            led_color_index = random.randint(1,10)
            led_rgb_color = led_color.get(led_color_index,[])
            leds.show_single(random_list[led_mode3_index - 1], led_rgb_color[0],led_rgb_color[1],led_rgb_color[2])
        elif(led_count == 4):
            time.sleep(0.02)

def draw_task():
    global draw_mode, draw_select, drawing_flag, last_draw_select
    print("draw_task\n")
    while 1:
        if(drawing_flag == 1):
            gcode_file = "/resources/gcode/square.gcode"
            if(draw_select == 1):
                gcode_file = "/resources/gcode/square.gcode"
            elif draw_select == 2:
                gcode_file = "/resources/gcode/pentagram.gcode"
            elif draw_select == 3:
                gcode_file = "/resources/gcode/plane.gcode"
            with open(gcode_file, "r") as f:
                if ((mode != 2) or (new_draw_select == 1)):
                    print("break drawing mode1\n")
                    f.close()
                    drawing_flag = 0
                    return
                line = f.readline()
                while line:
                    if ((mode != 2) or (new_draw_select == 1)):
                        print("break drawing mode2\n")
                        break
                    print("readline:%s" %line)
                    #time.sleep(1)
                    draw.processGcode(line)

                    #暂停模式 不继续执行
                    while((draw_mode == 0) & (mode == 2) & (new_draw_select == 0)):
                        print("draw_mode == 0")
                        time.sleep(0.5)
                    
                    if ((mode != 2) or (new_draw_select == 1)):
                        print("break drawing mode3\n")
                        break
                    line = f.readline()
            f.close()
            #if((new_draw_select != 1)):
            draw_mode = 0
            drawing_flag = 0
            last_draw_select = 0
            print("read file end!\r\n")
        else:
            time.sleep(0.1)


def get_ir_command():
    global last_ir_code_value
    while True:
        new_ir_code_value = sensor.get_ir_code()

        #print("new_ir_code: " + str(new_ir_code_value))

        #当收到四个方向键，当做最终按键值，直接跳出
        if((new_ir_code_value == "left") | (new_ir_code_value == "right") | (new_ir_code_value == "forward") | (new_ir_code_value == "backward")):
            #print("direction ir code\n")
            ir_code_value = new_ir_code_value
            last_ir_code_value = new_ir_code_value
            return ir_code_value
        #当收到非方向键,必须等待按键抬起，也就是收到0时，才返回.
        #后续考虑实现：或者收到非方向键,超过xx ms内未收到0或其他按键，也返回按键值。
        else:
            if(new_ir_code_value == 0):
                if(last_ir_code_value == 0):
                    ir_code_value = 0
                    last_ir_code_value = new_ir_code_value
                    return ir_code_value
                else:
                    ir_code_value = last_ir_code_value
                    last_ir_code_value = new_ir_code_value
                    return ir_code_value
            else:
                last_ir_code_value = new_ir_code_value
#工作模式分为：遥控模式，巡线模式，画画模式，（巡线模式，画画模式下）只有在暂停模式下可以切换工作模式
#巡线模式分为：开始，暂停
#画画模式分为：选择图案，开始，暂停

        
def ir_command_process(command):
    global mode, line_following_mode, draw_mode, draw_select, drawing_flag, volume_data, led_count, display_drawing_led_matrix_flag, last_draw_select, new_draw_select
    global linefollowflag, move_flag, trun_more_angle, loca_time, show_xflag, wait_flag, out_forward, turn_flag, out_light, turn_left_flag
    #ir_code_value = sensor.get_ir_code()
    #print("ir_code_value:" + str(ir_code_value))
    #print(ir_code_value)
    #遥控模式
    global  sensors_value, color, min_value, max_value, max_speed, position
    
    if mode == 0:
        if(show_xflag == 1):
            loca_time = time.time()
            led_matrix.show_image(bytearray([0x00,0x00,0x10,0x22,0x10,0x14,0x7c,0x08,0x10,0x14,0x10,0x22,0x00,0x00,0x00,0x00]), "None")
            show_xflag = 0
            wait_flag = 1
        elif(wait_flag == 1):
            wait_time = time.time() - loca_time
            if(wait_time > 5):
                wait_flag = 0
                led_matrix.picture_bank(0,face_table[0],1)
                led_matrix.picture_bank(1,face_table[1],1)
                led_matrix.picture_bank(2,face_table[2],1)
                led_matrix.picture_bank(3,face_table[1],1)
                led_matrix.picture_bank(4,face_table[0],200)
                led_matrix.set_orientation('turn pages')
                led_matrix.auto_play(5, True)
                print('draw face')
        if  command == "play":
            #暂停
                audio.play_stop()
        elif command == 'dance':
            #舞蹈
            led_last_count = led_count
            led_count = 4
            time.sleep(0.2)
            leds.show_all(0, 0, 0)
            dance_index = random.randint(1,6)
            action.dance(dance_index)
            led_count = led_last_count
        elif command == 'music' :
            #音乐
            sing_index = random.randint(1,6)
            audio.sing(str(sing_index))
        elif command == 'led' :
            #led模式
            #leds.show_all(0, 0, 0)
            led_count = led_count + 1
            if led_count > 3 :
                led_count = 0
        elif command == "forward":
            #前进
            move_flag = 1
            car_move(max_speed, max_speed)
        elif command == "backward":
            #后退
            move_flag = 1
            car_move(-max_speed, -max_speed)
        elif command == "left":
            #左转
            move_flag = 1
            car_move(-max_speed, max_speed)
        elif command == "right":
            #右转
            move_flag = 1
            car_move(max_speed, -max_speed)
        elif command == "volume":
            #音量
            if(volume_data == 50):
                volume_data = 70
            elif(volume_data == 70):
                volume_data = 90
            elif(volume_data == 90):
                volume_data = 50
            else:
                volume_data = 70
            audio.set_volume(volume_data)
            audio.play("/sdcard/music/effect/28-score.mp3")
        elif command == "speed":
            #速度
            set_speed()
        elif command == "mode":
            #模式切换  1
            print("mode 1 mode ")
            mode = 1
            led_matrix.clear()
            _thread.stack_size(THREAD_SIZE)
            _thread.start_new_thread(display_line_following_start_led_matrix, (), 1, 2)
            #audio.play_say("english", "Line following mode", sync = False)
            led_twinkle()
            #显示Line following表情面板
        else:
            if(move_flag == 1):
                move_flag = 0
                motion.stop(2)

    #巡线模式
    elif mode == 1:
        #Play巡线开始，暂停模式切换，在暂停模式下，模式按键可切换工作模式
        if  command == "speed":
            set_speed()
        if command == "mode":
            #在暂停模式下，模式按键可切换工作模式
            if line_following_mode == 0:
                mode = 2
                _thread.stack_size(THREAD_SIZE)
                _thread.start_new_thread(display_drawing_led_matrix, (), 1, 2)
                #audio.play_say("english", "Drawing mode", sync = False)
                led_twinkle()
                #audio.play_say("english", "Drawing mode", sync = True)
                print("mode 2 mode ")
        elif command == "play":
            #Play巡线开始，暂停模式切换
            line_following_mode = not line_following_mode
            print("mode 1 play " + str(line_following_mode))
            if(line_following_mode == 1):
                move_flag = 1
                trun_more_angle = 0
        elif line_following_mode == 1:
            sensor_update()
            if(channel_type == 2):
                if sensors_value[2] == 0:
                    car_stop()
            #两边在白色区域
            if min_value >= WHITE_AREA_VALUE:
                if(position != 0):
                    if position > 0:
                        turn_left_flag = 1
                    else :
                        turn_left_flag = 2
                car_move_out()

            #全部是黑色区域
            elif max_value <= BLACK_AREA_VALUE:
                #小车被抬起
                if(channel_type == 2):
                    if sensors_value[2] <= min_value / 3:
                        position = 0
                        car_stop()
                    else:
                        position = 0
                    car_move(int(max_speed), int(max_speed))
                # #黑线情况, 不计算偏移，直接前进
                else:
                    position = 0
                    car_move(int(max_speed), int(max_speed))
            else:
                pid_calc()
                calc_turn()
        else:
            if(move_flag == 1):
                move_flag = 0
                motion.stop(2)
    #画画模式，开始，暂停模式切换，在画画暂停模式下，1,2,3切换图案，模式按键切换工作模式
    elif mode == 2:
        #Play开始画画，暂停模式切换，只有暂停模式才可切换工作模式
        if command == "mode":
            if draw_mode == 0:
                mode = 0
                draw_select = 0
                show_xflag = 1
                loca_time = time.time()
                print("mode 0 mode ")
                #audio.play_say("english", "Remote control mode", sync = False)
                led_twinkle()
                led_matrix.show_image(bytearray([0x00,0x00,0x10,0x22,0x10,0x14,0x7c,0x08,0x10,0x14,0x10,0x22,0x00,0x00,0x00,0x00]), "None")
                #显示画画表情面板
                #显示LED
        elif command == "play":
            if(draw_select != 0):
                if(last_draw_select != draw_select):
                    if(last_draw_select != 0):
                        new_draw_select = 1
                    while(drawing_flag):
                        time.sleep(0.02)
                    new_draw_select = 0
                    draw_mode = not draw_mode
                    last_draw_select = draw_select
                    drawing_flag = 1
                else:
                    draw_mode = not draw_mode
        elif command == '1':
            #显示图案1
            draw_select = 1
            #last_draw_select = 1
            while(display_drawing_led_matrix_flag == 1):
                time.sleep(0.2)
            time.sleep(0.5)

            led_matrix.show_image(bytearray([0x00,0x01,0x80,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x00,0x01,0x80,0x03,0x00,0x00]), "None")
        elif command == '2':
            #显示图案2
            draw_select = 2
            while(display_drawing_led_matrix_flag == 1):
                time.sleep(0.2)
            time.sleep(0.5)
            led_matrix.show_image(bytearray([0x80,0x03,0x40,0x04,0x00,0x04,0x00,0x03,0x80,0x00,0x40,0x00,0xc0,0x07,0x00,0x00]), "None")
        elif command == '3':
            #显示图案3
            draw_select = 3
            while(display_drawing_led_matrix_flag == 1):
                time.sleep(0.2)
            time.sleep(0.5)
            led_matrix.show_image(bytearray([0xc0,0x07,0x00,0x04,0x00,0x02,0x00,0x03,0x00,0x04,0x40,0x04,0x80,0x03,0x00,0x00]), "None")
_thread.start_new_thread(led_task,())
_thread.stack_size(THREAD_SIZE)
_thread.start_new_thread(draw_task, ())
#led_twinkle()
loca_time = time.time()
while True:
    ir_command = get_ir_command()
    ir_command_process(ir_command)

    time.sleep(0.02)
