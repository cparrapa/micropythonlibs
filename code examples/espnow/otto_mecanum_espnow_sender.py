import network
import espnow
from time import sleep

# Initialize Wi-Fi interface in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.init()

# Add peer (replace with the MAC address of the receiver)
peer = b'\x24\x0A\xC4\x12\x34\x56'  # Example MAC address, replace with actual
e.add_peer(peer)

# List of commands to send
commands = [
    "forward",
    "backward",
    "turn_left",
    "turn_right",
    "crab_left",
    "crab_right",
    "diag_left",
    "diag_right",
    "stop"
]

# Send each command with a delay
for command in commands:
    print(f"Sending command: {command}")
    e.send(peer, command)
    sleep(2)

print("All commands sent.")
