from time import sleep
from time import time
from umqtt.simple import MQTTClient
import machine
from dht import DHT22
import onewire, ds18x20
from struct import unpack
from machine import Pin

print ('dht_publish_water_esp32.py  v25/10/23 15:04')

p4 = Pin(4, Pin.OUT) #power pin
p5 = Pin(5, Pin.IN) #read water pin
p3 = Pin(3, Pin.IN) #read water analogue pin


#connect to mqqt
SERVER = '192.168.86.248'  # MQTT Server Address (Change to the IP address of your Pi)
CLIENT_ID = 'ESP32_DHT22_Sensor'
TOPIC = b'temp_humidity'
rtc = machine.RTC()

print('Connecting to MQTT')
client = MQTTClient(CLIENT_ID, SERVER)
try:
   client.connect()   # Connect to MQTT broker
except IndexError:
   print ('index error: can not connect to MQQT')

print('turn on power pin 4')
p4.value(1) #turn on the power pin
sleep(1)
print('read pin 5 the sensor pin')
dreading = p5.value()
areading = p3.value()
print('turn off power pin')
p4.value(0)

# push to MQQT
try:
        date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())
        msg = date_str +  "," + str('water_p5') + "," + str(dreading)
        client.publish(TOPIC, msg)
        print (msg)   
        msg = date_str +  "," + str('water_p3') + "," + str(areading)
        client.publish(TOPIC, msg)
        print (msg)
except:
        date_str = "{2:02d}/{1:02d}/{0:4d} {4:02d}:{5:02d}".format(*rtc.datetime())
        msg = date_str +  "," + 'reading failed'
        print('Failed to read sensor.')
        client.publish(TOPIC,msg)

sleep(2)

