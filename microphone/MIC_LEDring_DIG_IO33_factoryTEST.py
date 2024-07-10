from machine import Pin
import neopixel
import time

# 定義LED的數量
NUM_LEDS = 13

# 定義GPIO引腳
SOUND_SENSOR_PIN = 33
LED_PIN = 4

# 初始化聲音感測器
sound_sensor = Pin(SOUND_SENSOR_PIN, Pin.IN)

# 初始化LED環
np = neopixel.NeoPixel(Pin(LED_PIN), NUM_LEDS)

def set_leds(sound_detected):
    """根據聲音檢測設置點亮的LED數量"""
    leds_to_light = int((sound_detected / 4095) * NUM_LEDS)
    for i in range(NUM_LEDS):
        if i < leds_to_light:
            np[i] = (0, 0, 255)  # 藍色
        else:
            np[i] = (0, 0, 0)    # 關閉LED
    np.write()

while True:
    # 讀取聲音感測器的值
    sound_detected = sound_sensor.value()
    
    # 將sound_detected映射到0到4095之間的值
    sound_level = sound_detected * 4095  # 假設數字感測器輸出為0或1
    
    # 根據聲音級別設置LED
    set_leds(sound_level)
    
    # 小延遲以去除感測器讀數抖動
    time.sleep(0.1)
