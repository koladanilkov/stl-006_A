import time
import network
import app.secrets as secrets
from app.mymqtt import MQTTClient
from .hardwear import setKoefBrightnes, client_id, setPower, getPower, pwm17
import machine


mqtt_server = '109.248.175.143'
topic_sub_scan = b'controllers/scan'
topic_sub_koef_brightness = b'controllers/set/koef_brightness'
topic_sub_power = b'controller/'+ client_id + b'/power'
topic_sub_ip = b'controller/'+ client_id + b'/get/ip'
topic_sub_reset = b'controller/'+ client_id + b'/reset'
topic_sub_reset_all = b'controllers/reset'
topic_sub_web_repl = b'controller/'+ client_id + b'/web_repl'


topic_pub_health_check = b'controllers/' + client_id + b'/health_check'
topic_pub_scan = b'controllers/' + client_id
topic_pub_reset = b'controller/'+ client_id + b'/reset/ok'
topic_pub_status = b'controller/' + client_id + b'/satus'
topic_pub_ip = b'controller/' + client_id + b'/ip'

machineIp = '(0, 0, 0, 0)'
client = None


def connectToWiFi():
  global machineIp
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(secrets.WIFI_SSID, secrets.WIFI_PASSWORD)
  print('conneting to wifi..')
  while not station.isconnected():
      pass
  print('Connection successful')
  print(station.ifconfig())
  machineIp = station.ifconfig()[0]


def health_check_pub(msg):
  client.publish(topic_pub_health_check, str(msg))
  
def reset_pub():
  client.publish(topic_pub_reset, '1')

def sub_cb(topic, msg):
  print((topic, msg))
  if topic == topic_sub_scan and msg == b'1':
    client.publish(topic_pub_scan, str(getPower()))
  elif topic == topic_sub_power:
    power = min(max(int(msg), 15), 100)
    setPower(power)
    print('power = %s' %(power))
    client.publish(topic_pub_status, str(power))
  elif topic == topic_sub_koef_brightness:
    setKoefBrightnes(min(max(int(msg), 1), 20))
  elif (topic == topic_sub_reset or topic == topic_sub_reset_all) and msg == b'1':
    print('mqtt => reset')
    reset_pub()
    machine.reset()
  elif (topic == topic_sub_ip and msg == b'1'):
    print('mqtt => get ip')
    client.publish(topic_pub_ip, machineIp)
  elif (topic == topic_sub_web_repl):
    pwm17.duty(1023)
    time.sleep(10)
    exit()
    
def connect_and_subscribe():
  client = MQTTClient(client_id, mqtt_server, user = b'test', password = b'P@ssw0rd!')
  client.set_callback(sub_cb)
  client.connect()

  client.subscribe(topic_sub_power)
  client.subscribe(topic_sub_scan)
  client.subscribe(topic_sub_koef_brightness)
  client.subscribe(topic_sub_reset)
  client.subscribe(topic_sub_reset_all)
  client.subscribe(topic_sub_ip)
  client.subscribe(topic_sub_web_repl)
  print('Connected to %s MQTT broker, subscribed to topics: \n %s \n %s \n %s \n %s \n %s \n %s \n %s' % (mqtt_server, topic_sub_power, topic_sub_scan, topic_sub_koef_brightness, topic_sub_reset, topic_sub_reset_all, topic_sub_ip, topic_sub_web_repl))
  return client


def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()  
  
  
def connectToMQTT():
  global client
  try:
    client = connect_and_subscribe()
  except OSError as e:
    restart_and_reconnect()
