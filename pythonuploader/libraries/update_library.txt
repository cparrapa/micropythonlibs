from wifi_manager import WiFiManager
from machine import Pin, PWM
import config
import gc
import urequests
import time
import os
import util
import uhashlib
import json
import machine


class UpdateLibraryManager:
    wifi_ssid: str
    wifi_password: str
    base_url: str
    session_id: str
    session_files: list[str] = []
    session_files_full: list[dict] = []
    wifi: WiFiManager | None = None
    buzzer = None
    buzzer_enabled = True

    def __init__(self, log = print):
        self.log = log

    # Configure Otto parameters
    def configure(self, wifi_ssid: str, wifi_password: str, session_id: str, base_url: str) -> None:
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.session_id = session_id
        self.base_url = base_url

    # Save configured parameters to persistent storage
    def save_configuration(self) -> None:
        util.set_nvs_value(config.NVS_WIFI_SSID_KEY, self.wifi_ssid)
        util.set_nvs_value(config.NVS_WIFI_PASSWORD, self.wifi_password)
        util.set_nvs_value(config.NVS_UPDATE_SESSION_ID, self.session_id)
        util.set_nvs_value(config.NVS_BASE_URL, self.base_url)
        util.set_nvs_value(config.NVS_UPDATE_MODE, config.NVS_UPDATE_MODE_VALUE)

    # Entrypoint for starting update libraries process
    def trigger_update_libraries(self, wifi_ssid: str, wifi_password: str, session_id: str, base_url: str):
        self.configure(wifi_ssid, wifi_password, session_id, base_url)

        # self.log("w:connecting")
        # if not self.test_configuration():
        #     self.log("w:failed")
        #     return

        # self.log("w:success")

        self.save_configuration()
        machine.reset()

    # Load buzzer for sounds
    def load_buzzer(self):
        try:
            from ottobuzzer import OttoBuzzer
            # Initialize servo motors before buzzer
            PWM(Pin(13), freq=50)
            PWM(Pin(14), freq=50)

            self.buzzer = OttoBuzzer(25)
        except Exception as e:
            self.buzzer = None
            print(e)
            print("Failed buzzer initialization. Ignoring")

    # Play buzzer sound or ignore if buzzer not initialized
    def play_buzzer_emoji(self, emoji: str):
        if not self.buzzer_enabled:
            return

        if not self.buzzer:
            print("Buzzer is not initialized. Ignoring")
            return

        try:
            self.buzzer.play_emoji(emoji)
        except Exception:
            print("Failed playing buzzer emoji. Ignoring")
            return


    # Proceed with update libraries
    def update(self):
        # Update runs only once
        util.delete_nvs_key(config.NVS_UPDATE_MODE)

        # self.load_buzzer()

        # Loading stored configuration from NVS
        if not self.load_configuration():
            self.log("Failed loading configuration, some values may be missing. Aborting")
            # self.play_buzzer_emoji("sad")
            return self.cleanup(False)

        # self.play_buzzer_emoji("happy")

        # Connect to wifi
        if not self.connect_wifi():
            self.log("Failed connecting to wifi. Aborting")
            # self.play_buzzer_emoji("sad")
            return self.cleanup(False)

        # self.play_buzzer_emoji("happy")

        # Get session configuration from server
        if not self.get_session_configuration():
            self.log("Failed getting session configuration from the server. Aborting")
            # self.play_buzzer_emoji("sad")
            return self.cleanup(False)

        # self.play_buzzer_emoji("happy")


        # Download new files, store them as temp_, and verify their checksums
        if not self.update_files():
            self.log("Failed updating files. Aborting")
            self.send_device_event(config.EVENT_FAILED)
            # self.play_buzzer_emoji("sad")
            return self.cleanup(True)

        # self.play_buzzer_emoji("happy")

        # Backup files
        self.send_device_event(config.EVENT_FILES_BACKUP_START)
        if not self.backup_files():
            self.log("Failed backing up old files. Aborting")
            self.send_device_event(config.EVENT_FILES_BACKUP_FAILED)
            # self.play_buzzer_emoji("sad")
            return self.cleanup(True)
        else:
            # self.play_buzzer_emoji("happy")
            self.send_device_event(config.EVENT_FILES_BACKUP_SUCCESS)


        # Replace existing files with new temp_ files
        self.send_device_event(config.EVENT_FILES_REPLACE_START)
        if not self.replace_files():
            self.log("Failed replacing new files. Aborting")
            # self.play_buzzer_emoji("confused")
            self.send_device_event(config.EVENT_FILES_REPLACE_FAILED)
            self.send_device_event(config.EVENT_FILES_ROLLBACK_START)

            # Rollback to previous files in replacing failed
            if not self.rollback_files():
                # self.play_buzzer_emoji("confused")
                self.send_device_event(config.EVENT_FILES_ROLLBACK_FAILED)
            else:
                # self.play_buzzer_emoji("happyshort")
                self.send_device_event(config.EVENT_FILES_ROLLBACK_SUCCESS)

            return self.cleanup(True)
        else:
            # self.play_buzzer_emoji("happy")
            self.send_device_event(config.EVENT_FILES_REPLACE_SUCCESS)


        # Delete existing backup files. Can fail, no problem
        self.send_device_event(config.EVENT_FILES_BACKUP_DELETE_START)
        if not self.delete_backup():
            # self.play_buzzer_emoji("confused")
            self.send_device_event(config.EVENT_FILES_BACKUP_DELETE_FAILED)
        else:
            # self.play_buzzer_emoji("happy")
            self.send_device_event(config.EVENT_FILES_BACKUP_DELETE_SUCCESS)

        self.update_version_lock()

        self.send_device_event(config.EVENT_SUCCESS)
        # self.play_buzzer_emoji("superhappy")
        return self.cleanup(False)


    # Cleanup after successfull or unsuccessfull update
    def cleanup(self, send_failed_event: bool):
        try:
            if send_failed_event:
                self.send_device_event(config.EVENT_FAILED)

            # Cleanup
            util.delete_nvs_key(config.NVS_UPDATE_MODE)

            files = os.listdir()
            for file in files:
                if "temp_" in file or "bck_" in file:
                    try:
                        os.remove(file)
                    except OSError:
                        pass
        except Exception:
            pass

        machine.reset()


    # Check if Otto should proceed with update libraries
    def should_update(self) -> bool:
        return util.get_nvs_value(config.NVS_UPDATE_MODE) == config.NVS_UPDATE_MODE_VALUE

    # Load configuration from persistent storage
    def load_configuration(self) -> bool:
        wifi_ssid = util.get_nvs_value(config.NVS_WIFI_SSID_KEY)
        wifi_password = util.get_nvs_value(config.NVS_WIFI_PASSWORD)
        base_url = util.get_nvs_value(config.NVS_BASE_URL)
        session_id = util.get_nvs_value(config.NVS_UPDATE_SESSION_ID)

        if not wifi_ssid or not wifi_password or not base_url or not session_id:
            return False


        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.base_url = base_url
        self.session_id = session_id

        return True

    # Connect to wifi using WiFiManager
    def connect_wifi(self) -> bool:
        self.wifi = WiFiManager(self.wifi_ssid, self.wifi_password, self.log)
        return self.wifi.connect()

    # Check is configured parameters are valid and Otto can connect to the server
    def test_configuration(self) -> bool:
        gc.collect()
        return self.connect_wifi()

    # Replace existing files with new temp files
    def replace_files(self) -> bool:
        for file in self.session_files:
            temp_file = f"temp_{file}"
            try:
                os.stat(temp_file)
            except OSError:
                self.log(f"Temp file {temp_file} does not exist. Aborting")
                return False

            try:
                os.remove(file)
            except OSError:
                self.log(f"Original file {file} did not exist. No problem here")

            try:
                os.rename(temp_file, file)
                self.log(f"Replaced {file} with {temp_file}")
            except Exception as e:
                self.log(e)
                self.log(f"Failed replacing file {file} with {temp_file} ")
                return False

        return True

    # Rollback backups into previous files
    def rollback_files(self) -> bool:
        success = True
        for file in self.session_files:
            try:
                backup_name = f"bck_{file}"
                try:
                    os.stat(backup_name)
                except OSError:
                    self.log(f"Backup for {file}/{backup_name} not found. Skipping")
                    continue

                try:
                    os.remove(file)
                except OSError as e:
                    self.log(e)
                    self.log("Failed deleting new file, maybe it doesn't exist. No problem")
                    continue

                try:
                    os.rename(backup_name, file)
                except OSError as e:
                    self.log(e)
                    success = False
            except Exception as e:
                self.log(e)
                return False

        return success



    # Create a backup of files that are being downloaded
    def backup_files(self) -> bool:
        for file in self.session_files:
            try:
                try:
                    os.stat(file)
                except OSError:
                    self.log(f"File {file} does not exist yet. Not backing up")
                    continue

                backup_name = f"bck_{file}"
                with open(file, "rb") as source:
                    content = source.read()

                with open(backup_name, "wb") as backup:
                    backup.write(content)
            except Exception as e:
                self.log(f"Failed backing up file: {file}")
                self.log(e)
                return False

        return True

    # Delete backed up files. Can fail
    def delete_backup(self) -> bool:
        success = True

        for file in self.session_files:
            backup_name = f"bck_{file}"
            try:
                os.stat(backup_name)
            except Exception:
                self.log(f"Backup not found for file {file}/{backup_name}")
                continue

            try:
                os.remove(backup_name)
            except Exception as e:
                success = False
                self.log(e)
                self.log(f"Failed deleting backup file {file}/{backup_name}")

        return success


    # Update files - Update every file in session files
    def update_files(self) -> bool:
        for file in self.session_files:
            if not self.update_file(file, False):
                return False

        return True

    # Download and verify new library
    def update_file(self, file: str, is_retry: bool) -> bool:
        if not self.download_file(file):
            if not is_retry:
                self.log("Failed downloading file. Waiting 5s and retrying")
                time.sleep(5)
                return self.update_file(file, True)

            self.log("Failed downloading file again. Aborting")
            return False

        digest = self.get_downloaded_file_digest(file, True)

        if not digest:
            self.log("Failed generating digest for downloaded file. It may not be downloaded. Aborting")
            return False

        if not self.verify_file(file, digest):
            self.log("Failed verifying downloaded file. Aborting.")
            return False

        return True

    # Download file from server and mark it as temp_ for rollback
    def download_file(self, file: str) -> bool:
        try:
            gc.collect()

            response = urequests.get(self.__download_file_ep(file))

            if response.status_code != 200:
                self.log(f"Error downloading file, status code: {response.status_code}")
                return False


            with open(f"temp_{file}", 'wb') as f:
                f.write(response.content)

            response.close()
            return True
        except Exception as e:
            self.log(f"Error downloading file: {e}")
            return False

    # Get downloaded file SHA256 hex digest for verification
    def get_downloaded_file_digest(self, file: str, temp: bool) -> str | None:
        gc.collect()
        try:
            file_name = f"temp_{file}" if temp else file

            with open(file_name, "rb") as f:
                content = f.read()
                sha256 = uhashlib.sha256()
                sha256.update(content)
                checksum = sha256.digest()
                checksum_hex = ''.join('{:02x}'.format(b) for b in checksum)
                return checksum_hex

        except Exception:
            self.log(f"Error reading downloaded file {file}")
            return None

    # Verify file digest with server
    def verify_file(self, file: str, digest: str) -> bool:
        gc.collect()

        body_data = {
            'file': file,
            'digest': digest,
            'sessionId': self.session_id
        }
        body = json.dumps(body_data)
        headers = {'Content-Type': 'application/json'}

        try:
            response = urequests.post(self.__file_verify_ep(), data = body, headers = headers)
            is_verified = response.text == 'true'
            response.close()

            return is_verified
        except Exception as e:
            self.log("Failed file verification")
            return False

    # Send device event
    def send_device_event(self, type: str) -> bool:
        gc.collect()

        body_data = {
            "type": type,
            "sessionId": self.session_id
        }
        body = json.dumps(body_data)
        headers = {'Content-Type': 'application/json'}

        try:
            response = urequests.post(self.__send_device_event_ep(), data = body, headers = headers)
            response.close()
            return True
        except Exception:
            self.log("Failed sending device event")
            return False

    # Update lock.json with new libraries and their digests
    def update_version_lock(self) -> bool:
        data = {}

        try:
            with open('lock.json', 'r') as f:
                data = json.load(f)
        except Exception as e:
            self.log(e)
            self.log("Creating new lock.json from downloaded files")
            data['libraries'] = {}

        for file in self.session_files_full:
            digest = self.get_downloaded_file_digest(file["file"], False)

            if not digest:
                self.log(f"Failed getting for {file}. Skipping")
                continue

            data['libraries'][file["file"]] = {"version": file["version"], "digest": digest}

        try:
            with open("lock.json", "w") as f:
                json.dump(data, f)
                self.log("lock.json updated successfully")
                return True
        except Exception as e:
            self.log(e)
            self.log("Failed updating lock.json")
            return False

    # Get session configuration - files from server
    def get_session_configuration(self):
        gc.collect()

        try:
            response = urequests.get(self.__session_config_ep(False))
            self.session_files = [x["file"] for x in response.json()["files"]]
            self.session_files_full = response.json()["files"]
            response.close()
            return True
        except Exception as e:
            self.log("Failed loading session config")
            self.log(e)
            return False


    # Get endpoint URL for getting session config and testing connection
    def __session_config_ep(self, preflight: bool) -> str:
        preflight_param = "true" if preflight else "false"
        return self.base_url + config.EP_SESSION_CONFIG + "/" + self.session_id + "?preflight=" + preflight_param

    # Get endpoint URL for file digest verification
    def __file_verify_ep(self) -> str:
        return self.base_url + config.EP_FILE_VERIFY

    # Get endpoint URL for download files
    def __download_file_ep(self, file: str) -> str:
        return self.base_url + config.EP_DOWNLOAD_FILE + "/" + file + "?session=" + self.session_id

    # Get endpoint URL for sending device events
    def __send_device_event_ep(self) -> str:
        return self.base_url + config.EP_DEVICE_EVENT
