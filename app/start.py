import gc
gc.collect()
import utime
import app.hardwear as hardwear
import app.conection as conection
import webrepl
import machine
conection.connectToWiFi()
conection.connectToMQTT()
webrepl.start()
timeLastRedact = utime.ticks_ms()
timeLastReconect = utime.ticks_ms()
timeLastReboot = utime.ticks_ms()
while True:
  try:
    conection.client.check_msg()
    if utime.ticks_ms() - timeLastRedact > 100:
        hardwear.brightnesCorecting()
        timeLastRedact = utime.ticks_ms()
    if utime.ticks_ms() - timeLastReconect > 300000:
        conection.connectToMQTT()
        timeLastReconect = utime.ticks_ms()
    if utime.ticks_ms() - timeLastReboot > 18000000:
        machine.reset()
      
  except OSError as e:
    conection.restart_and_reconnect()
