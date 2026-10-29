import gc
import time
import network
import urequests
import os
import json
import uhashlib

class WiFiManagerSlim:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self, max_retries=10, timeout=5):
        if not self.wlan.active():
            self.wlan.active(True)
            time.sleep(1)

        if self.wlan.isconnected():
            print(f"Already connected to WiFi: {self.ssid}")
            print(f"IP address: {self.wlan.ifconfig()[0]}")
            return True

        print(f"Connecting to WiFi: {self.ssid}...")
        self.wlan.connect(self.ssid, self.password)

        retry_count = 0
        while not self.wlan.isconnected() and retry_count < max_retries:
            print("Waiting for connection...")
            time.sleep(timeout)
            retry_count += 1

        if self.wlan.isconnected():
            print(f"Connected to WiFi: {self.ssid}")
            print(f"IP address: {self.wlan.ifconfig()[0]}")
            return True
        else:
            print(f"Failed to connect to WiFi: {self.ssid}")
            self.wlan.active(False)
            return False

    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
            self.wlan.active(False)
            print("Disconnected from WiFi")

class OttoInit:
    wifi_ssid: str
    wifi_password: str
    base_url: str
    wifi: WiFiManagerSlim
    file_list: list[tuple[str, str]] = []

    def __init__(self, wifi_ssid: str, wifi_password: str, base_url: str):
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.base_url = base_url
        self.wifi = WiFiManagerSlim(wifi_ssid, wifi_password)


    def get_file_list(self) -> None:
        response = urequests.get(self.base_url + "/firmware-connection/files")
        data = response.json()

        for file in data:
            if file['required']:
                self.file_list.append((file['file'], file['version']))

    def install(self):
        self.clean()

        if not self.wifi.connect():
            print("Failed to connect to WiFi, aborting init process")
            return

        self.get_file_list()

        for file, version in self.file_list:
            gc.collect()

            if not self.download_file(file):
                return

            time.sleep(0.5)

        self.create_version_lock()
        self.wifi.disconnect()


    def download_file(self, file: str) -> bool:
        try:
            response = urequests.get(self.base_url + "/firmware/file/" + file)

            if response.status_code != 200:
                print(f"Error downloading file, status code: {response.status_code}")
                return False

            with open(file, 'w') as f:
                f.write(response.text)

            response.close()
            print(f"Downloaded: {file}")
            return True

        except Exception as e:
            print(f"Error downloading file: {e}")
            return False

    def clean(self):
        files = os.listdir()
        for file in files:
            try:
                os.remove(file)
            except OSError:
                pass

    def create_version_lock(self) -> None:
        data = {"libraries": {}}

        for file, version in self.file_list:
            digest = self.get_file_digest(file)

            data['libraries'][file] = {"version": version, "digest": digest}

        try:
            with open("lock.json", "w") as f:
                json.dump(data, f)
                print("lock.json updated successfully")
                return True
        except Exception as e:
            print(e)
            print("Failed updating lock.json")
            return False

    def get_file_digest(self, file: str) -> str | None:
        gc.collect()
        try:
            with open(file, "rb") as f:
                content = f.read()
                sha256 = uhashlib.sha256()
                sha256.update(content)
                checksum = sha256.digest()
                checksum_hex = ''.join('{:02x}'.format(b) for b in checksum)
                return checksum_hex

        except Exception:
            print(f"Error reading downloaded file {file}")
            return None


def run(wifi_ssid, wifi_password, base_url):
    otto_init = OttoInit(wifi_ssid, wifi_password, base_url)
    otto_init.install()

run("WiFi", "password", "https://com-moravia-consulting-otto-be-540711117835.europe-west1.run.app/v1")
