import ubluetooth
import hashlib

def get_short_id_from_mac():
    ble = ubluetooth.BLE()
    ble.active(True)
    mac = ble.config("mac")[1]
    print(mac)

    # Convert MAC bytes to a hash for better distribution
    mac_hash = hashlib.sha256(mac).digest()

    # Extract first 4 bytes and convert to integer
    short_id = int.from_bytes(mac_hash[:4], 'big')

    # Optionally limit to a specific range (e.g., 4-digit number)
    short_id = short_id % 1000000

    return short_id

# Usage
device_id = get_short_id_from_mac()
print(f"Device short ID: {device_id:04d}")
