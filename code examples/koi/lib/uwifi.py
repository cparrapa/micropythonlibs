import wifi
import socketpool
import ipaddress
import adafruit_minimqtt.adafruit_minimqtt as MQTT
import esp32_now
from adafruit_ntp import NTP
from screen import Screen
import time
import rtc
import sys

screen = Screen()
import ssl
from time import sleep
import adafruit_requests

__version__ = "1.0.12"
message = None

class Radio:
    def __init__(self,channel,peer=b'\xff\xff\xff\xff\xff\xff'):
        wifi.radio.tx_power = 5
        self.radio = esp32_now.Radio()
        self.radio.add_peer(peer)
        self.radio.channel = channel

    def send(self, buf, peer=b'\xff\xff\xff\xff\xff\xff'):
        self.radio.send(buf, peer)
    
    def sendForKey(self,key,value):
        buf = {'key':key,'value':value}
        buf = str(buf)
        self.send(buf)

    def read(self):
        r = self.radio.packet()
        if r: # addr and payload
            message = r['payload'].decode()
            try:
                eval(message)
                return message
            except:
                return r['payload'].decode()
        return None
    
    def readForKey(self,key):
        r = self.radio.packet()
        if r: # addr and payload
            try:
                message =  r['payload'].decode()
                message = eval(message)
                if message["key"] == key:
                    return message["value"]
            except:
                return None
        return None
        
class WIFI:
    def __init__(self):
        wifi.radio.tx_power = 5
        self._wifi = wifi
        self.ip=''
        self.netmask=''
        self.gateway=''
        self.dns=''

        self.mqtt = None

        self.ntp = None
        self.now = None
        self.message = {}
        
        self._pool = socketpool.SocketPool(wifi.radio)
        self._ssl_context = ssl.create_default_context()

        self.mqttHost = ""
        self.mqttClientId = ""
        self.mqttUser = ""
        self.mqttPassword = ""

        self.interval = time.monotonic()

        self._api_key = ""
        self._api_url = "https://restapi.amap.com/v3/weather/weatherInfo?city={}&key={}&extensions=all"

    def connect(self,name,pwd):
        self.__init__()
        message = ["succeed"]
        try:
            screen.fill((0, 0, 0))
            screen.rect(0,0,180,20,(0, 0, 255),1)
            screen.text("正在连接WIFI...",3,3,1,(255, 255, 255))
            screen.refresh()
            self._wifi.radio.connect(str(name),str(pwd))

            self.ip=self._wifi.radio.ipv4_address
            self.netmask=self._wifi.radio.ipv4_subnet
            self.gateway=self._wifi.radio.ipv4_gateway
            self.dns=self._wifi.radio.ipv4_dns
            
        except ValueError as e:
            errorMsg = str(e)
            print(errorMsg)
            if errorMsg == "password length must be 8-63":
                message = [
                    "WIFI密码错误",
                    "密码长度需要在8~63之间"
                    ]
            elif errorMsg == "ssid length must be 1-32":
                message = [
                    "WIFI名称错误",
                    "名称长度需要在1~32之间"
                    ]
            else:
                message = [
                    "未知错误：",
                    errorMsg
                    ]
        except ConnectionError as e:
            errorMsg = str(e)
            if errorMsg == "No network with that ssid":
                message = [
                    "未找到此WIFI名称",
                    "请检查WIFI名称是否正确"
                ]
            elif errorMsg == "Unknown failure 15":
                message = ["密码错误"]
            elif errorMsg == "Unknown failure 2":
                message = ["网络质量不佳，请重试"]
            else:
                message = [
                    "未知错误：",
                    errorMsg
                    ]
        if message[0] != "succeed":
            screen.fill((0, 0, 0))
            screen.rect(0,0,180,20,(255, 0, 0),1)
            screen.text("WIFI连接失败，请重试",3,3,1,(255, 255, 255))
            y = 30
            for i in message:
                screen.text(i,3,y,1,(255, 255, 255))
                y+=30
            screen.refresh()
            raise Exception("WIFI connection Error!")
        else:
            screen.rect(0,0,180,20,(0, 255, 0),1)
            screen.text("连接成功",3,3,1,(255, 255, 255))
            screen.text(('IP:'+str(self.ip)),3,25,1,(255, 255, 255))
            screen.refresh()
            sleep(2)
        return True
    
    def disconnect(self):
        try:
            self._wifi.radio.stop_station()
        except:
            return False
        return True
    
    def isconnect(self):
        if self._wifi.radio.ipv4_address:
            return True
        return False

    
    def Configuration(self):
        return(self.ip,self.netmask,self.gateway,self.dns)
    
    def connectChecker(self):
        if not(self.isconnect()):
            raise Exception('Please connect WIFI !')


    def mqttConnect(self,url,id,user,pwd):
        self.connectChecker()
        self.mqtt = MQTT.MQTT(
            broker=url,
            port=1883,
            username=user,
            password=pwd,
            socket_pool=self._pool,
            client_id=id,
            ssl_context=self._ssl_context,
        )

        self.mqttHost = url
        self.mqttClientId = id
        self.mqttUser = user
        self.mqttPassword = pwd

        self.mqtt.connect()
        self.mqtt.on_message = self.receiveMessage
        self.mqtt.on_disconnect = self.disconnected
    
    def publish(self,feed,message):
        if time.monotonic() - self.interval > 0.5:
            self.interval = time.monotonic()
            self.connectChecker()
            self.mqttSecurityDisposal(self.mqtt.publish,(feed,str(message)))

    def mqttSecurityDisposal(self,method,arguments):
        try:
            method(*arguments)
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            print("1:",e)
            count = 0
            while True:
                try:
                    self.mqttConnect(self.mqttHost,self.mqttClientId,self.mqttUser,self.mqttPassword)
                    break
                except KeyboardInterrupt:
                    sys.exit()
                except Exception as e2:
                    print("2:",e2)
                    continue
                finally:
                    count += 1
                    if count == 10:
                        raise ConnectionError("Retry failed")
                    time.sleep(2)
            #method(*arguments)




    def subscribe(self,feed):
        self.connectChecker()
        self.mqtt.subscribe(feed)

    def receiveMessage(self,client, feed_id, message):
        
        self.message[feed_id] = message
        
        print("Feed {0} received new message: {1}".format(feed_id, self.message[feed_id]))

    def disconnected(self,client, feed_id, message):
        self.connectChecker()
        print("Disconnected from MQTT!")

    def getMessage(self,feed_id):
        self.connectChecker()
        self.mqttSecurityDisposal(self.mqtt.loop,())
        sleep(0.3)
        try:
            value = self.message[feed_id]
            self.message[feed_id] = None
            return value
        except KeyError:
            return None

    def initNTP(self,tz_offset=8,server="ntp1.aliyun.com"):
        self.connectChecker()
        self.ntp = NTP(socketpool.SocketPool(self._wifi.radio),tz_offset=tz_offset,server=server)
        num = 0
        while True:
            num+=1
            if num==3:
                break
            try:
                rtc.RTC().datetime = self.ntp.datetime
                break
            except OSError as e:
                print("Network timeout")
                print(e)

    def updateNTPtime(self):
        pass
    
    def getNTPtime(self,timeFormat):
        self.connectChecker()
        data = ""
        if timeFormat=="year":
            data = time.localtime()[0]
        elif timeFormat=="mon":
            data = time.localtime()[1]
        elif timeFormat=="mday":
            data = time.localtime()[2]
        elif timeFormat=="wday":
            data = time.localtime()[6]
        elif timeFormat=="hour":
            data = time.localtime()[3]
        elif timeFormat=="min":
            data = time.localtime()[4]
        elif timeFormat=="sec":
            data = time.localtime()[5]
        elif timeFormat=="yday":
            data = time.localtime()[7]
            
        return data
    
    def setAPIKey(self,api_key):
        self._api_key = api_key

    def get_weather(self, city_code, day):
        try:
            self._api_url = self._api_url.format(city_code, self._api_key)

            request = self._create_request()
            response = request.get(self._api_url)
            weather_data = response.json()
            response.close()

            # 解析实时天气数据
            city = weather_data["forecasts"][0]["city"]
            weather = weather_data["forecasts"][0]["casts"][day]["dayweather"]
            wind = weather_data["forecasts"][0]["casts"][day]["daywind"]
            windPower = weather_data["forecasts"][0]["casts"][day]["daypower"]
            temperature = weather_data["forecasts"][0]["casts"][day]["daytemp_float"]
            
            return [city,weather,wind,windPower,temperature]

        except Exception as e:
            print("get_weather Error:", e)
            return [-1]*5

    def _create_request(self):
        try:
            request = adafruit_requests.Session(self._pool, ssl_context=self._ssl_context)
            return request
        except Exception as e:
            print("_create_request Error:", e)
            return None
    

