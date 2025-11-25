import os
import urequests
import time
import gc
from wifi_manager import WiFiManager

log = print


BASE_URL = "http://192.168.1.136:8080/ota"

FILES = [
    "/update.py",
    "/rollback.py",
    "/status.py",
    "/blockdev_writer.py",
    "__init__.py",
]

# Since we cannot run pip or mprepare on the clients ESP, we download the OTA library and place in in lib/ota folder
def create_dirs():
    log("Creating required directories")
    try:
        try:
            os.mkdir('/lib')
        except OSError:
            pass

        try:
            os.mkdir('/lib/ota')
        except OSError:
            pass

        return True
    except Exception as e:
        log("Creating required directories failed")
        return False

# def download_file(url, dest_path):
#     try:
#         gc.collect()
#
#         response = urequests.get(url)
#
#         if response.status_code != 200:
#             if "__init__.py" in url:
#                 with open(dest_path, 'w') as f:
#                     f.write("")
#             else:
#                 log(f"Error downloading file, status code: {response.status_code}")
#                 return False
#
#         with open(dest_path, 'w') as f:
#             f.write(response.text)
#
#         response.close()
#         log(f"Downloaded: {dest_path}")
#         return True
#
#     except Exception as e:
#         log(f"Error downloading file: {e}")
#         return False
def download_file(url, dest_path, chunk_size=64):
    try:
        gc.collect()
        log(f"Free memory: {gc.mem_free()}")

        # Open the request in streaming mode
        response = urequests.get(url, stream=True)

        if response.status_code != 200:
            response.close()
            if "__init__.py" in url:
                with open(dest_path, 'w') as f:
                    f.write("")
                log(f"Created empty __init__.py at {dest_path}")
                return True
            else:
                log(f"Error downloading file, status code: {response.status_code}")
                return False

        # Write the file chunk by chunk to avoid loading everything into memory
        with open(dest_path, 'w') as f:
            while True:
                chunk = response.raw.read(chunk_size)
                if not chunk:
                    break
                # Convert bytes to string for text mode writing
                f.write(chunk.decode('utf-8'))
                # Free memory after processing each chunk
                gc.collect()

        # Always close the response
        response.close()
        log(f"Downloaded: {dest_path}")
        return True

    except Exception as e:
        log(f"Error downloading file: {e}")
        # Make sure we close the response if there was an exception
        try:
            if 'response' in locals():
                response.close()
        except:
            pass
        return False


def install_library(wifi_ssid, wifi_password, global_print, base_url=BASE_URL):
    global log
    log = global_print
    wifi = WiFiManager(wifi_ssid, wifi_password, log)

    try:
        if not wifi.connect():
            log("Failed to connect to WiFi, aborting installation")
            return False

        if not create_dirs():
            return False

        success_count = 0
        total_files = len(FILES)

        # Download each file
        for file_path in FILES:
            # Construct full URL and destination path
            file_url = base_url + file_path
            dest_path = f'/lib/ota{file_path}'

            # Download the file
            if download_file(file_url, dest_path):
                success_count += 1

            # Small delay between downloads and free memory
            gc.collect()
            time.sleep(0.5)

        log(f"Installation complete: {success_count}/{total_files} files downloaded successfully")

        # Test if the library works
        try:
            log("Testing OTA library installation...")
            import ota.status
            log("Import successful!")

            # Test if OTA functionality works
            log("Checking OTA status:")
            ota.status.status()
            log("OTA library installed successfully!")
            return True

        except Exception as e:
            log(f"Error testing OTA library: {e}")
            log("Installation may have failed or is incomplete.")
            return False

    except Exception as e:
        log(f"Installation error: {e}")
        return False
    finally:
        # Always disconnect WiFi when done
        if wifi.is_connected():
            wifi.disconnect()

