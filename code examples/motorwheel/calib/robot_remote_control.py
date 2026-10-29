
import socket
from robot_library import Robot

robot = Robot(left_pin=14, right_pin=27)
robot.calibrate(left_offset=5, right_offset=0)

# Setup socket server
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

def handle_command(cmd):
    cmd = cmd.strip().lower()
    if cmd == 'forward':
        robot.forward(60)
    elif cmd == 'backward':
        robot.backward(60)
    elif cmd == 'left':
        robot.turn_left(60)
    elif cmd == 'right':
        robot.turn_right(60)
    elif cmd == 'stop':
        robot.stop()
    elif cmd == 'dance':
        robot.dance()
    elif cmd == 'spin':
        robot.joyful_spin()
    else:
        print('Unknown command:', cmd)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request_str = request.decode('utf-8')
    print('Request:', request_str)

    # Parse command from request
    try:
        cmd = request_str.split(' ')[1].strip('/')
        handle_command(cmd)
        response = "HTTP/1.1 200 OK
Content-Type: text/html

Command executed: {}".format(cmd)
    except:
        response = "HTTP/1.1 400 Bad Request

Invalid command"

    cl.send(response)
    cl.close()
