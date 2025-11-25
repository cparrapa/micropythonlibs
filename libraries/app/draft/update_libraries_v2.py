import gc
import time
import network

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

def force_defragmentation():
    """
    Force memory defragmentation by creating and deleting large objects
    """
    print(f"Before defrag: {gc.mem_free()} bytes free")

    # Create several large temporary objects to force memory compaction
    temp_objects = []
    try:
        # Try to allocate and immediately free several chunks
        for i in range(5):
            try:
                # Create progressively smaller chunks
                size = 8192 // (i + 1)  # 8KB, 4KB, 2.7KB, 2KB, 1.6KB
                temp_objects.append(bytearray(size))
            except:
                break

        # Delete all at once
        del temp_objects

        # Multiple garbage collection passes
        for _ in range(3):
            gc.collect()
            time.sleep_ms(10)

    except Exception as e:
        print(f"Defragmentation attempt failed: {e}")

    print(f"After defrag: {gc.mem_free()} bytes free")

def aggressive_memory_cleanup():
    """
    More aggressive memory cleanup
    """
    import sys

    # Clear any cached modules that might be holding memory
    if hasattr(sys, 'modules'):
        modules_to_clear = []
        for name in sys.modules:
            if name.startswith('urequests') or name.startswith('json'):
                modules_to_clear.append(name)

        for name in modules_to_clear:
            try:
                del sys.modules[name]
            except:
                pass

    # Force multiple GC passes
    for i in range(5):
        gc.collect()
        time.sleep_ms(20)

    # Try defragmentation
    force_defragmentation()


def download_file(url, dest_path):
    """
    Enhanced download function with fragmentation handling
    """
    print(f"\n--- Starting download: {dest_path} ---")

    # Pre-download memory management
    aggressive_memory_cleanup()

    free_before = gc.mem_free()
    print(f"Free memory: {free_before} bytes")


    # Fallback to urequests with aggressive defragmentation
    try:
        # Force defragmentation before importing urequests
        force_defragmentation()
        import urequests

        # Another cleanup after import
        gc.collect()
        time.sleep_ms(100)

        print(f"Making HTTP request to {url}")
        response = urequests.get(url)

        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            response.close()
            return False

        print("Response received, writing to file...")

        # Write in very small chunks with frequent cleanup
        with open(dest_path, 'w') as f:
            content = response.text
            chunk_size = 64  # Very small chunks

            for i in range(0, len(content), chunk_size):
                f.write(content[i:i+chunk_size])

                # Frequent garbage collection
                if i % (chunk_size * 8) == 0:  # Every 512 bytes
                    gc.collect()
                    time.sleep_ms(2)

        response.close()
        del response
        del content  # Explicitly delete content

        # Final cleanup
        gc.collect()
        time.sleep_ms(50)

        print(f"✓ Successfully downloaded {dest_path}")
        return True

    except MemoryError as e:
        print(f"Memory error during urequests download: {e}")
        print(f"Free memory: {gc.mem_free()} bytes")
        return False
    except Exception as e:
        print(f"urequests download failed: {e}")
        return False

def update_libraries(wifi_ssid, wifi_password, base_url, global_print=print):
    """
    Memory-fragmentation-aware update function
    """
    wifi = WiFiManager(wifi_ssid, wifi_password, global_print)

    try:
        # Initial memory cleanup
        aggressive_memory_cleanup()

        if not wifi.connect():
            global_print("Failed to connect to WiFi, aborting installation")
            return False

        success_count = 0
        total_files = len(FILES)

        # Start with smallest files to avoid early fragmentation
        FILES_BY_SIZE = [
            "util.py",
            "ottobuzzer.py",
            "ottoneopixel.py",
            "ottooled.py",
            "rc.py",
            "adxl345.py",
            "ottosensors.py",
            "ssd1306.py",
            "ottomotor.py",
            "wifi_manager.py",
            "ottowalkroll.py",
            "main.py"
        ]

        for i, filename in enumerate(FILES_BY_SIZE):
            global_print(f"\n=== File {i+1}/{total_files}: {filename} ===")

            # Pre-file cleanup
            global_print("Preparing memory...")
            aggressive_memory_cleanup()

            free_mem = gc.mem_free()
            global_print(f"Free memory before download: {free_mem} bytes")

            file_url = base_url + filename

            # Try download
            if download_file(file_url, filename):
                success_count += 1
                global_print(f"✓ {filename} downloaded successfully")
            else:
                global_print(f"✗ Failed to download {filename}")

                # Try one more time after aggressive cleanup
                global_print("Retrying after memory cleanup...")
                aggressive_memory_cleanup()
                time.sleep(2)

                if download_file(file_url, filename):
                    success_count += 1
                    global_print(f"✓ {filename} downloaded on retry")
                else:
                    global_print(f"✗ {filename} failed completely")

            # Long recovery period between files
            global_print("Memory recovery pause...")
            time.sleep(5)
            aggressive_memory_cleanup()

            final_mem = gc.mem_free()
            global_print(f"Free memory after file: {final_mem} bytes")

            # Stop if memory is critically fragmented
            if final_mem < 12000:
                global_print("⚠️ Memory critically low, stopping downloads")
                break

        global_print(f"\n🏁 Installation complete: {success_count}/{total_files} files downloaded successfully")
        return success_count == total_files

    except Exception as e:
        global_print(f"Installation error: {e}")
        return False
    finally:
        # Always disconnect WiFi when done
        if wifi.is_connected():
            wifi.disconnect()

        # Final cleanup
        aggressive_memory_cleanup()

# Your FILES list (reorder as needed)
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
    "wifi_manager.py"
]
