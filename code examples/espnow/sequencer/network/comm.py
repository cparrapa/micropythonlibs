import network
import espnow
import ujson

class Comm:
    def __init__(self, runtime):
        self.runtime = runtime
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.espnow = espnow.ESPNow()
        self.espnow.active(True)
        self.peers = set()

    def add_peer(self, mac):
        if mac not in self.peers:
            self.espnow.add_peer(mac)
            self.peers.add(mac)

    def send_program(self, mac, program):
        self.add_peer(mac)
        self.espnow.send(mac, ujson.dumps(program))

    def poll(self):
        host, msg = self.espnow.recv(0)
        if msg:
            program = ujson.loads(msg)
            self.runtime.load_program(program)
            self.runtime.run()