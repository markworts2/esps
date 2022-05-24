import time
import sys
from time import sleep
import ntptime
import machine
from machine import Pin

from auth import (
   wifi_essid,
   wifi_pass
)

led = Pin(13, Pin.OUT)    # led no pin 13 do ESP32
print('in main')
print ('Version 20220329_v_0.1')

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

def get_html():
    print('in ina_219')
    import publish_ina219_esp8266
    print('done import')
    print('done run')

try:
    conectarwifi()
    get_html()
    print('in try')
except KeyboardInterrupt:
    print('keyboard')
    sys.exit()
except Exception as e:
     sys.print_exception(e)
#    pass
print('back in main, sleep 1 mins')
machine.deepsleep(60000)
#machine.reset()
