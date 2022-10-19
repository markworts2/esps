import time
from time import sleep
import ntptime
import machine
from machine import Pin

from auth import (
   wifi_essid,
   wifi_pass
)

print('in main')

#Conect to WiFi
def conectarwifi():
    print('in wifi')
    import network
    wlan = network.WLAN(network.STA_IF)
    print(wlan.active())
    wlan.active(True)
    sleep(3)
    print(wlan.active())
    x = 1
    if not wlan.isconnected():
        print('connecting to network...',wifi_essid)
        wlan.connect(wifi_essid, wifi_pass)
        while not wlan.isconnected() or x > 5:
            sleep(5)
            x = x + 1
            if x == 6:
              break
            print('Not connected',x)
            try:
              wlan.active(True)
            except OSError as err:
              print ("OS error in 5 wifi loop")
              wlan.active(True)
            print(wlan.status())
    print('network config:', wlan.ifconfig())
    x = 1
    while x < 5:
      x = x + 1
      try:
        print("Local time before synchronization：%s" %str(time.localtime()))
        ntptime.settime()
      except:
        pass

    print("Local time before synchronization：%s" %str(time.localtime()))

def startdht():
    print('in startdht')
    import publish_dht_esp32 #choose with publish module to run
    print('done import')
#    dht_publish.run
    print('done run')

try:
    conectarwifi()
    startdht()
    print('in try')
except KeyboardInterrupt:
    print('keyboard')
    sys.exit()
except:
    pass
print('back in main, sleep 60000')
machine.deepsleep(60000)
