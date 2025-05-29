import network

# Initialize the network interface b'\x08\xd1\xf9\xfb\xf5\xc8
wlan = network.WLAN(network.STA_IF)
# Activate the WLAN Interface
wlan.active(True)

# Check if the interface is active (connected)
if wlan.active():
    # Get the MAC address
    mac_address = wlan.config("mac")
    print(mac_address)
    print("Device MAC Address:", ":".join(["{:02X}".format(byte) for byte in mac_address]))
else:
    print("Wi-Fi is not active.")