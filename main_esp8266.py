import time
from time import sleep
import ntptime
import machine
import os
from machine import Pin

from auth import (
   wifi_essid,
   wifi_pass
)

print('in main')
print ('Version 20230109_v_0.1')

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
        #print("OS error: {0}".format(err))
        pass

    print("Local time before synchronization：%s" %str(time.localtime()))

def startdht():
    print('in startdht')
    import publish_dht_esp8266 #choose which publish module to run
    print('done import')
#    dht_publish.run
    print('done run')

try:
    conectarwifi()
    startdht()
    print('in try catch hit ctrl-c now!')
    sleep(5)
    print('Too late')
except KeyboardInterrupt:
    print('keyboard')
    exit()
except:
    print('Error going to pass')
    pass
print('back in main, sleep 5 mins')
machine.deepsleep(30000)
machine.reset()
