from wifi_manager import WiFiManager
import gc
import urequests
import time

FILES = [
  "adxl345.py",
  "main.py",
  "ottobuzzer.py",
  "ottomotor.py",
  "ottoneopixel.py",
  "ottooled.py",
  "ottosensors.py",
  "ottowalktus_code}")
            return False

        with open(dest_path, 'w') as f:
            f.write(response.text)

        response.close()
        del response
        print(f"Downloaded: {dest_path}")
        return True

    except Exception as e:
        print(f"Error downloading file: {e}")
        return False


def update_libraries(wifi_ssid, wifi_password, base_url, global_print=print):
    wifi = WiFiManager(wifi_ssid, wifi_password, print)

    try:
        if not wifi.connect():
            print("Failed to connect to WiFi, aborting installation")
            return False

        success_count = 0
        total_files = len(FILES)

        # Download each file
        for file_path in FILES:
            # Construct full URL and destination path
            file_url = base_url + file_path
            dest_path = file_path

            # Download the file
            if download_file(file_url, dest_path):
                success_count += 1

            # Small delay between downloads and free memory
            gc.collect()
            time.sleep(1)

        print(f"Installation complete: {success_count}/{total_files} files downloaded successfully")

    except Exception as e:
        print(f"Installation error: {e}")
        return False
    finally:
        # Always disconnect WiFi when done
        if wifi.is_connected():
            wifi.disconnect()
