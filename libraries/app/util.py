import esp32
import ubluetooth
import hashlib

BLE_NVS_NAMESPACE = 'storage'
BLE_NAME_NVS_KEY = 'ble_name'
BLE_DEFAULT_NAME = "otto"
BLE_BUFFER_SIZE=20


def get_ble_name_from_mac_address():
    ble = ubluetooth.BLE()
    ble.active(True)
    mac = ble.config("mac")[1]

    mac_hash = hashlib.sha256(mac).digest()

    short_id = int.from_bytes(mac_hash[:4], 'big')
    short_id = short_id % 1000000

    return BLE_DEFAULT_NAME + " " + str(short_id)


def get_ble_name():
    try:
        nvs = esp32.NVS(BLE_NVS_NAMESPACE)
        buff = bytearray(BLE_BUFFER_SIZE)
        actual_lenght = nvs.get_blob(BLE_NAME_NVS_KEY, buff)
        data = buff[:actual_lenght]
        return data.decode("utf-8")
    except OSError:
        try:
            return get_ble_name_from_mac_address()
        except:
            return BLE_DEFAULT_NAME


def set_ble_name(name):
    try:
        nvs = esp32.NVS(BLE_NVS_NAMESPACE)
        nvs.set_blob(BLE_NAME_NVS_KEY, name.encode())
        nvs.commit()
    except OSError:
        print("Settings BLE name failed")


def reset_ble_name():
    try:
        nvs = esp32.NVS(BLE_NVS_NAMESPACE)
        nvs.erase_key(BLE_NAME_NVS_KEY)
        nvs.commit()
    except OSError:
        print("Deleting BLE name failed")
