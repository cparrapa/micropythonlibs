import network
import espnow
from time import sleep
from otto4wd import OttoMecanum

# Initialize the robot (adjust connector numbers if needed)
robot = OttoMecanum()

# Define a speed value (within -50 to +50)
speed = 30
duration = 2  # seconds

# Initialize Wi-Fi interface in station mode
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Initialize ESP-NOW
e = espnow.ESPNow()
e.init()

# Add peer (replace with the MAC address of the remote controller)
peer = b'\xFF\xFF\xFF\xFF\xFF\xFF'  # Broadcast address
e.add_peer(peer)

def execute_command(command):
    if command == 'forward':
        print("Moving forward")
        robot.forward(speed)
    elif command == 'backward':
        print("Moving backward")
        robot.backward(speed)
    elif command == 'left':
        print("Turning left")
        robot.turn_left(speed)
    elif command == 'right':
        print("Turning right")
        robot.turn_right(speed)
    elif command == 'crab_left':
        print("Crabbing left")
        robot.crab_left(speed)
    elif command == 'crab_right':
        print("Crabbing right")
        robot.crab_right(speed)
    elif command == 'diag_left':
        print("Diagonal left")
        robot.diag_left(speed)
    elif command == 'diag_right':
        print("Diagonal right")
        robot.diag_right(speed)
    elif command == 'stop':
        print("Stopping")
        robot.stop()
    else:
        print(f"Unknown command: {command}")

# Main loop to listen for ESP-NOW messages
while True:
    host, msg = e.recv()
    if msg:
        command = msg.decode('utf-8')
        execute_command(command)
        sleep(0.1)  # Small delay to avoid overwhelming the robot
