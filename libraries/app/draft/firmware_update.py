from wifi_manager import WiFiManager
import time
import machine
import gc

try:
    import ota.update
    import ota.status
except ImportError:
    raise Exception("OTA libraries not found")


FIRMWARE_URL = "http://192.168.1.136:8080/firmware/latest.app-bin"

def check_ota_ready(log):
    if ota.status.ready():
        log("Device is OTA-ready!")
        ota.status.status()
        return True
    else:
        log("Device is not OTA ready")
        return False


def update_firmware(wifi_ssid, wifi_password, log, url=FIRMWARE_URL):
    if not check_ota_ready(log):
        return

    try:
        wifi = WiFiManager(wifi_ssid, wifi_password, log)
        if not wifi.connect():
            log("Wifi connection failed")


        log("Starting OTA update...")
        gc.collect()
        ota.update.from_file(url)
        log("OTA update completed. Device will reboot shortly.")
    except Exception as e:
        log(e)
        raise
    finally:
        if wifi.is_connected():
            wifi.disconnect()
