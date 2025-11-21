import gc
import time
import network
import urequests
import os

FILES = [
  "adxl345.py",
  "main.py",
  "ottobuzzer.py",
  "ottomotor.py",
  "ottoneopixel.py",
  "ottooled.py",
  "ottosensors.py",
  "ottowalkroll.py",
  "rc.py",
  "util.py",
  "ssd1306.py",
  "wifi_manager.py",
  "update_library.py"
]

def download_file(url, dest_path):
    try:
        response = urequests.get(url)

        if response.status_code != 200:
            print(f"Error downloading file, status code: {response.status_code}")
            return False

        with open(dest_path, 'w') as f:
            f.write(response.text)

        response.close()
        print(f"Downloaded: {dest_path}")
        return True

    except Exception as e:
        print(f"Error downloading file: {e}")
        return False


def update_libraries(wifi_ssid, wifi_password, libraries_url, global_print=print):
    wifi = WiFiManager(wifi_ssid, wifi_password, print)

    try:
        if not wifi.connect():
            print("Failed to connect to WiFi, aborting installation")
            return False

        success_count = 0
        total_files = len(FILES)

        # Download each file
        for file_path in FILES:
            file_url = libraries_url + file_path
            dest_path = file_path

            if download_file(file_url, dest_path):
                success_count += 1

            gc.collect()
            time.sleep(1)

        print(f"Installation complete: {success_count}/{total_files} files downloaded successfully")

    except Exception as e:
        print(f"Installation error: {e}")
        return False
    finally:
        if wifi.is_connected():
            wifi.disconnect()


class WiFiManager:
    def __init__(self, ssid, password, log = print):
        self.log = log
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self, max_retries=10, timeout=5):
        if not self.wlan.active():
            self.wlan.active(True)
            time.sleep(1)

        if self.wlan.isconnected():
            self.log(f"Already connected to WiFi: {self.ssid}")
            self.log(f"IP address: {self.wlan.ifconfig()[0]}")
            return True

        self.log(f"Connecting to WiFi: {self.ssid}...")
        self.wlan.connect(self.ssid, self.password)

        retry_count = 0
        while not self.wlan.isconnected() and retry_count < max_retries:
            self.log("Waiting for connection...")
            time.sleep(timeout)
            retry_count += 1

        if self.wlan.isconnected():
            self.log(f"Connected to WiFi: {self.ssid}")
            self.log(f"IP address: {self.wlan.ifconfig()[0]}")
            return True
        else:
            self.log(f"Failed to connect to WiFi: {self.ssid}")
            self.wlan.active(False)  # Turn off interface to save power
            return False

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
            self.wlan.active(False)
            self.log("Disconnected from WiFi")

    def is_connected(self):
        return self.wlan.isconnected()

    def ifconfig(self):
        return self.wlan.ifconfig()


def clean():
    files = os.listdir()
    for file in files:
        try:
            os.remove(file)
        except OSError:
            pass


def run(wifi_ssid, wifi_password, libraries_url):
    clean()
    update_libraries(wifi_ssid, wifi_password, libraries_url)

run("hotspot", "hotspot123", "https://koalotto.vercel.app/code/")
