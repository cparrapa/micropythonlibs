
# More details can be found in TechToTinker.blogspot.com   
# George Bantique | tech.to.tinker@gmail.com  
from time import sleep_ms  
from time import ticks_ms  
from rotary_irq import RotaryIRQ  
from machine import Pin, SoftI2C  
from machine import RTC  
from ssd1306 import SSD1306_I2C   
led = Pin(2, Pin.OUT)  
rsw = Pin(26, Pin.IN)  
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=400000)   
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)   
r = RotaryIRQ(pin_num_clk=18,   
        pin_num_dt=19,   
        min_val=0,   
        max_val=19,   
        reverse=True,   
        range_mode=RotaryIRQ.RANGE_WRAP)        
val_old = r.value()
val_new = 0
rtc = RTC()  
rtc.datetime((2021, 4, 11, 0, 10, 12, 0, 0))  
# rtc.datetime((YYYY, MM, DD, WD, HH, MM, SS, MS))  
# WD 0 = Monday  
# WD 6 = Sunday  
menus = ['Blink LED',  
    'Activate LED',  
    'Invert OLED',  
    'Display Time',  
    'Display Date',  
    'Display Weekday',  
    'Menu 6',  
    'Menu 7',  
    'Menu 8',  
    'Menu 9',  
    'Menu 10',  
    'Menu 11',  
    'Menu 12']  
working_idx = 0  
sel_menu_idx = 0  
menu_idx = 0  
prev_time = ticks_ms()  
isBlinkLED = False  
isActiveLED = False  
isInvertOLED = False  
isDisplayTime = False  
isDisplayDate = False  
isDisplayWkday = False  
def print_menu(rotary_dir=0):  
    NUM_MENU_LINE = 5  
    global menus  
    global working_idx  
    global sel_menu_idx  
    global menu_idx  
    print_cnt = 0  
    menu_x_pos = 10 # default x position  
    menu_y_pos = 10 # default y position, will be updated every menu printed by 10  
    # Clear the screen  
    oled.fill_rect(0, 9, 128, 55, 0)  
    # Create the working index  
    # It can only have a value of 0 to len(menus)-1  
    working_idx += rotary_dir  
    if working_idx < 0:  
        working_idx = 0  
    elif working_idx > len(menus) - 1:  
        working_idx = len(menus) - 1  
# Create the selected menu  
# It can only have a value of  
# 0, 1, 2, 3, 4  
# to create 5 lines of menus
    if working_idx > 1 and working_idx < len(menus)-2:  
        sel_menu_idx = 2  
    elif working_idx == len(menus)-2:  
        sel_menu_idx = 3  
    elif working_idx == len(menus)-1:  
        sel_menu_idx = 4  
    else:  
        sel_menu_idx = working_idx  
    if working_idx < 2:  
        menu_idx = 0  
    elif working_idx > len(menus)-NUM_MENU_LINE + 1:  
        menu_idx = len(menus)-NUM_MENU_LINE  
    else:  
        menu_idx = working_idx - 2  
    for i in range(menu_idx, len(menus), 1):  
        if print_cnt < NUM_MENU_LINE:  
            if print_cnt == sel_menu_idx:  
            #oled.fill_rect(x, y, w, h, col)  
                oled.fill_rect(0, ( ( ( sel_menu_idx + 1 ) * 10 ) -1 ), 128, 9, 1)  
                oled.text(menus[i], menu_x_pos, menu_y_pos, 0)  
            else:  
                oled.text(menus[i], menu_x_pos, menu_y_pos, 1)  
                oled.show()
                menu_y_pos+=10
                print_cnt+=1  
# Prints the header  
oled.text('Rotary Encoder:', 0, 0)   
# Prints the initial menus  
print_menu()

while True:  
    if ticks_ms() - prev_time >= 200:  
        val_new = r.value()  
    if val_old != val_new:  
        if val_old == 0 and val_new == 19:  
            val_dif = -1  
        elif val_old == 19 and val_new == 0:  
            val_dif = 1  
        else:  
            val_dif = val_new - val_old
        print_menu(val_dif)  
        val_old = val_new  
    if rsw.value()==1:  
        if working_idx==0: # Blink LED  
            isBlinkLED = not isBlinkLED  
            isActiveLED = False  
            if isBlinkLED:  
                oled.fill_rect(0, 9, 128, 55, 0)  
                msg = 'Blinking LED'  
                print('Status: {}'.format(msg))  
                oled.text(msg, 63-len(msg)*8//2, 40)  
                oled.show()  
            else:  
                print_menu()  
        elif working_idx==1: # Activate LED  
            isActiveLED = not isActiveLED  
            isBlinkLED = False  
            if isActiveLED:  
                oled.fill_rect(0, 9, 128, 55, 0)  
                msg = 'LED activated'  
                print('Status: {}'.format(msg))  
                oled.text(msg, 63-len(msg)*8//2, 40)  
                oled.show()  
            else:  
                print_menu()  
        elif working_idx==2: # Invert OLED  
            isInvertOLED = not isInvertOLED  
            oled.invert(isInvertOLED)  
            oled.show()  
        elif working_idx==3: # Display Time  
            isDisplayTime = not isDisplayTime  
            isDisplayDate = False  
            isDisplayWkday = False  
            if isDisplayTime:  
                oled.fill_rect(0, 9, 128, 55, 0)  
                t = rtc.datetime()  
                time = '{:02d}:{:02d}'.format(t[4],t[5])  
                print('Time: {}'.format(time))  
                oled.text(time, 63-len(time)*8//2, 40)  
                oled.show()  
            else:  
                print_menu()  
        elif working_idx==4: # Display Date  
            isDisplayTime = False  
            isDisplayDate = not isDisplayDate  
            isDisplayWkday = False  
            if isDisplayDate:  
                oled.fill_rect(0, 9, 128, 55, 0)  
                t = rtc.datetime()  
                date = '{:04d}-{:02d}-{:02d}'.format(t[0],t[1],t[2])  
                print('Date: {}'.format(date))  
                oled.text(date, 63-len(date)*8//2, 40)  
                oled.show()  
            else:  
                print_menu()  
        elif working_idx==5: # Display Weekday  
            isDisplayTime = False  
            isDisplayDate = False  
            isDisplayWkday = not isDisplayWkday  
            if isDisplayWkday:  
                oled.fill_rect(0, 9, 128, 55, 0)  
                t = rtc.datetime()  
                if t[3]==0:  
                    wkday = 'Monday'  
                elif t[3]==1:  
                    wkday = 'Tuesday'  
                elif t[3]==2:  
                    wkday = 'Wednesday'  
                elif t[3]==3:  
                    wkday = 'Thursday'  
                elif t[3]==4:  
                    wkday = 'Friday'  
                elif t[3]==5:  
                    wkday = 'Saturday'  
                elif t[3]==6:  
                    wkday = 'Sunday'  
                print('Weekday: {}'.format(wkday))  
                oled.text(wkday, 63-len(wkday)*8//2, 40)  
                oled.show()  
            else:  
                print_menu()  
        if isBlinkLED:  
            led.value(not led.value())  
        elif isActiveLED:  
            led.value(1)  
        else:  
            led.value(0)  
        prev_time = ticks_ms()  
