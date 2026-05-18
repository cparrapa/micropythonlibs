import board
import math
import array
from audiobusio import PDMIn
import binascii
import json
import socketpool
import wifi
import time

__version__ = "1.0.5"


def mean(values):
    return sum(values) / len(values)
class Audio:

  def __init__(self):
    self.mic = PDMIn(clock_pin=board.MIC_CLK, data_pin=board.MIC_DAT, sample_rate=16000, bit_depth=16)
    pass
  
  def loudness(self):
    samples = array.array('h', [0] * 320)
    self.mic.record(samples, len(samples))
    minbuf = int(mean(samples))
    samples_sum = sum(
        float(sample - minbuf) * (sample - minbuf)
        for sample in samples
    )
    audoSize = math.sqrt(samples_sum / len(samples))
    audoSize = min(20000,audoSize)
    audoSize = int(4095/20000*audoSize)
    return audoSize

  def recognize(self,sec=3,vid=1537):
    s = socketpool.SocketPool(wifi.radio)
    addr = s.getaddrinfo("ai2.kittenbot.cn", 20204)[0][-1]
    # addr = s.getaddrinfo("192.168.0.23", 20204)[0][-1]
    b = array.array("h", [0] * 16000*sec)
    self.mic.record(b, len(b))
    n = binascii.b2a_base64(b).decode().strip()
    tcp = s.socket()
    tcp.connect(addr)
    data = ('{"mode":"voice","op":1,"vid":%s,"voc":"%s"}\n' %(vid,n))
    index = 0
    while True:
      print("%d/%d" %(index,len(data)))
      try:
        sendSizi = tcp.send(data[index:])
        index+=sendSizi
        if index >= len(data):
          break
      except OSError:
        pass
    data = bytearray(256)
    tcp.recv_into(data)
    result = json.loads(data.decode())
    if result['err_no'] == 0:
      return result['result'][0]
    raise Exception(result['err_msg'])

if __name__ == '__main__':
   wifi.radio.connect("Kittenbot","kittenbot428")
   a = Audio()
   b = a.recognize()
   print(b)