class TCP:
    def __init__(self):
        self.wifi = WIFI()
        self.port = None
        self.timeout = 0
        self.backlog = 1
        self.maxbuf = 1024
        self.pool = None
        self.host = None
        self.s = None
        self.buf = bytearray(self.maxbuf)
        self.conn = None

    def tcpStart(self,port):
        self.port = port
        self.wifi.connectChecker()
        self.pool = socketpool.SocketPool(self.wifi._wifi.radio)
        self.host = str(self.wifi._wifi.radio.ipv4_address) 
        print("Create TCP Server socket", (self.host, self.port))
        screen.fill((0, 0, 0))
        screen.text('等待连接中、、、',5,10,1,(255, 255, 255))
        screen.text('ip:'+str(self.host),5,30,1,(255, 255, 255))
        screen.text('端口:'+str(self.port),5,50,1,(255, 255, 255))
        screen.refresh()
        s = self.pool.socket(self.pool.AF_INET, self.pool.SOCK_STREAM)
        s.settimeout(None)
        s.bind((self.host, self.port))
        s.listen(self.backlog)
        print("Wating for connected...")
        self.conn,addr = s.accept()
        self.conn.settimeout(self.timeout)
        print(addr)
        screen.fill((0, 0, 0))
        screen.text('tcp连接成功！',5,10,1,(0, 170, 0))
        screen.text('对方ip:'+addr[0],5,30,1,(255, 255, 255))
        screen.refresh()

    
    def read(self):
        self.wifi.connectChecker()
        if self.conn:
            size = self.conn.recv_into(self.buf, self.maxbuf)
            data = self.buf[:size].decode()
            return data
        else:
            print("plase start tcpStart!!")
    
    def send(self,message):
        data = message.encode()
        self.conn.send(data)
