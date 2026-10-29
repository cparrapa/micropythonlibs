import network
import time

class WiFiManager:
    def __init__(self, ssid, password, log = print):
        self.log = log
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self, max_retries=10, timeout=4):
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
