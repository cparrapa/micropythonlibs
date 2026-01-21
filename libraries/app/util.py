import esp32
import ubluetooth
import hashlib

BLE_NVS_NAMESPACE = 'cnfg'
BLE_NAME_NVS_KEY = 'ble_name'
BLE_DEFAULT_NAME = "otto"


def get_nvs_value(key: str) -> str | None:
    nvs = esp32.NVS(BLE_NVS_NAMESPACE)
    try:
        blob_length = nvs.get_blob(key, bytearray())
        buffer = bytearray(blob_length)
        nvs.get_blob(key, buffer)
        return buffer.decode()
    except OSError:
        return None


def set_nvs_value(key: str, value: str):
    nvs = esp32.NVS(BLE_NVS_NAMESPACE)
    nvs.set_blob(key, value.encode())
    nvs.commit()


def delete_nvs_key(key: str):
    nvs = esp32.NVS(BLE_NVS_NAMESPACE)
    try:
        nvs.erase_key(key)
        nvs.commit()
    except OSError:
        # The key is already deleted
        return



def get_ble_name_from_mac_address():
    ble = ubluetooth.BLE()
    ble.active(True)
    mac = ble.config("mac")[1]

    mac_hash = hashlib.sha256(mac).digest()

    short_id = int.from_bytes(mac_hash[:4], 'big')
    short_id = short_id % 1000000

    return BLE_DEFAULT_NAME + " " + str(short_id)


def get_ble_name():
    found_nvs_value = get_nvs_value(BLE_NAME_NVS_KEY)
    if not found_nvs_value:
        try:
            return get_ble_name_from_mac_address()
        except:
            return BLE_DEFAULT_NAME

    return found_nvs_value


def set_ble_name(name):
    try:
        set_nvs_value(BLE_NAME_NVS_KEY, name)
    except OSError:
        print("Settings BLE name failed")


def reset_ble_name():
    delete_nvs_key(BLE_NAME_NVS_KEY)
